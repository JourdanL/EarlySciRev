import json
import glob
import os
import re
from tqdm import tqdm
from Levenshtein import distance
import pydetex.parsers as texpars

CLEAN_DIR="tex_cleaned"
EXTRACT_DIR="extract_tex"


def split_units(text):
    return [l for l in text.splitlines() if l.strip()]

def best_window_match(comment_text, final_text):
    units = split_units(final_text)
    best = None

    for size in range(1, len(units)+ 1):
        for i in range(len(units) - size + 1):
            window = "\n".join(units[i:i+size])
            lev = distance(comment_text, window)
            ratio = lev / max(len(comment_text), len(window))
            if best is None or ratio < best["ratio"]:
                best = {
                    "window": window,
                    "ratio": ratio,
                    "lev": lev,
                    "start": i,
                    "size": size
                }
    return best


def is_comment_line(line):
    return re.match(r"\s*%", line) is not None

def strip_comment_prefix(text):
    cleaned = []

    for line in text.splitlines():
        # Remove leading spaces + % + optional single space
        cleaned.append(re.sub(r"^\s*%*\s?", "", line))

    return "\n".join(cleaned)


def is_empty_final(line):
    return line.strip() == ""

def is_empty_comment(line):
    return re.fullmatch(r"\s*%*\s*", line) is not None



def group_consecutive_blocks(lines):
    #comment_start = re.compile(r"(?<!\\)%")
    blocks = []

    current = []
    current_clean = []
    current_type = None

    for line in lines:
        is_comment = is_comment_line(line) #bool(comment_start.search(line))
        block_type = "comment" if is_comment else "final"        
        line=strip_comment_prefix(line)
        if block_type=="final":
            line_clean=re.sub("⇱COMMENT_PERCENTAGE_SYMBOL⇲","\%",texpars.remove_comments(line))
                
        else:
            line_clean=line

        # Check for empty separator lines
        if (
            (block_type == "final" and is_empty_final(line)) or
            (block_type == "comment" and is_empty_comment(line))
        ):
            # Close current block if any
            if current:
                blocks.append({
                    "type": current_type,
                    "text": " ".join(current),#"text": "\n".join(current)
                    "text_clean":" ".join(current_clean)
                })
                current = []
                current_clean = []
                current_type = None
            continue  # do not include separator line

        # Normal block accumulation
        if current_type is None or block_type == current_type:
            if len(current)>0:
                if current[-1][-1]==".":
                    current.append("\n"+line)
                    current_clean.append("\n"+line_clean)
                else:
                    current.append(line)
                    current_clean.append(line_clean)
            else:
                current.append(line)
                current_clean.append(line_clean)
        else:
            blocks.append({
                "type": current_type,
                "text": " ".join(current),#"text": "\n".join(current)
                "text_clean":" ".join(current_clean)
            })
            current = [line]
            current_clean = [line_clean]

        current_type = block_type

    # Flush last block
    if current:
        blocks.append({
            "type": current_type,
            "text": " ".join(current),#"text": "\n".join(current)
            "text_clean":" ".join(current_clean)
        })

    return blocks


def find_block_pairs(list_content):
    blocks = group_consecutive_blocks(list_content)
    cpt_pairs = 0

    list_matching={}
    for idx, block in enumerate(blocks):
        if block["type"] != "comment":
            continue

        for idx_neighbour in range(max(0, idx - 5), min(idx + 5, len(blocks))):
            if idx_neighbour == idx:
                continue

            candidate = blocks[idx_neighbour]
            if candidate["type"] != "final":
                continue

            #comment_text = block["text"]
            comment_text = strip_comment_prefix(block["text"])
            final_text = candidate["text"]
                

            if len(comment_text) < 100:
                continue

            ##################
            match = best_window_match(comment_text, final_text)

            if match and match["ratio"] <= 0.70:
                cpt_pairs += 1
                if idx_neighbour not in list_matching.keys():
                    list_matching[idx_neighbour]=[idx]
                else:
                    list_matching[idx_neighbour].append(idx)

                    
    dict_matching=[{"final_parag_old":blocks[idx_fin]["text"],"final_parag_clean":blocks[idx_fin]["text_clean"],
                    "candidate_comments":[blocks[idx_com]["text"] for idx_com in list_idx_com],
                    "final_is_diff" :abs(len(blocks[idx_fin]["text"].replace(' ', ''))-len(blocks[idx_fin]["text_clean"].replace(' ', '')))>=2} for idx_fin,list_idx_com in list_matching.items()]
    return cpt_pairs,dict_matching

def extract_rev(og_text_path:str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    
    # try to open tar safely
    try:
        tex = open(og_text_path, "r")
    except :
        print(f"[WARN] Could not open tar file: {og_text_path}. Empty mapping created.")
        return
    
    content = tex.read()
    return find_block_pairs(content.splitlines())



#################################################

cpt_total=0
for file in tqdm(glob.glob(CLEAN_DIR + "/*")):
    if file.endswith(".tex"):
        #print(file)
        cpt_article,pairing_parag=extract_rev(og_text_path=file, output_dir=CLEAN_DIR)
        cpt_total+=cpt_article
        if len(pairing_parag)>0:
            with open(EXTRACT_DIR+"/"+file.split("/")[-1][:-3]+"jsonl","w") as extract_file:
                for pair in pairing_parag:
                    json.dump(pair, extract_file)
                    extract_file.write('\n')
print("TOTAL NUMBER OF REVISED PAIRS :",cpt_total)

