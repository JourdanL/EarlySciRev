import json
import glob
from collections import defaultdict

SRC_DIR = "src"
TEX_DIR = "tex"



import os
import re
import tarfile
import hashlib

def arxiv_id_from_tarpath(tar_path: str) -> str:
    """
    Given a path like ".../2101.00001v1.tar.gz" or ".../2101.00001v1.tar",
    return "2101.00001v1".
    """
    name = os.path.basename(tar_path)

    if name.endswith(".tar.gz"):
        name = name[:-7]          # remove ".tar.gz"
    elif name.endswith(".tar"):
        name = name[:-4]          # remove ".tar"

    return name


def has_non_command_comments(tex_content: str) -> bool:
    """
    Return True if the LaTeX file contains comments that are NOT LaTeX commands.
    """
    comment_start = re.compile(r"(?<!\\)%")  # unescaped %

    for line in tex_content.splitlines():
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

def extract_tex_files(tar_path: str, output_dir: str):
    """
    Extract .tex files from an arXiv tarball, store them in `output_dir`,
    rename each using a short SHA1 hash, and write a mapping file.

    If the tar file cannot be opened, create an empty mapping TSV.
    """
    os.makedirs(output_dir, exist_ok=True)

    # try to open tar safely
    try:
        tar = tarfile.open(tar_path, "r:*")
    except (tarfile.TarError, FileNotFoundError, IsADirectoryError):
        #print(f"[WARN] Could not open tar file: {tar_path}. Empty mapping created.")
        return

    # extract .tex files
    with tar:
        try:
            for member in tar.getmembers():
                if member.isfile() and member.name.lower().endswith(".tex"):

                    original = member.name
                    h = hashlib.sha1(original.encode("utf-8")).hexdigest()[:16] + ".tex"
                    out_path = os.path.join(output_dir, arxiv_id_from_tarpath(tar_path) + '-' + h)


                    src = tar.extractfile(member)
                    if src is None:
                        continue

                    content = src.read()

                    if not has_non_command_comments(content.decode("utf-8", errors="ignore")):
                        continue

                    with open(out_path, "wb") as dst:
                        dst.write(content)
        except(EOFError):
            print(tar_path+" end of file problem")
            return

            
    #print(f"[OK] Extracted {len(mapping)} tex files from {tar_path}")
    #print(f"[OK] Mapping written to {mapping_tsv}")


for file in glob.glob(SRC_DIR + "/*"):
    if file.endswith((".tar", ".tar.gz")):
        print(file)
        extract_tex_files(tar_path=file, output_dir=TEX_DIR)
