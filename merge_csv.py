import csv
import os

BASE_DIR = r"C:\Projects\the-index"
CSV_FILE = os.path.join(BASE_DIR, "data.csv")
VAULT_FILE = os.path.join(BASE_DIR, "the-vault.txt")

existing_slugs = set()
all_data = []

# Read existing data.csv
with open(CSV_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        existing_slugs.add(row['slug'])
        all_data.append(row)

# Append vault data
added = 0
if os.path.exists(VAULT_FILE):
    with open(VAULT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 3:
                industry = parts[0].strip()
                pain = parts[1].strip()
                slug = parts[2].strip()
                if slug not in existing_slugs:
                    all_data.append({"industry": industry, "pain_point": pain, "slug": slug})
                    existing_slugs.add(slug)
                    added += 1

# Write unified data.csv
with open(CSV_FILE, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["industry", "pain_point", "slug"])
    writer.writeheader()
    writer.writerows(all_data)

print(f"Merged {added} new rows into data.csv. Total rows: {len(all_data)}")
