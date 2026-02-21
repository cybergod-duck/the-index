import time
import csv
import json
import os
import traceback
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from random import uniform
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

# --- UI SETUP ---
console = Console()

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

def aggressive_click(driver, selectors, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        for sel in selectors:
            try:
                btns = driver.find_elements(By.XPATH, sel)
                for b in btns:
                    if b.is_displayed() and b.is_enabled():
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", b)
                        time.sleep(0.5)
                        driver.execute_script("arguments[0].click();", b)
                        return True
            except: pass
        time.sleep(1)
    return False

def post_pin_flawless(driver, row, progress, task_id):
    slug = row['slug']
    industry = row['industry'].strip()
    pain = row['pain_point'].strip()
    title = f"Best CRM for {industry} (2026) #{industry.replace(' ', '')}"
    description = f"Stop struggling with {pain}. See the full review on THE INDEX. #CRM #Software #{industry.replace(' ', '')}"
    link = f"https://crmindex.net/{slug}/"
    image_path = PIN_DIR / f"pin-{slug}.png"
    
    if not image_path.exists(): 
        return False

    try:
        progress.update(task_id, description=f"[bold yellow]Navigating:[/] {slug}")
        driver.get("https://www.pinterest.com/pin-builder/")
        wait = WebDriverWait(driver, 20)
        time.sleep(7)

        # 1. UPLOAD IMAGE
        progress.update(task_id, description=f"[bold blue]Uploading:[/] {slug}")
        image_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        image_input.send_keys(os.path.abspath(str(image_path)))
        time.sleep(5)

        # 2. TITLE
        progress.update(task_id, description=f"[bold blue]Filling Title:[/] {slug}")
        t_el = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@id, 'pin-draft-title-')] | //textarea[contains(@placeholder, 'title')]")))
        t_el.click()
        t_el.send_keys(Keys.CONTROL + "a")
        t_el.send_keys(Keys.BACKSPACE)
        t_el.send_keys(title)
        time.sleep(1)

        # 3. DESCRIPTION
        progress.update(task_id, description=f"[bold blue]Filling Desc:[/] {slug}")
        d_xpath = "//div[@role='combobox'][contains(@aria-label, 'Pin')] | //div[contains(@placeholder, 'Tell someone')] | //div[@contenteditable='true']"
        d_el = wait.until(EC.presence_of_element_located((By.XPATH, d_xpath)))
        d_el.click()
        driver.execute_script("arguments[0].innerText = arguments[1];", d_el, description)
        d_el.send_keys(" ")
        time.sleep(2)

        # 4. URL
        progress.update(task_id, description=f"[bold blue]Filling URL:[/] {slug}")
        l_xpath = "//*[contains(@id, 'pin-draft-link-')] | //textarea[contains(@placeholder, 'link')]"
        l_el = wait.until(EC.element_to_be_clickable((By.XPATH, l_xpath)))
        l_el.click()
        l_el.send_keys(link)
        time.sleep(3)

        # 5. PUBLISH
        progress.update(task_id, description=f"[bold magenta]Publishing:[/] {slug}")
        pub_selectors = [
            "//button[@data-test-id='board-dropdown-save-button']",
            "//button[contains(., 'Publish')]",
            "//div[@role='button'][contains(., 'Publish')]",
            "//button[contains(., 'Save')]"
        ]
        if not aggressive_click(driver, pub_selectors, timeout=15):
            l_el.send_keys(Keys.TAB)
            time.sleep(1)
            driver.switch_to.active_element.send_keys(Keys.ENTER)
        
        # 6. SEE MY PIN
        time.sleep(8)
        aggressive_click(driver, [
            "//button[contains(., 'See your Pin')]",
            "//*[contains(text(), 'See your Pin')]",
            "//div[contains(@role, 'button')][contains(., 'See')]"
        ], timeout=10)

        # 7. SAVE
        time.sleep(5)
        if "/pin/" in driver.current_url:
            aggressive_click(driver, ["//button[contains(., 'Save')]", "//div[contains(@role, 'button')][contains(., 'Save')]"], timeout=5)

        # 8. BACK
        driver.get("https://www.pinterest.com/pin-builder/")
        time.sleep(5)
        
        return True

    except Exception as e:
        driver.save_screenshot(str(BASE_DIR / f"fail-{slug}.png"))
        return False

def main():
    console.clear()
    console.print(Panel.fit("[bold cyan]SOLO TITAN v4.0 - AESTHETIC MODE[/bold cyan]\n[green]Status: READY[/green]", border_style="bold blue"))
    
    state = load_state()
    posted = state.get("posted", [])
    all_data = []
    with CSV_FILE.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader: all_data.append(row)
            
    to_post = [row for row in all_data if row['slug'] not in posted][:30]
    
    if not to_post:
        console.print("[bold green]🏁 ALL PINS COMPLETE! EXITING...[/bold green]")
        return

    options = Options()
    options.add_argument(f"--user-data-dir={PROFILE_DIR}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        overall_task = progress.add_task("[bold green]Batch Progress[/]", total=len(to_post))
        
        try:
            for row in to_post:
                slug = row['slug']
                if post_pin_flawless(driver, row, progress, overall_task):
                    if slug not in posted: posted.append(slug)
                    state["posted"] = posted
                    save_state(state)
                    progress.advance(overall_task)
                    console.print(f" [bold green]✨ SUCCESS:[/] {slug}")
                else:
                    console.print(f" [bold red]❌ FAILED:[/] {slug}")
        finally:
            driver.quit()

if __name__ == "__main__":
    main()
