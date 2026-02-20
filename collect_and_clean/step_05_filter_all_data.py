# install this lib : pip install {PATH}/ParaPLUIE
import os
from PPLUIE import ppluie
import json
import time
import glob
from tqdm import tqdm

SRC_DIR = "data/extract_tex"
TEX_DIR = "data/final_dataset"

template = "DETECTREV"

device = "cuda" 
root_path = "" #fill with location of the model 


model_name = "Qwen/Qwen3-14B"


scorer = ppluie(root_path+"/"+model_name, device)
scorer.setTemplate(template)

print("Loading over")

def import_corpus(path,filename):
    with open(path+filename, 'r') as corpus_file:
        liste_paragraphs=[json.loads(line.strip('\n')) for line in corpus_file]  
    return liste_paragraphs 

liste_problem=[]
threshold=5.55
start = time.time()
accepted,rejected=0,0


#for idx,file in enumerate(tqdm(sorted(glob.glob(SRC_DIR + "/*"))[x:y])):
for idx,file in enumerate(tqdm(sorted(glob.glob(SRC_DIR + "/*")))):
    article=import_corpus("",file)
    parag_kept=[]
    for parag in article:
        parag.pop("final_is_diff")
        parag.pop("final_parag_old")
        parag["final_parag"]=parag["final_parag_clean"]
        parag.pop("final_parag_clean")
        comments_kept=[]
        
        for comment in parag["candidate_comments"]:
            try:
                score_ppluie=scorer(reference=parag["final_parag"], hypothese=comment)
                if score_ppluie>threshold:
                    accepted+=1
                    comments_kept.append(comment)
                else:
                    rejected+=1
            except Exception as e:
                print("index fail:",idx)
                print(type(e))
                print(e)
                liste_problem.append(file)
        parag["candidate_comments"]=comments_kept
        if len(comments_kept)>0:
            parag_kept.append(parag)
        
    if len(parag_kept)>0:
        file_export=open(TEX_DIR+"/"+file.split("/")[-1],'w')
        for parag in parag_kept:
            json.dump(parag,file_export)
            file_export.write('\n')
        file_export.close()
end = time.time()
print("Time ppluie parapluie")
print(end - start)
print("accepted",accepted,"rejected",rejected)
print("Problems:",len(liste_problem),liste_problem)

