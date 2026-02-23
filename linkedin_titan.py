import time
import csv
import json
import os
from pathlib import Path
from social_templates import generate_natural_post
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()

# --- CONFIG ---
BASE_DIR = Path(r'C:\Projects\the-index')
CSV_FILE = BASE_DIR / 'data.csv'
STATE_FILE = BASE_DIR / 'linkedin_state.json'
PROFILE_DIR = BASE_DIR / 'chrome_profile_final'

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"posted": []}

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

def post_to_linkedin(driver, row, progress, task_id):
    slug = row['slug']
    industry = row['industry'].strip()
    pain = row['pain_point'].strip()
    link = f"https://crmindex.net/{slug}/"
    
    # Pull from our dynamic conversational pool
    post_text = generate_natural_post(industry, pain, link)
    post_text += f"\n\n#CRM #BusinessAutomation #{industry.replace(' ', '')} #LeadGeneration #B2BSales"
    
    try:
        progress.update(task_id, description=f"[bold yellow]Loading LinkedIn:[/] {slug}")
        driver.get("https://www.linkedin.com/feed/")
        wait = WebDriverWait(driver, 15)
        
        # Check login state
        time.sleep(5)
        if "login" in driver.current_url or "signup" in driver.current_url:
            console.print("\n[bold red]NOT LOGGED INTO LINKEDIN![/bold red]")
            console.print("[yellow]Please run Chrome manually on the `chrome_profile_final` profile, go to linkedin.com, and log in. Then restart this bot.[/yellow]")
            return "LOGGED_OUT"

        # 1. Click "Start a post"
        progress.update(task_id, description=f"[bold blue]Opening Composer:[/] {slug}")
        if not aggressive_click(driver, [
            "//button[contains(., 'Start a post')]", 
            "//span[contains(., 'Start a post')]/parent::button"
        ]):
            raise Exception("Could not click 'Start a post' button")
            
        time.sleep(3)

        # 2. Type Post
        progress.update(task_id, description=f"[bold blue]Drafting Post:[/] {slug}")
        editor = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='textbox'] | //div[contains(@class, 'ql-editor')]")))
        
        # Click into editor
        driver.execute_script("arguments[0].click();", editor)
        time.sleep(1)
        
        # Paste text using JS
        driver.execute_script("""
            const text = arguments[0];
            const dataTransfer = new DataTransfer();
            dataTransfer.setData('text', text);
            const event = new ClipboardEvent('paste', {
                clipboardData: dataTransfer,
                bubbles: true
            });
            arguments[1].dispatchEvent(event);
        """, post_text, editor)
        
        # Fallback if paste fails
        if len(editor.text) < 5:
            editor.send_keys(post_text)
            
        # 3. Wait for Link Preview Generation
        editor.send_keys(" ")
        progress.update(task_id, description=f"[bold cyan]Awaiting Preview:[/] {slug}")
        time.sleep(6) # LinkedIn takes a few seconds to scrape the meta image
        
        # 4. Publish Post
        progress.update(task_id, description=f"[bold magenta]Publishing:[/] {slug}")
        if not aggressive_click(driver, [
            "//button[contains(@class, 'share-actions__primary-action')]", 
            "//button[contains(., 'Post')]"
        ]):
            raise Exception("Could not click Publish button")
            
        time.sleep(8)
        return True

    except Exception as e:
        console.print(f"[red]Error on {slug}: {e}[/red]")
        driver.save_screenshot(str(BASE_DIR / f"fail-li-{slug}.png"))
        return False

def main():
    console.clear()
    console.print(Panel.fit("[bold blue]LINKEDIN TITAN - B2B SEO SYNDICATION[/bold blue]\n[green]Status: READY[/green]", border_style="bold blue"))
    
    state = load_state()
    posted = state.get("posted", [])
    
    all_data = []
    with CSV_FILE.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader: all_data.append(row)
            
    # Safely post 1 per execution. You can schedule this to run via Windows Task Scheduler every few hours.
    to_post = [row for row in all_data if row['slug'] not in posted][:1]
    
    if not to_post:
        console.print("[bold green]🏁 ALL URLS SYNDICATED TO LINKEDIN! EXITING...[/bold green]")
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
                result = post_to_linkedin(driver, row, progress, overall_task)
                
                if result == "LOGGED_OUT":
                    break
                elif result == True:
                    posted.append(slug)
                    state["posted"] = posted
                    save_state(state)
                    progress.advance(overall_task)
                    console.print(f" [bold green]✨ SUCCESS (LinkedIn):[/] {slug}")
                    time.sleep(30) # Wait between posts
                else:
                    console.print(f" [bold red]❌ FAILED:[/] {slug}")
                    
        finally:
            driver.quit()

if __name__ == "__main__":
    main()
