import json
import os
import difflib

# --- CONFIGURATION ---
SOURCE_FOLDER = './dataset_part1b'  # Dossier contenant vos .jsonl
OUTPUT_DATA = 'import_label_studio_1_clean.json'
OUTPUT_SUMMARY = 'index_fichiers_1_clean.json'
MAX_TOTAL_TASKS = 38  # Seuil maximum de paragraphes à importer

def get_dual_colored_html(ref, cand):
    """Génère le miroir HTML pour la référence et le candidat."""
    ref_words = ref.split()
    cand_words = cand.split()
    d = difflib.Differ()
    diff = list(d.compare(ref_words, cand_words))
    
    html_ref, html_cand = [], []
    for word in diff:
        marker = word[0]
        # Échappement LaTeX/HTML
        content = word[2:].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        if marker == ' ':  # COMMUN -> VERT
            span = f'<span style="color: #28a745; font-weight: bold;">{content}</span>'
            html_ref.append(span)
            html_cand.append(span)
        elif marker == '-':  # REF ONLY
            html_ref.append(content)
        elif marker == '+':  # CAND ONLY
            html_cand.append(content)
            
    return " ".join(html_ref), " ".join(html_cand)

all_tasks = []
summary = {}
task_counter = 0

# On récupère tous les fichiers jsonl et on les trie pour garder un ordre logique
files = sorted([f for f in os.listdir(SOURCE_FOLDER) if f.endswith('.jsonl')])

print(f"Début du traitement de {len(files)} fichiers...")

for filename in files:
    if task_counter >= MAX_TOTAL_TASKS:
        print("Seuil maximum atteint. Arrêt du traitement.")
        break
        
    start_index = task_counter
    file_path = os.path.join(SOURCE_FOLDER, filename)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        file_tasks_count = 0
        
        for line in f:
            if task_counter >= MAX_TOTAL_TASKS:
                break
                
            try:
                obj = json.loads(line.strip())
                final_parag_raw = obj.get("final_parag_clean", "")
                id_parag = obj.get("id_parag")
                
                candidates_data = []
                for i, cand_text in enumerate(obj.get("candidate_comments", [])):
                    ref_colored, cand_colored = get_dual_colored_html(final_parag_raw, cand_text)
                    # ref_colored, cand_colored = final_parag_raw, cand_text
                    candidates_data.append({
                        "label": f"Candidat n°{i + 1}",
                        "ref_html": ref_colored,
                        "cand_html": cand_colored
                    })
                
                # Ajout de la tâche à la liste globale
                all_tasks.append({
                    "data": {
                        "candidates": candidates_data,
                        "source_file": id_parag  # Utile pour la traçabilité dans LS ==> ICI l'id PARAG
                    }
                })
                
                task_counter += 1
                file_tasks_count += 1
                
            except Exception as e:
                print(f"Erreur dans le fichier {filename}: {e}")

    # Enregistrement dans le sommaire si des tâches ont été ajoutées
    if file_tasks_count > 0:
        summary[filename] = {
            "first_task_index": start_index,
            "last_task_index": task_counter - 1,
            "total_added": file_tasks_count
        }
        print(f"Fichier {filename} traité : {file_tasks_count} tâches ajoutées.")

# --- SAUVEGARDE ---
with open(OUTPUT_DATA, 'w', encoding='utf-8') as f:
    json.dump(all_tasks, f, indent=2, ensure_ascii=False)

with open(OUTPUT_SUMMARY, 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print(f"\nTerminé !")
print(f"Total tâches : {task_counter}")
print(f"Données enregistrées dans : {OUTPUT_DATA}")
print(f"Sommaire enregistré dans : {OUTPUT_SUMMARY}")