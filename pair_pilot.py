import time
import csv
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIG ---
BASE_DIR = Path(r'C:\Projects\the-index')
CSV_FILE = BASE_DIR / 'data.csv'
STATE_FILE = BASE_DIR / 'posted_state.json'
PROFILE_DIR = BASE_DIR / 'chrome_profile_final'
PIN_DIR = BASE_DIR / 'premium_pins'

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"posted": [], "remaining": []}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)

def run_pair_pilot():
    state = load_state()
    posted = state.get("posted", [])
    
    # Load data
    all_data = []
    with CSV_FILE.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_data.append(row)
            
    # Next 15
    to_post = [row for row in all_data if row['slug'] not in posted][:15]
    
    if not to_post:
        print("🎉 No pins left!")
        return

    print(f"🚀 PAIR-PILOT (Enhanced): Starting batch of {len(to_post)}")
    
    # Init Chrome
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
            title = f"Best CRM for {industry} ({time.strftime('%Y')})"
            description = f"Stop struggling with {pain}. We compared the top software solutions for {industry}. See the full review on THE INDEX. #CRM #Software"
            link = f"https://crmindex.net/{slug}/"
            image = PIN_DIR / f"pin-{slug}.png"

            print(f"\n--- ⚡ PIN: {slug} ---")
            driver.get("https://www.pinterest.com/pin-builder/")
            
            print("⏳ Waiting for page load (10s)...")
            time.sleep(10)
            
            # Helper to find by multiple selectors
            def find_el(selectors):
                for sel in selectors:
                    try:
                        el = driver.find_element(By.XPATH, sel)
                        if el.is_displayed(): return el
                    except: continue
                return None

            # 1. Fill fields
            print("🖋️ Filling Title...")
            title_box = find_el([
                "//input[contains(@placeholder, 'Add your title')]",
                "//textarea[contains(@placeholder, 'Add your title')]",
                "//*[@data-test-id='pin-builder-draft-title']"
            ])
            if title_box:
                title_box.click()
                title_box.clear()
                title_box.send_keys(title)
            
            print("🖋️ Filling Description...")
            desc_box = find_el([
                "//div[@role='textbox'][contains(@aria-placeholder, 'Pin')]",
                "//div[contains(@placeholder, 'Tell everyone')]",
                "//textarea[contains(@placeholder, 'Tell everyone')]"
            ])
            if desc_box:
                desc_box.click()
                desc_box.send_keys(description)
            else:
                print("⚠️ Fallback: Using TAB to try and hit description")
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.TAB)
                time.sleep(0.5)
                driver.switch_to.active_element.send_keys(description)

            print("🔗 Filling Link...")
            link_el = find_el([
                "//*[starts-with(@id, 'pin-draft-link-')]",
                "//input[@id='WebsiteField']",
                "//input[@type='url']"
            ])
            if link_el:
                link_el.click()
                link_el.clear()
                link_el.send_keys(link)
            else:
                print("⚠️ Fallback: Using TAB to try and hit link")
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.TAB)
                time.sleep(0.5)
                driver.switch_to.active_element.send_keys(link)

            # 2. Upload Image
            print("📤 Uploading image...")
            try:
                file_input = driver.find_element(By.XPATH, "//input[@type='file']")
                file_input.send_keys(str(image))
            except:
                print("⚠️ Could not find file input")
            
            print("\n👀 VERIFY NOW:")
            print(f"   Link: {link}")
            print("\nIf it looks good:")
            print("   1. Click PUBLISH in the browser")
            print("   2. Type 'y' here and press ENTER if it posted successfully")
            print("   3. Type 'n' if it failed or you want to skip")
            
            choice = input("Success? (y/n): ").lower()
            if 'y' in choice:
                posted.append(slug)
                state["posted"] = posted
                save_state(state)
                print(f"✅ Logged success for {slug}")
            else:
                print(f"⚠️ Skipped {slug}")
                
    finally:
        driver.quit()

if __name__ == "__main__":
    run_pair_pilot()
