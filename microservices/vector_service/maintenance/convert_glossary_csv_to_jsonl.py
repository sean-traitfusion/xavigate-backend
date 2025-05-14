import csv
import json
from pathlib import Path

def csv_to_jsonl(csv_path: str, jsonl_path: str):
    with open(csv_path, newline='', encoding='utf-8') as infile, open(jsonl_path, 'w', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        for row in reader:
            json_obj = {
                "id": row.get("ID", "").strip(),
                "term": row.get("Term", "").strip(),
                "definition": row.get("Definition", "").strip(),
                "example": row.get("Example", "").strip(),
                "related_terms": [t.strip() for t in row.get("Related Terms", "").split(',') if t.strip()],
                "related_to": [t.strip() for t in row.get("Related To", "").split(',') if t.strip()],
                "term_type": row.get("Term Type", "").strip()
            }
            outfile.write(json.dumps(json_obj) + '\n')

if __name__ == "__main__":
    csv_file = "data/Glossary.csv"
    jsonl_file = "data/glossary.jsonl"
    csv_to_jsonl(csv_file, jsonl_file)
    print(f"✅ Converted {csv_file} to {jsonl_file}")