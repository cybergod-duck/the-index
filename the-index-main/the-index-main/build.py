import csv
import os
import json
import shutil
from datetime import datetime

# CONFIGURATION
# Get the absolute path of the folder where this script lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'public')
CSV_FILE = os.path.join(BASE_DIR, 'data.csv')
AFFILIATE_LINK = "/go/partner" 
CURRENT_YEAR = "2026"
DATE_NOW = datetime.now().strftime("%Y-%m-%d")

# PINTEREST TAG
PINTEREST_TAG = '<meta name="p:domain_verify" content="8984bb98bac4dc62b448397598faf575"/>'

# VISUAL STYLING
css_style = """
<style>
    :root { --primary: #2563eb; --dark: #1f2937; --light: #f3f4f6; --white: #ffffff; --text: #4b5563; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: var(--light); color: var(--text); margin: 0; padding: 0; line-height: 1.6; }
    .container { max-width: 800px; margin: 40px auto; background: var(--white); padding: 40px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    .nav { font-size: 0.85rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px; border-bottom: 1px solid #e5e7eb; padding-bottom: 20px; }
    .nav a { color: #6b7280; text-decoration: none; font-weight: 600; }
    h1 { color: var(--dark); font-size: 2.25rem; letter-spacing: -0.025em; margin-bottom: 10px; }
    h2 { color: var(--dark); font-size: 1.5rem; margin-top: 40px; font-weight: 700; }
    p { margin-bottom: 20px; font-size: 1.1rem; }
    ul { background: #eff6ff; border-left: 4px solid var(--primary); padding: 20px 40px; border-radius: 4px; color: var(--dark); }
    li { margin-bottom: 10px; font-weight: 500; }
    .cta-button { display: block; text-align: center; background-color: var(--primary); color: white; padding: 20px; font-weight: 600; font-size: 1.2rem; margin: 40px 0; border-radius: 8px; text-decoration: none; transition: background 0.2s; box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2); }
    .cta-button:hover { background-color: #1d4ed8; color: white; transform: translateY(-1px); }
    .meta { font-size: 0.8rem; color: #9ca3af; margin-top: 60px; border-top: 1px solid #e5e7eb; padding-top: 20px; text-align: center; }
</style>
"""

def generate_schema(title, description, url):
    schema = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "description": description,
        "datePublished": DATE_NOW,
        "author": { "@type": "Organization", "name": "CRM Index" }
    }
    return f'<script type="application/ld+json">{json.dumps(schema)}</script>'

def create_page(row):
    industry = row['industry'].strip()
    pain = row['pain_point'].strip()
    slug = row['slug'].strip()
    
    title = f"Best CRM for {industry} ({CURRENT_YEAR} Review)"
    desc = f"Stop struggling with {pain}. We compare the top software solutions for {industry}."
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <meta name="description" content="{desc}">
        <link rel="icon" type="image/png" href="/favicon.png">
        {PINTEREST_TAG}
        {generate_schema(title, desc, slug)}
        {css_style}
    </head>
    <body>
        <div class="container">
            <div class="nav"><a href="/">CRM INDEX</a> / SOFTWARE / {industry.upper()}</div>
            <h1>Best CRM for {industry}</h1>
            <p>If you are running a business in <strong>{industry}</strong>, your efficiency is likely being drained by one major issue: <strong>{pain}</strong>.</p>
            <p>Spreadsheets and manual tracking are no longer sufficient. To scale, you need a dedicated operating system.</p>
            <h2>Why Generic Software Fails {industry}</h2>
            <p>Most "one-size-fits-all" tools are too rigid. They don't account for the specific workflow nuances of {pain}. You need a platform that is flexible enough to adapt to your reality.</p>
            <a href="{AFFILIATE_LINK}" class="cta-button">View Top Recommended Software &rarr;</a>
            <h2>Key Features You Need</h2>
            <ul>
                <li><strong>Automation:</strong> Eliminate the manual work of {pain}.</li>
                <li><strong>Customization:</strong> Tailor the dashboard to {industry} workflows.</li>
                <li><strong>Scalability:</strong> A tool that grows as you acquire more clients.</li>
            </ul>
            <h2>Our Recommendation</h2>
            <p>After reviewing the market landscape for {CURRENT_YEAR}, we have identified one platform that stands out for its versatility and ease of use.</p>
            <p><a href="{AFFILIATE_LINK}" style="color: var(--primary); font-weight: bold;">Click here to try the software for free.</a></p>
            <div class="meta">
                © {CURRENT_YEAR} CRM Index. All Rights Reserved. | <a href="/privacy" style="color: #9ca3af;">Privacy</a>
            </div>
        </div>
    </body>
    </html>
    """
    
    dir_path = os.path.join(OUTPUT_DIR, slug)
    os.makedirs(dir_path, exist_ok=True)
    with open(os.path.join(dir_path, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    
    return f'<li><a href="/{slug}/">{industry} Software</a></li>'

if __name__ == "__main__":
    print("SYSTEM STATUS: BUILDING SITE (NO EMOJI MODE)")
    print(f"Working in: {BASE_DIR}")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # SEARCH FOR FAVICON
    icon_source = None
    possible_names = ['favicon.png', 'favicon.png.png']
    
    for name in possible_names:
        candidate = os.path.join(BASE_DIR, name)
        if os.path.exists(candidate):
            icon_source = candidate
            print(f"FOUND FAVICON: {name}")
            break
            
    if icon_source:
        shutil.copy(icon_source, os.path.join(OUTPUT_DIR, 'favicon.png'))
        print("Favicon injected successfully.")
    else:
        print("WARNING: Still cannot find favicon.png. Check folder content.")

    links = []
    try:
        with open(CSV_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['industry']:
                    links.append(create_page(row))
    except FileNotFoundError:
        print(f"ERROR: Could not find {CSV_FILE} at {CSV_FILE}")
        exit()

    index_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CRM Index - The Best Software for Every Industry</title>
        <link rel="icon" type="image/png" href="/favicon.png">
        {PINTEREST_TAG}
        {css_style}
    </head>
    <body>
        <div class="container">
            <div class="nav">CRM INDEX / DIRECTORY</div>
            <h1>Industry Software Index</h1>
            <p>Find the perfect operating system for your specific business model. Select your industry below.</p>
            <h2>Browse by Sector</h2>
            <ul>{''.join(links)}</ul>
            <div class="meta">© {CURRENT_YEAR} CRM Index.</div>
        </div>
    </body>
    </html>
    """
    
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
        
    print(f"SUCCESS: {len(links)} Pages Generated. Ready for Deploy.")