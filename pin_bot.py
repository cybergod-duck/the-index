import time
import json
import csv
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ⚡ CONFIGURATION ⚡
BASE_DIR = Path(r'C:\Projects\the-index')
CSV_FILE = BASE_DIR / 'data.csv'
STATE_FILE = BASE_DIR / 'posted_state.json'
PIN_DIR = BASE_DIR / 'premium_pins'
PROFILE_DIR = BASE_DIR / 'chrome_profile_final'  # Fresh profile to avoid ALL ghosts

def load_data():
    data = {}
    with CSV_FILE.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[row['slug']] = row
    return data

def load_state():
    if STATE_FILE.exists():
        with STATE_FILE.open('r') as f:
            return json.load(f)
    return {"posted": [], "remaining": []}

def save_state(state):
    with STATE_FILE.open('w') as f:
        json.dump(state, f, indent=4)

def setup_driver():
    print(f"🛠️ Initializing Chrome. Profile: {PROFILE_DIR}")
    chrome_options = Options()
    # 🛡️ Persistent Profile for Login Persistence
    chrome_options.add_argument(f"--user-data-dir={PROFILE_DIR}")
    chrome_options.add_argument("--profile-directory=Default")
    # Stealth
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # Hide automation footprint
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver

def dismiss_modals(driver, max_attempts=5):
    """Aggressively tries to dismiss various Pinterest popups."""
    # Try hitting escape first
    try:
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(1)
    except Exception:
        pass
    modal_selectors = [
        "//button[@aria-label='Close']",
        "//div[@role='dialog']//button",
        "//button[contains(., 'Next')]",
        "//button[contains(., 'Got it')]",
        "//button[contains(., 'Skip')]",
        "//button[contains(., 'Dismiss')]",
        "//button[contains(., 'Take Tour')]",
        "//div[contains(@class, 'modal')]//button",
        "//*[@aria-label='Close']"
    ]
    for attempt in range(max_attempts):
        found_any = False
        for selector in modal_selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                for el in elements:
                    if el.is_displayed():
                        print(f" 👋 Dismissing popup element ({attempt+1})...")
                        driver.execute_script("arguments[0].click();", el)
                        time.sleep(1.5)
                        found_any = True
            except Exception:
                pass
        if not found_any:
            break

def post_pin(driver, slug, row):
    print(f"\n⚡ Preparing Pin: {slug}")
    image_path = PIN_DIR / f"pin-{slug}.png"
    if not image_path.exists():
        print(f" ⚠️ Skipping: Image not found at {image_path}")
        return False
    industry = row['industry'].strip()
    pain = row['pain_point'].strip()
    # 🏷️ Optimized for Discoverability
    hashtag_industry = industry.replace(" ", "")
    hashtags = f" #CRM #{hashtag_industry} #Software #BusinessAutomation"
    title = f"Best CRM for {industry} ({time.strftime('%Y')})"
    if len(title) + len(f" #{hashtag_industry}") < 95:
        title += f" #{hashtag_industry}"
    description = f"Stop struggling with {pain}. We compared the top software solutions for {industry}. See the full review on THE INDEX.{hashtags}"
    link = f"https://crmindex.net/{slug}/"
    try:
        driver.get("https://www.pinterest.com/pin-builder/")
        wait = WebDriverWait(driver, 15)
        # 1. Dismiss Modals
        dismiss_modals(driver)
        # 2. Upload
        file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        file_input.send_keys(str(image_path))
        print(" ✅ Image Hooked")
        # Dismiss any modals that appeared AFTER upload
        dismiss_modals(driver)
        # 3. Text Content
        print(" 🖋️ Entering metadata...")
        # Title
        title_box = wait.until(EC.presence_of_element_located((By.XPATH,
            "//input[contains(@placeholder, 'Add your title')] | "
            "//textarea[contains(@placeholder, 'Add your title')] | "
            "//div[@role='textbox' and @aria-label='Title'] | "
            "//*[@data-test-id='pin-builder-draft-title'] |"
            "//h1[contains(@aria-label, 'Title')]//following-sibling::div//div[@role='textbox']"
        )))
        title_box.clear()
        title_box.send_keys(title)
        # Description
        desc_box = wait.until(EC.presence_of_element_located((By.XPATH,
            "//div[@role='textbox' and contains(., 'Tell everyone')] | "
            "//div[@role='textbox' and contains(@aria-placeholder, 'description')] | "
            "//div[@role='textbox' and contains(@aria-label, 'description')] | "
            "//textarea[contains(@placeholder, 'description')] | "
            "//div[contains(@aria-placeholder, 'description')] |"
            "//div[contains(@class, 'public-DraftEditor-content')] [not(contains(@aria-label, 'Title'))]"
        )))
        desc_box.send_keys(description)
        # Link
        print(" 🔗 Entering link (Surgical Mode)...")
        link_entered = False
        try:
            # 1. Broad search for anything matching 'link'
            triggers = [
                "//input[contains(@placeholder, 'link')]",
                "//*[text()='Add a destination link']",
                "//div[contains(@aria-placeholder, 'link')]",
                "//input[@id='link-input']"
            ]
            
            target = None
            for sel in triggers:
                els = driver.find_elements(By.XPATH, sel)
                if els and els[0].is_displayed():
                    target = els[0]
                    break
            
            if target:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", target)
                time.sleep(2) # Wait for it to turn into an input
                
                # Now find the actual input
                final_input = driver.execute_script("""
                    var active = document.activeElement;
                    if (active.tagName === 'INPUT' || active.tagName === 'TEXTAREA') return active;
                    
                    var inputs = document.querySelectorAll('input');
                    for (var inp of inputs) {
                        if (inp.placeholder && inp.placeholder.toLowerCase().includes('link')) return inp;
                        if (inp.value === '') return inp; // Often the link is the only empty input left
                    }
                    return null;
                """)
                
                if final_input:
                    driver.execute_script("""
                        function setNativeValue(element, value) {
                            const { set: valueSetter } = Object.getOwnPropertyDescriptor(element, 'value') || {};
                            const prototype = Object.getPrototypeOf(element);
                            const { set: prototypeValueSetter } = Object.getOwnPropertyDescriptor(prototype, 'value') || {};
                            if (prototypeValueSetter && prototypeValueSetter !== valueSetter) {
                                prototypeValueSetter.call(element, value);
                            } else if (valueSetter) {
                                valueSetter.call(element, value);
                            } else {
                                element.value = value;
                            }
                        }
                        setNativeValue(arguments[0], arguments[1]);
                        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                        arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
                    """, final_input, link)
                    print(" ✅ Link injected via Surgical JS")
                    link_entered = True
        except Exception as e:
            print(f" ⚠️ Surgical link failure: {e}")

        if not link_entered:
            print(" ⌨️ Final Tab Fallback...")
            try:
                desc_box.click()
                time.sleep(1)
                webdriver.ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(link).send_keys(Keys.ENTER).perform()
                time.sleep(1)
            except: pass

        print(" ✅ Metadata Entry Phase Complete")

        # 4. Board Selection
        print(" 🖱️ Selecting board...")
        try:
            board_btn = None
            board_selectors = [
                "//*[@data-test-id='board-dropdown-select-button']",
                "//button[contains(., 'Business')]",
                "//button[contains(., 'Select board')]",
                "//button[contains(@aria-label, 'board')]"
            ]
            for sel in board_selectors:
                els = driver.find_elements(By.XPATH, sel)
                if els and els[0].is_displayed():
                    board_btn = els[0]
                    break
            
            if board_btn:
                driver.execute_script("arguments[0].click();", board_btn)
                time.sleep(2)
                first = wait.until(EC.element_to_be_clickable((By.XPATH, 
                    "//div[@data-test-id='board-row'] | //div[@role='listitem'] | //div[contains(@class, 'boardRow')]"
                )))
                first.click()
                print(" ✅ Board Selected")
        except Exception as e:
            print(f" ℹ️ Board selection skip: {e}")

        # 5. Final Publish
        print(" ⏳ Finalizing for Publish...")
        time.sleep(5)
        
        publish_btn = None
        publish_selectors = [
            "//button[contains(normalize-space(), 'Publish')]",
            "//div[text()='Publish']/parent::button",
            "//button[@data-test-id='board-dropdown-save-button']",
            "//button[contains(@class, 'next')]", # Sometimes 'Next' in some views
            "//div[@role='button'][contains(., 'Publish')]"
        ]
        for sel in publish_selectors:
            els = driver.find_elements(By.XPATH, sel)
            if els and els[0].is_displayed():
                publish_btn = els[0]
                break
        
        if publish_btn:
            print(f" 🚀 Clicking Publish Button...")
            driver.execute_script("arguments[0].click();", publish_btn)
            print(" ✅ Publish Command Sent")
            time.sleep(12) 
            return True
        else:
            raise Exception("Publish button not found")
    except Exception as e:
        print(f" ❌ Flow Interrupted: {e}")
        try:
            error_img = BASE_DIR / f"error-{slug}.png"
            driver.save_screenshot(str(error_img))
            print(f" 📸 Screenshot saved to {error_img}")
        except Exception:
            pass
        return False

def main():
    state = load_state()
    data = load_data()
    if not state["remaining"]:
        state["remaining"] = list(data.keys())
        save_state(state)
    if not state["remaining"]:
        print("🎉 All caught up!")
        return
    driver = setup_driver()
    
    # 🔓 Automatic Login Detection
    print("🌐 Checking login status...")
    driver.get("https://www.pinterest.com/pin-builder/")
    time.sleep(8)
    
    if "login" in driver.current_url.lower():
        print("\n" + "="*60)
        print("� LOGIN REQUIRED: Please log in in the opened Chrome window.")
        print("   The profile will save your session for future automated runs.")
        print("="*60 + "\n")
        input("👉 Press [ENTER] here once you are logged in and seeing the Pin Builder page...")
    else:
        print("✅ Active session detected. Proceeding to batch...")

    batch = state["remaining"][:15]
    posted = []
    for slug in batch:
        if post_pin(driver, slug, data.get(slug)):
            posted.append(slug)
            print(f"--- Processed {len(posted)}/15 ---")
        else:
            print("🛑 Error detected. Pausing/Stopping.")
            break
        print("💤 Cooling down (30s)...")
        time.sleep(30)
    # Sync
    for s in posted:
        state["remaining"].remove(s)
        state["posted"].append(s)
    save_state(state)
    print(f"\n🏁 Finished! {len(posted)} pins posted. Total: {len(state['posted'])}")
    driver.quit()

if __name__ == "__main__":
    main()
