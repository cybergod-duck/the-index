import json
import os
import csv

BASE_DIR = r'C:\Projects\the-index'
CSV_FILE = os.path.join(BASE_DIR, 'data.csv')
STATE_FILE = os.path.join(BASE_DIR, 'posted_state.json')
PIN_DIR = os.path.join(BASE_DIR, 'premium_pins')

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"posted": [], "remaining": []}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)

def initialize_state():
    state = load_state()
    if not state["remaining"] and not state["posted"]:
        with open(CSV_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            state["remaining"] = [row['slug'] for row in reader]
    save_state(state)
    return state

def get_next_batch(count=15):
    state = load_state()
    batch = state["remaining"][:count]
    return batch

def mark_as_posted(slugs):
    state = load_state()
    for slug in slugs:
        if slug in state["remaining"]:
            state["remaining"].remove(slug)
            state["posted"].append(slug)
    save_state(state)

if __name__ == "__main__":
    state = initialize_state()
    next_up = get_next_batch(15)
    print(f"Total Posted: {len(state['posted'])}")
    print(f"Remaining: {len(state['remaining'])}")
    print(f"Next Batch: {next_up}")
