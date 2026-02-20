
import json
import random
import argparse
from tqdm import tqdm
from generators import init_generator, TextParser
import os
import time

def check_revision(data, model, limit=None):
    data = list(data)

    random.seed(0)
    random.shuffle(data)

    if limit:
        data = data[:limit]

    generator = init_generator(model)
    model_name = model.rstrip("/").split("/")[-1]
    output_path = f"output/{model_name}.jsonl"
    os.makedirs("output", exist_ok=True)

    # Clear the file at the start
    open(output_path, "w").close() 

    start = time.time()
    with open(output_path, "a") as f:
        for item in tqdm(data, total=len(data)):
            id_parag = item['id_parag']
            candidates = item['candidate_comments']
            target = item['final_parag']
            for i, candidate in enumerate(candidates):
                prediction = generator.predict_revision(candidate, target)
                prediction_parsed = TextParser().parse(prediction)

                f.write(json.dumps({
                    "id_parag": id_parag,
                    "id_candidate": i,
                    "prediction": prediction_parsed
                }) + "\n")

    end = time.time()
    print(end - start)

def main():
    parser = argparse.ArgumentParser(description='Generate queries')
    parser.add_argument('--model', type=str, required=True)
    parser.add_argument('--limit', type=int, default=None)
    args = parser.parse_args()

    with open('annotated_subset.jsonl') as f:
        data = [json.loads(line) for line in f]

    check_revision(data, args.model, limit=args.limit)

main()