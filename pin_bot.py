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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
BASE_DIR = Path(r'C:\Projects\the-index')
CSV_FILE = BASE_DIR / 'data.csv'
STATE_FILE = BASE_DIR / 'posted_state.json'
PIN_DIR = BASE_DIR / 'premium_pins'
PROFILE_DIR = BASE_DIR / 'chrome_profile_final'

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"posted": [], "remaining": []}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)

def dismiss_modals(driver):
    """Try to click 'close' or 'not now' on any overlays."""
    selectors = [
        "//button[contains(., 'Not now')]",
        "//button[contains(., 'Got it')]",
        "//div[@role='button'][contains(., 'Close')]",
        "//button[@aria-label='Close modal']"
    ]
    for sel in selectors:
        try:
            btns = driver.find_elements(By.XPATH, sel)
            for b in btns:
                if b.is_displayed():
                    b.click()
                    print(f" ✖️ Modal dismissed: {sel}")
        except:
            pass

def post_pin(driver, row):
    industry = row['industry'].strip()
    pain = row['pain_point'].strip()
    slug = row['slug'].strip()
    image_path = PIN_DIR / f"pin-{slug}.png"
    
    if not image_path.exists():
        print(f" ❌ Missing image: {image_path}")
        return False

    hashtag_industry = industry.replace(" ", "")
    hashtags = f" #CRM #{hashtag_industry} #Software #BusinessAutomation"
    title = f"Best CRM for {industry} ({time.strftime('%Y')})"
    if len(title) + len(f" #{hashtag_industry}") < 95:
        title += f" #{hashtag_industry}"
    description = f"Stop struggling with {pain}. We compared the top software solutions for {industry}. See the full review on THE INDEX.{hashtags}"
    link = f"https://crmindex.net/{slug}/"

    try:
        driver.get("https://www.pinterest.com/pin-builder/")
        wait = WebDriverWait(driver, 30)
        
        print(" ⏳ Waiting for page load...")
        time.sleep(12) 
        dismiss_modals(driver)

        # Helper for stable value setting
        def set_val_js(xpath, val):
            try:
                el = driver.find_element(By.XPATH, xpath)
                driver.execute_script("""
                    var el = arguments[0];
                    var val = arguments[1];
                    el.focus();
                    var setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value') || 
                                 Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value');
                    if (setter && setter.set) {
                        setter.set.call(el, val);
                    } else {
                        el.value = val;
                    }
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                """, el, val)
                return True
            except:
                return False

        # 1. Title
        print(" 🖋️ Title...")
        title_xpath = "//*[contains(@placeholder, 'title')] | //*[@data-test-id='pin-builder-draft-title']"
        if not set_val_js(title_xpath, title):
            t_box = wait.until(EC.element_to_be_clickable((By.XPATH, title_xpath)))
            t_box.send_keys(title)
        
        # 2. Description
        print(" 🖋️ Description...")
        desc_xpath = "//div[@role='textbox'] | //textarea[contains(@placeholder, 'Pin')] | //div[contains(@class, 'DraftEditor')]"
        try:
            d_box = driver.find_element(By.XPATH, desc_xpath)
            d_box.click()
            d_box.send_keys(description)
        except:
            set_val_js(desc_xpath, description)
            
        # 3. Destination Link (Dynamic ID)
        print(" 🔗 Link...")
        link_xpath = "//*[starts-with(@id, 'pin-draft-link-')] | //input[@type='url']"
        if not set_val_js(link_xpath, link):
            try:
                l_input = wait.until(EC.presence_of_element_located((By.XPATH, link_xpath)))
                l_input.send_keys(link)
            except:
                # If it's a button we need to click first
                btn_xpath = "//button[contains(., 'Add a destination link')]"
                try:
                    driver.find_element(By.XPATH, btn_xpath).click()
                    time.sleep(2)
                    set_val_js(link_xpath, link)
                except:
                    pass
            
        time.sleep(2)

        # 4. Upload Image
        print(" 📤 Image...")
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        file_input.send_keys(str(image_path))
        time.sleep(10)

        # 5. Select Board
        print(" 🖱️ Board...")
        try:
            board_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@data-test-id='board-dropdown-select-button'] | //button[contains(., 'Select')]")))
            driver.execute_script("arguments[0].click();", board_btn)
            time.sleep(2)
            first_board = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-test-id='board-row'] | //div[@role='listitem']")))
            first_board.click()
            print(" ✅ Board Selected")
        except:
            print(" ℹ️ Board skip")

        # 6. Final Publish
        print(" 🚀 Publishing...")
        publish_xpath = "//button[@data-test-id='board-dropdown-save-button'] | //button[contains(., 'Publish')]"
        publish_btn = wait.until(EC.element_to_be_clickable((By.XPATH, publish_xpath)))
        driver.execute_script("arguments[0].click();", publish_btn)
        print(" ✅ Published!")
        time.sleep(15)
        return True

    except Exception as e:
        print(f" ❌ Failed: {e}")
        driver.save_screenshot(str(BASE_DIR / f"error-{slug}.png"))
        return False

def main():
    state = load_state()
    posted_slugs = state.get("posted", [])
    
    # Load data
    all_data = []
    with CSV_FILE.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_data.append(row)
            
    # Find next items (limit 15 per day)
    to_post = [row for row in all_data if row['slug'] not in posted_slugs][:15]
    
    if not to_post:
        print(" 🎉 No pins left to post!")
        return

    print(f" 🏁 Starting batch of {len(to_post)} pins...")
    
    # Init Chrome
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={PROFILE_DIR}")
    chrome_options.add_argument("--profile-directory=Default")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        for row in to_post:
            slug = row['slug']
            print(f"\n⚡ Processing: {slug}")
            if post_pin(driver, row):
                if slug not in posted_slugs:
                    posted_slugs.append(slug)
                state["posted"] = posted_slugs
                # Remove from remaining if present
                if "remaining" in state and slug in state["remaining"]:
                    state["remaining"].remove(slug)
                save_state(state)
                print(f" ✅ Success: {slug}")
            else:
                print(f" 🛑 Error detected. Skipping and pausing.")
                time.sleep(5)
                
    finally:
        print(f"\n🏁 Batch finished! Total posted: {len(posted_slugs)}")
        driver.quit()

if __name__ == "__main__":
    main()
