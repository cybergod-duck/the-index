import csv
import json
import tweepy
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from social_templates import generate_natural_post

console = Console()
BASE_DIR = Path(r'C:\Projects\the-index')
CSV_FILE = BASE_DIR / 'data.csv'
STATE_FILE = BASE_DIR / 'x_api_state.json'

# --- OFFICIAL X API KEYS ---
# Loaded from local user desktop config at C:\Users\ovjup\Desktop\x_keys.txt
CONSUMER_KEY = "qQcINMldO0uaV0sGhoOngykx2"
CONSUMER_SECRET = "grfTv8lJg8OGV6PQA4roOMiFXOGRjwBH7I2bORoPbf7hyOdoL2"
ACCESS_TOKEN = "1591464000608501761-hyDf217DVhmDg3RK8i0zZBCXz9fah5"
ACCESS_SECRET = "pio8VuqNvczI65pyUzptqECHvOb2iJcqPBbxmOhrIZQmq"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAPjU7gEAAAAAmnMDVUhN4mHhJkNKCTn%2FrvOfaqo%3D0SaKeoG2OpIFOjkxgvCPOUlFLXZs1JQrg5OtcDtzE9adCJ5D33"

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"posted": []}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)

def main():
    console.clear()
    console.print(Panel.fit("[bold blue]X (TWITTER) OFFICIAL API TITAN[/bold blue]\n[green]Status: READY [API MODE ACTIVATED][/green]", border_style="bold blue"))
    
    state = load_state()
    posted = state.get("posted", [])
    
    all_data = []
    with CSV_FILE.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader: all_data.append(row)
            
    # Process only ONE post per run so the user can schedule this to run safely
    # (e.g. via Windows Task Scheduler every 2 hours) without spamming Twitter.
    to_post = [row for row in all_data if row['slug'] not in posted][:1]
    
    if not to_post:
        console.print("[bold green]🏁 ALL URLS SYNDICATED TO X! EXITING...[/bold green]")
        return
        
    try:
        # Initialize Tweepy V2 Client
        client = tweepy.Client(
            bearer_token=BEARER_TOKEN,
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_SECRET,
            wait_on_rate_limit=True
        )
    except Exception as e:
        console.print(f"[bold red]Failed to authenticate with X API:[/] {e}")
        return

    for row in to_post:
        slug = row['slug']
        industry = row['industry'].strip()
        pain = row['pain_point'].strip()
        link = f"https://crmindex.net/{slug}/"
        
        # Pull from our dynamic conversational pool
        tweet_text = generate_natural_post(industry, pain, link)
        console.print(f"\n[bold yellow]Drafting Tweet for {slug}...[/bold yellow]")
        console.print(f'[cyan]"{tweet_text}"[/cyan]\n')
        
        try:
            # Send the Tweet via official API (Extremely fast and 100% reliable)
            response = client.create_tweet(text=tweet_text)
            console.print(f"[bold green]✨ SUCCESS (X API):[/] Tweet published! ID: {response.data['id']}")
            
            # Record it as complete
            posted.append(slug)
            state["posted"] = posted
            save_state(state)
            
        except Exception as e:
            console.print(f" [bold red]❌ FAILED:[/] {e}")

if __name__ == "__main__":
    main()
