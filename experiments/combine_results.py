import json
from collections import defaultdict

input_files = [
    "phi-4",
    "gemma-3-4b-it",
    "gemma-3-12b-it",
    "Qwen3-4B",
    "Qwen3-14B",
    "Llama-3.1-8B-Instruct",
    "Olmo-3-7B-Instruct"
]

output_file = "output/results.jsonl"

combined = defaultdict(lambda: defaultdict(dict))

for filename in input_files:
    with open(f"output/{filename}.jsonl", "r") as f:
        for line in f:
            line = line.strip()
            obj = json.loads(line)
            id_parag = obj["id_parag"]
            id_candidate = obj["id_candidate"]
            combined[id_parag][id_candidate][filename] = obj["prediction"]

with open(output_file, "w") as f:
    for id_parag, candidates in combined.items():
        for id_candidate, predictions in candidates.items():
            record = {
                "id_parag": id_parag,
                "id_candidate": id_candidate,
                **predictions
            }
            f.write(json.dumps(record) + "\n")

print(f"Combined file saved as {output_file}")
