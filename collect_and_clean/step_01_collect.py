import json
from collections import defaultdict

ARXIV_JSON_DUMP = "data/arxiv-metadata-oai-snapshot.json"
SRC_DIR = "data/src"
MAX_PAPERS = 1000

VALID_LICENCES = set(['http://creativecommons.org/licenses/by/4.0/', 'http://creativecommons.org/licenses/publicdomain/', 'http://creativecommons.org/licenses/by-nc-sa/3.0/','http://creativecommons.org/licenses/by/3.0/', 'http://creativecommons.org/licenses/by-sa/4.0/', 'http://creativecommons.org/licenses/by-nc-sa/4.0/', 'http://creativecommons.org/publicdomain/zero/1.0/'])


# Selecting papers with permissive licence
papers = []
licences = defaultdict(int)
with open(ARXIV_JSON_DUMP, 'r') as f:
    for line in f:
        paper = json.loads(line.strip())
        # count the licence
        licences[paper["license"]] += 1
        if paper["license"] in VALID_LICENCES:
            papers.append(paper)

        # if len(papers) >= MAX_PAPERS:
        #     break
# print(licences)
print(sum(licences.values()), 'papers in total')
print(len(papers), 'papers with a valid licence')


# Selecting papers from Computer Science
cs_papers = []
for paper in papers:
    categories = [c.split(".")[0].lower() for c in paper["categories"].split()]
    if "cs" in categories:
        cs_papers.append(paper)
print(len(cs_papers), 'cs_papers with a valid licence')


# Sort papers by date (newest first)
import dateutil.parser as parser

cs_papers.sort(key=lambda x: parser.parse(x['versions'][0]['created']), reverse=True)


import os
import time
import requests
import hashlib
import tarfile

# export.arxiv.org
ARXIV_SOURCE_URL = "https://export.arxiv.org/e-print/{arxiv_id}v1"

def download_source(arxiv_id: str, output_dir: str):
    """Download LaTeX source from arXiv ID."""

    # Possible target filenames
    tar_path     = f"{output_dir}/{arxiv_id}.tar"
    targz_path   = f"{output_dir}/{arxiv_id}.tar.gz"

    # If either file already exists -> skip
    if os.path.exists(tar_path) or os.path.exists(targz_path):
        # print(f"[SKIP] {arxiv_id} already downloaded")
        return

    url = ARXIV_SOURCE_URL.format(arxiv_id=arxiv_id)

    try:
        response = requests.get(url, stream=True, timeout=30)
        if response.status_code != 200:
            print(f"[ERROR] HTTP {response.status_code} for {arxiv_id}")
            return
        
        ext = ".tar"
        ct = response.headers.get("Content-Type", "")
        if "gzip" in ct:
            ext =  ".tar.gz"

        src_file = f"{output_dir}/{arxiv_id}{ext}"
        with open(src_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        #print(f"[OK] Saved: {src_file}")

    except Exception as e:
        print(f"[ERROR] {arxiv_id}: {e}")
    


import os
from tqdm import tqdm
import random
import shutil

#for paper in tqdm(cs_papers[x*MAX_PAPERS:y*MAX_PAPERS]):
for paper in tqdm(cs_papers):
    arxiv_id = paper["id"]
    download_source(arxiv_id=arxiv_id, output_dir=SRC_DIR)
