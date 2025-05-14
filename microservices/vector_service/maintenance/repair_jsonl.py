from pathlib import Path
import json

INPUT_FILE = "bulk_chunks_all.jsonl"
OUTPUT_FILE = "bulk_chunks_all_cleaned.jsonl"

def sanitize_line(line: str) -> str:
    return line.strip().replace('\u2028', ' ').replace('\u2029', ' ')

def clean_jsonl():
    input_path = Path(INPUT_FILE)
    output_path = Path(OUTPUT_FILE)

    cleaned = 0
    skipped = 0

    with input_path.open("r", encoding="utf-8") as infile, output_path.open("w", encoding="utf-8") as outfile:
        for i, line in enumerate(infile, start=1):
            clean_line = sanitize_line(line)
            if not clean_line:
                skipped += 1
                continue
            try:
                obj = json.loads(clean_line)
                outfile.write(json.dumps(obj, ensure_ascii=False) + "\n")
                cleaned += 1
            except json.JSONDecodeError as e:
                print(f"⚠️ Skipping line {i}: {e}")
                skipped += 1

    print(f"\n✅ Done: {cleaned} lines cleaned, {skipped} lines skipped.")
    print(f"🧼 Cleaned output written to {OUTPUT_FILE}")

if __name__ == "__main__":
    clean_jsonl()