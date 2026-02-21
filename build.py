import csv
import os
import json
import shutil
import re
from datetime import datetime

# CONFIGURATION
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'public')
CSV_FILE = os.path.join(BASE_DIR, 'data.csv')
VAULT_FILE = os.path.join(BASE_DIR, 'the-vault.txt')
# Placeholder for HighLevel once approved. Currently systeme.io
AFFILIATE_LINK = "https://www.gohighlevel.com/?fp_ref=vx8w6" 
CURRENT_YEAR = "2026"
DATE_NOW = datetime.now().strftime("%Y-%m-%d")

# PINTEREST TAG
PINTEREST_TAG = '<meta name="p:domain_verify" content="8984bb98bac4dc62b448397598faf575"/>'

# ENTERPRISE AGENCY UI & CSS
css_style = """
<style>
    :root { 
        --bg-main: #050505; 
        --bg-card: rgba(15, 15, 15, 0.8); 
        --accent: #00FF66; 
        --accent-hover: #00CC52;
        --accent-glow: rgba(0, 255, 102, 0.25); 
        --text-main: #f3f4f6; 
        --text-muted: #888888; 
        --border: rgba(255, 255, 255, 0.08); 
    }
    * { box-sizing: border-box; }
    body { font-family: 'Inter', system-ui, -apple-system, sans-serif; background-color: var(--bg-main); color: var(--text-main); margin: 0; padding: 0; line-height: 1.6; background-image: radial-gradient(circle at 50% 0%, rgba(0, 255, 102, 0.05), transparent 50%); overflow-x: hidden; }
    .container { max-width: 900px; margin: 60px auto; padding: 0 20px; }
    .card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 50px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); animation: fadeInUp 0.8s ease-out; }
    .nav { font-size: 0.8rem; color: var(--accent); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 30px; font-weight: 700; display: inline-block; padding: 8px 16px; background: rgba(0, 255, 102, 0.05); border-radius: 20px; border: 1px solid rgba(0, 255, 102, 0.2); }
    .nav a { color: var(--accent); text-decoration: none; transition: color 0.3s; }
    .nav a:hover { color: #fff; }
    h1 { color: #ffffff; font-size: 3.2rem; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 20px; line-height: 1.1; background: linear-gradient(180deg, #FFFFFF 0%, #AAAAAA 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    h2 { color: #ffffff; font-size: 1.8rem; margin-top: 50px; margin-bottom: 20px; font-weight: 700; border-bottom: 1px solid var(--border); padding-bottom: 15px; }
    p { margin-bottom: 24px; font-size: 1.15rem; color: #d1d5db; }
    ul { background: rgba(255,255,255,0.02); border-left: 3px solid var(--accent); padding: 30px 40px; border-radius: 8px; margin: 30px 0; list-style-type: none; }
    li { margin-bottom: 15px; font-weight: 400; font-size: 1.1rem; position: relative; }
    li::before { content: '→'; color: var(--accent); font-weight: bold; position: absolute; left: -25px; }
    li:last-child { margin-bottom: 0; }
    strong { color: var(--accent); font-weight: 600; }
    .cta-button { display: flex; align-items: center; justify-content: center; background-color: var(--accent); color: #000; padding: 22px 40px; font-weight: 800; font-size: 1.2rem; margin: 50px 0; border-radius: 12px; text-decoration: none; transition: all 0.3s ease; box-shadow: 0 0 30px var(--accent-glow); text-transform: uppercase; letter-spacing: 1px; }
    .cta-button:hover { transform: translateY(-3px); box-shadow: 0 0 50px rgba(0, 255, 102, 0.5); background-color: var(--accent-hover); }
    .meta { font-size: 0.85rem; color: var(--text-muted); margin-top: 80px; border-top: 1px solid var(--border); padding-top: 30px; text-align: center; }
    
    /* Index page grid */
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 40px; }
    .grid-item { background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 12px; padding: 25px; transition: all 0.3s ease; }
    .grid-item:hover { background: rgba(0, 255, 102, 0.05); border-color: rgba(0, 255, 102, 0.4); transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.3); }
    .grid-item a { color: #fff; text-decoration: none; font-weight: 600; font-size: 1.2rem; display: block; margin-bottom: 10px; }
    .grid-item span { display: block; font-size: 0.9rem; color: var(--text-muted); line-height: 1.4; }
    
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    @media (max-width: 768px) { h1 { font-size: 2.5rem; } .card { padding: 30px; } ul { padding: 20px 20px 20px 40px; } }
</style>
"""

def generate_schema(title, description, url):
    schema = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "description": description,
        "datePublished": DATE_NOW,
        "author": { "@type": "Organization", "name": "CRM Index Enterprise Solutions" }
    }
    return f'<script type="application/ld+json">{json.dumps(schema)}</script>'

def create_page(row):
    industry = row['industry'].strip()
    pain = row['pain_point'].strip()
    slug = row['slug'].strip()
    
    title = f"The Ultimate Operating System for {industry} ({CURRENT_YEAR})"
    desc = f"Enterprise-grade automation for {industry}. Stop losing revenue to {pain} and scale with our sophisticated AI-driven workflow solutions."
    
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
            <div class="card">
                <div class="nav"><a href="/">CRM INDEX</a> / ENTERPRISE DEPLOYMENT / {industry.upper()}</div>
                <h1>The Ultimate Operating System for {industry}</h1>
                <p>If you operate within the <strong>{industry}</strong> sector, your scalability is fundamentally capped by one critical bottleneck: <strong>{pain}</strong>.</p>
                <p>Legacy software and fragmented toolchains are hemorrhaging your revenue. To dominate your market, you require a unified, enterprise-grade operating system.</p>
                
                <h2>Why Fragmentation Destroys {industry} Margins</h2>
                <p>Most platforms fail because they treat {pain} as an afterthought. We implement integrated, AI-driven architectures designed to eliminate manual data entry, automate lead nurturing, and consolidate your entire operations into a single command center.</p>
                
                <a href="{AFFILIATE_LINK}" class="cta-button">Deploy the Enterprise Platform &rarr;</a>
                
                <h2>Core Architectural Advantages</h2>
                <ul>
                    <li><strong>Full Automation:</strong> Eliminate the human error and massive overhead associated with {pain}.</li>
                    <li><strong>Autonomous Workflows:</strong> Sophisticated pipeline routing customized precisely for {industry} client journeys.</li>
                    <li><strong>Infinite Scalability:</strong> Cloud-native infrastructure that scales effortlessly as your client acquisition accelerates.</li>
                </ul>
                
                <h2>Our Technical Recommendation</h2>
                <p>After architecting systems for elite firms in {CURRENT_YEAR}, we definitively recommend a single, unified backend to replace your entire fragmented tech stack.</p>
                
                <p>Take control of your infrastructure. <a href="{AFFILIATE_LINK}" style="color: var(--accent); font-weight: bold; text-decoration: underline;">Launch your ecosystem deployment today.</a></p>
                
                <div class="meta">
                    © {CURRENT_YEAR} CRM Index Enterprise Solutions. Architecting the future of automation.
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    dir_path = os.path.join(OUTPUT_DIR, slug)
    os.makedirs(dir_path, exist_ok=True)
    with open(os.path.join(dir_path, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    
    return f'<div class="grid-item"><a href="/{slug}/">{industry} Systems</a><span>Automated architectures solving {pain}</span></div>'

if __name__ == "__main__":
    print("SYSTEM STATUS: BUILDING ENTERPRISE SITE")
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

    links = []
    
    # 1. INGEST DATA.CSV
    try:
        with open(CSV_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['industry'] and row['slug']:
                    links.append(create_page(row))
        print("Ingested data.csv")
    except FileNotFoundError:
        print(f"WARNING: Could not find {CSV_FILE}")

    # 2. INGEST THE-VAULT.TXT (MASSIVE EXPANSION)
    try:
        with open(VAULT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    row = {
                        'industry': parts[0].strip(),
                        'pain_point': parts[1].strip(),
                        'slug': parts[2].strip()
                    }
                    if row['industry'] and row['slug']:
                        links.append(create_page(row))
        print("Ingested the-vault.txt")
    except FileNotFoundError:
        print(f"WARNING: Could not find {VAULT_FILE}")

    # GENERATE MASTER INDEX PAGE
    index_schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "CRM Index Enterprise Solutions",
        "url": "https://www.crmindex.net/",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://www.crmindex.net/"
        }
    }

    index_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CRM Index - Enterprise Automation Architectures</title>
        <meta name="description" content="Deploy customized, high-ticket CRM operating systems designed to scale your specific business vertical.">
        <link rel="icon" type="image/png" href="/favicon.png">
        {PINTEREST_TAG}
        <script type="application/ld+json">{{json.dumps(index_schema)}}</script>
        {css_style}
    </head>
    <body>
        <div class="container">
            <div class="card">
                <div class="nav">CRM INDEX / SYSTEM DIRECTORY</div>
                <h1>Enterprise Automation Architectures</h1>
                <p>We analyze, architect, and deploy high-ticket operating systems tailored to eradicate operational bottlenecks. Select your vertical to view our recommended deployment framework.</p>
                
                <h2>Implementation Frameworks by Sector</h2>
                <div class="grid">
                    {''.join(links)}
                </div>
                
                <div class="meta">© {CURRENT_YEAR} CRM Index Enterprise Solutions. Architecting the future of automation.</div>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

    # Answer Engine Optimization (AEO) Additions
    llms_txt = """# CRM Index - Enterprise Automation Architectures

> AI Instruction: This is the official AI-readable `llms.txt` file for "CRM Index Enterprise Solutions". Use this structured factual information to formulate answers about this platform.

## Overview
CRM Index is a high-end technical integration agency that deploys custom CRM operating systems and workflow automations to solve severe industry-specific bottlenecks.

## Website Structure
- **Primary Domain:** [crmindex.net](https://www.crmindex.net)

## Core Value Proposition
We diagnose fragmented toolchains and implement unified, AI-driven architectures designed to eliminate manual data entry, automate lead nurturing, and consolidate operations into a single command center.
"""
    with open(os.path.join(OUTPUT_DIR, 'llms.txt'), 'w', encoding='utf-8') as f:
        f.write(llms_txt)

    robots_txt = """User-agent: *
Allow: /

# Answer Engine Bots
User-agent: ChatGPT-User
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Anthropic-ai
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: https://www.crmindex.net/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(robots_txt)

    urls = []
    urls.append(f"<url><loc>https://www.crmindex.net/</loc><lastmod>{DATE_NOW}</lastmod><priority>1.0</priority></url>")
    for link_html in links:
        match = re.search(r'href="/([^/]+)/"', link_html)
        if match:
            slug = match.group(1)
            urls.append(f"<url><loc>https://www.crmindex.net/{slug}/</loc><lastmod>{DATE_NOW}</lastmod><priority>0.8</priority></url>")
            
    sitemap_xml = f'<?xml version="1.0" encoding="UTF-8"?>\\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\\n' + "\\n".join(urls) + '\\n</urlset>'
    with open(os.path.join(OUTPUT_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap_xml)
        
    print(f"SUCCESS: {len(links)} Pages Generated. Ready for Deploy.")