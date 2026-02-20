import json
import glob
import os
import re

TEX_DIR = "tex"
CLEAN_DIR="tex_cleaned"

def has_non_command_comments(list_content: str) -> bool:
    """
    Return True if the LaTeX file contains comments that are NOT LaTeX commands.
    """
    comment_start = re.compile(r"(?<!\\)%")  # unescaped %

    for line in list_content:
        m = comment_start.search(line)
        if not m:
            continue

        # extract text after '%'
        comment = line[m.start() + 1 :].strip()
        if not comment:
            continue  # empty comment like "%"

        # if comment starts with "\" -> it's a LaTeX command, ignore
        if comment.startswith("\\"):
            continue

        # otherwise it's a plain comment -> revision-like
        return True

    return False


def keep_inside_document(text_content:str):
    new_content=[]    
    for line in text_content.splitlines():
        line=remove_commands(line)
        if r"\begin{document}" in line:
            new_content=[]        
        new_content.append(line)        
        if r"\end{document}" in line:
            break
    return new_content

eq_token="[EQUATION]"
def remove_tables_and_figures(list_content):
    write_token=True
    new_content=[]
    for line in list_content:
        if (r"\begin{sidewaystable" in line) or (r"\begin{table" in line) or (r"\begin{figure" in line) or (r"\begin{equation" in line) or (r"\begin{align" in line) or (r"\begin{tikz" in line) or (r"\begin{algorithm" in line):
            write_token=False
            #cprint(line, "red")
        elif (r"\end{sidewaystable" in line) or (r"\end{table" in line) or (r"\end{figure" in line) or (r"\end{equation" in line) or (r"\end{align" in line) or (r"\end{tikz" in line) or (r"\end{algorithm" in line):
            write_token=True  
            #cprint(line, "red")
            if (r"\end{equation" in line):
                new_content.append(eq_token)
                #cprint(eq_token, "green")
        elif write_token:
            new_content.append(line)
            #cprint(line, "green")
       # else:
            #cprint(line, "red")
    return new_content
        
def is_empty(list_content):
    return all(isinstance(s, str) and s.isspace() for s in list_content) or len(list_content)==0


def remove_commands(text_line):
    text_line=re.sub(r"\\vspace\*?\{[^}]*\}", "", text_line)
    text_line=re.sub(r"\\soulregister\*?\{[^}]*\}", "", text_line)
    text_line=re.sub(r"\\sethlcolor\*?\{[^}]*\}", "", text_line)
    text_line=re.sub(r"\\input\*?\{[^}]*\}", "", text_line)
    text_line=re.sub(r"\\bibliography\*?\{[^}]*\}", "", text_line)
    text_line=re.sub(r"\\bibliographystyle\*?\{[^}]*\}", "", text_line)
    text_line=re.sub(r"\\label\*?\{[^}]*\}", "", text_line)
    text_line=re.sub(r"\\maketitle", "", text_line)
    text_line=re.sub(r"\\linenumbers", "", text_line)
    text_line=re.sub(r"\\newpage", "", text_line)
    text_line=re.sub(r"\\appendix", "", text_line)
    text_line=re.sub(r"\\noindent", "", text_line)
    text_line=re.sub(r"\\onecolumn", "", text_line)
    if (r"\newcommand" in text_line) or (r"\renewcommand" in text_line) or (r"\author" in text_line) or (r"\cortext" in text_line) or (r"\address" in text_line) or (r"\icml" in text_line):
        text_line=""
    return text_line


def clean_file(og_text_path:str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    
    # try to open tar safely
    try:
        tex = open(og_text_path, "r")
    except :
        print(f"[WARN] Could not open tar file: {og_text_path}. Empty mapping created.")
        return
    
    try:
        content = tex.read()
    except:
        print("problem reading file")
        return
    list_content = remove_tables_and_figures(keep_inside_document(content))
    
    if not is_empty(list_content): 
        if has_non_command_comments(list_content):
            with open(output_dir+"/"+og_text_path.split("/")[-1],"w") as clean_file:
                clean_file.write('\n'.join(list_content))


for file in glob.glob(TEX_DIR + "/*"):
    if file.endswith(".tex"):
        print(file)
        clean_file(og_text_path=file, output_dir=CLEAN_DIR)
