import time
import csv
import json
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIG ---
BASE_DIR = Path(r'C:\Projects\the-index')
CSV_FILE = BASE_DIR / 'data.csv'
STATE_FILE = BASE_DIR / 'posted_state.json'
PROFILE_DIR = BASE_DIR / 'chrome_profile_final'
LOGS_DIR = BASE_DIR / 'training_logs'

if not LOGS_DIR.exists():
    LOGS_DIR.mkdir()

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"posted": [], "remaining": []}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)

def log_selector(field_type, element):
    """Log winner properties for tomorrow's solo bot."""
    try:
        data = {
            "timestamp": time.time(),
            "field": field_type,
            "id": element.get_attribute("id"),
            "class": element.get_attribute("class"),
            "placeholder": element.get_attribute("placeholder") or element.get_attribute("aria-placeholder"),
            "aria-label": element.get_attribute("aria-label"),
            "tag": element.tag_name,
            "role": element.get_attribute("role")
        }
        log_file = LOGS_DIR / "winners.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(data) + "\n")
    except:
        pass

def run_titan_auto_log_30():
    state = load_state()
    posted = state.get("posted", [])
    
    # Load data
    all_data = []
    with CSV_FILE.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_data.append(row)
            
    # Batch size: 30
    to_post = [row for row in all_data if row['slug'] not in posted][:30]
    
    if not to_post:
        print("🎉 No pins left to post!")
        return

    print(f"👻 AUTO-LOG GHOST MODE: {len(to_post)} PINS")
    print("NO TERMINAL PROMPT: I'll detect success by watching the URL change.")
    
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={PROFILE_DIR}")
    chrome_options.add_argument("--profile-directory=Default")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        for row in to_post:
            slug = row['slug']
            industry = row['industry'].strip()
            pain = row['pain_point'].strip()
            title = f"Best CRM for {industry} (2026) #{industry.replace(' ', '')}"
            description = f"Stop struggling with {pain}. See the full review on THE INDEX. #CRM #Software #{industry.replace(' ', '')}"
            link = f"https://crmindex.net/{slug}/"

            print(f"\n--- ⚡ PIN: {slug} ---")
            driver.get("https://www.pinterest.com/pin-builder/")
            
            filled = {"title": False, "desc": False, "link": False}
            starting_url = driver.current_url

            print("👂 Click Title, Desc, or Link... I'll type instantly.")
            
            while not all(filled.values()):
                try:
                    el = driver.switch_to.active_element
                    placeholder = (el.get_attribute("placeholder") or el.get_attribute("aria-placeholder") or "").lower()
                    label = (el.get_attribute("aria-label") or "").lower()
                    el_id = (el.get_attribute("id") or "").lower()
                    val = el.get_attribute("value") or ""
                    text = el.text or ""

                    if val or text:
                        if not filled["title"] and ("title" in placeholder or "title" in label): filled["title"] = True
                        if not filled["desc"] and ("tell" in placeholder or "description" in placeholder): filled["desc"] = True
                        if not filled["link"] and ("link" in placeholder or "destination" in placeholder or "pin-draft-link" in el_id): filled["link"] = True
                        continue

                    if not filled["title"] and ("title" in placeholder or "title" in label):
                        print("   🖋️ Typing Title...")
                        el.send_keys(title); log_selector("title", el)
                        filled["title"] = True; time.sleep(1)

                    elif not filled["desc"] and ("tell" in placeholder or "description" in placeholder or "tell" in label):
                        print("   🖋️ Typing Description...")
                        el.send_keys(description); log_selector("description", el)
                        filled["desc"] = True; time.sleep(1)

                    elif not filled["link"] and ("link" in placeholder or "destination" in placeholder or "pin-draft-link" in el_id):
                        print("   🖋️ Typing Link...")
                        el.send_keys(link); log_selector("link", el)
                        filled["link"] = True; time.sleep(1)
                except: pass
                time.sleep(0.4)
            
            print("✅ Fields filled. UPLOAD image and click PUBLISH.")
            print("👂 Watching for publication... (I'll auto-log when the page changes)")
            
            # Wait for publication (URL change or refresh)
            while driver.current_url == starting_url or "/pin-builder/" in driver.current_url:
                # If the URL contains a new pin ID, it's definitely posted
                if "/pin/" in driver.current_url and "/pin-builder/" not in driver.current_url:
                    break
                time.sleep(2)
            
            # Success detection
            print(f"🎉 Success detected for {slug}!")
            if slug not in posted:
                posted.append(slug)
            state["posted"] = posted
            save_state(state)
            print(f"💾 Logged success. Moving to next.")
            time.sleep(3)

    finally:
        driver.quit()

if __name__ == "__main__":
    run_titan_auto_log_30()
