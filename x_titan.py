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
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()

# --- CONFIG ---
BASE_DIR = Path(r'C:\Projects\the-index')
CSV_FILE = BASE_DIR / 'data.csv'
STATE_FILE = BASE_DIR / 'x_state.json'
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

def post_to_x(driver, row, progress, task_id):
    slug = row['slug']
    industry = row['industry'].strip()
    pain = row['pain_point'].strip()
    link = f"https://crmindex.net/{slug}/"
    
    # Professional B2B SEO-optimized Tweet
    tweet_text = f"If you run a business in {industry}, {pain} is the #1 bottleneck to scaling.\n\nWe just published the definitive architecture on how to automate your entire workflow using GoHighLevel.\n\nRead the full system breakdown here:\n{link}\n\n#CRM #BusinessAutomation #{industry.replace(' ', '')}"
    
    try:
        progress.update(task_id, description=f"[bold yellow]Loading X:[/] {slug}")
        driver.get("https://x.com/compose/tweet")
        wait = WebDriverWait(driver, 15)
        
        # Check if we are logged in - if the login page appears instead of compose, bail out
        time.sleep(5)
        if "login" in driver.current_url or "i/flow/login" in driver.current_url:
            console.print("\n[bold red]NOT LOGGED INTO X![/bold red]")
            console.print("[yellow]Please run Chrome manually on the `chrome_profile_final` profile, go to x.com, and log in. Then restart this bot.[/yellow]")
            return "LOGGED_OUT"

        # 1. Type Tweet
        progress.update(task_id, description=f"[bold blue]Drafting Tweet:[/] {slug}")
        tweet_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tweetTextarea_0']")))
        tweet_box.click()
        
        # Paste text using JS to avoid rendering issues with emojis or weird characters
        driver.execute_script("""
            const text = arguments[0];
            const dataTransfer = new DataTransfer();
            dataTransfer.setData('text', text);
            const event = new ClipboardEvent('paste', {
                clipboardData: dataTransfer,
                bubbles: true
            });
            arguments[1].dispatchEvent(event);
        """, tweet_text, tweet_box)
        
        # Fallback if JS paste fails
        if len(tweet_box.text) < 5:
            tweet_box.send_keys(tweet_text)
            
        time.sleep(4)
        
        # 2. Add some space at the end to ensure the link card generates
        tweet_box.send_keys(" ")
        time.sleep(5) # Wait for Twitter to fetch the link preview from crmindex.net
        
        # 3. Post Tweet
        progress.update(task_id, description=f"[bold magenta]Posting:[/] {slug}")
        if not aggressive_click(driver, ["//div[@data-testid='tweetButton']"]):
            raise Exception("Could not click Tweet button")
            
        time.sleep(5)
        return True

    except Exception as e:
        console.print(f"[red]Error on {slug}: {e}[/red]")
        driver.save_screenshot(str(BASE_DIR / f"fail-x-{slug}.png"))
        return False

def main():
    console.clear()
    console.print(Panel.fit("[bold blue]X (TWITTER) TITAN - SEO SYNDICATION[/bold blue]\n[green]Status: READY[/green]", border_style="bold blue"))
    
    state = load_state()
    posted = state.get("posted", [])
    
    all_data = []
    with CSV_FILE.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader: all_data.append(row)
            
    # X limits: Safely post ~10-15 per day to avoid shadowbans on a new account
    to_post = [row for row in all_data if row['slug'] not in posted][:12]
    
    if not to_post:
        console.print("[bold green]🏁 ALL URLS SYNDICATED TO X! EXITING...[/bold green]")
        return

    options = Options()
    options.add_argument(f"--user-data-dir={PROFILE_DIR}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--window-size=1920,1080")
    
    # Run in the background headless (uncomment below if you want to hide it)
    # options.add_argument("--headless=new")
    
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
                result = post_to_x(driver, row, progress, overall_task)
                
                if result == "LOGGED_OUT":
                    break
                elif result == True:
                    posted.append(slug)
                    state["posted"] = posted
                    save_state(state)
                    progress.advance(overall_task)
                    console.print(f" [bold green]✨ SUCCESS (X):[/] {slug}")
                    time.sleep(20) # Wait between posts
                else:
                    console.print(f" [bold red]❌ FAILED:[/] {slug}")
                    
        finally:
            driver.quit()

if __name__ == "__main__":
    main()
