import os
import csv
import time
from html2image import Html2Image
from rich.console import Console

console = Console()
h2i = Html2Image(size=(1000, 1500))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'data.csv')
OUTPUT_DIR = os.path.join(BASE_DIR, 'premium_pins')

os.makedirs(OUTPUT_DIR, exist_ok=True)

# THE ENTERPRISE PIN TEMPLATE
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <!-- Load Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0A0A0A;
            --card-bg: rgba(20, 20, 20, 0.7);
            --neon-green: #00FF66;
            --text-main: #FFFFFF;
            --text-muted: #A0A0A0;
            --border-color: rgba(255, 255, 255, 0.1);
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
        }}

        body {{
            width: 1000px;
            height: 1500px;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(0, 255, 102, 0.08), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(0, 255, 102, 0.05), transparent 25%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 80px;
            color: var(--text-main);
            position: relative;
            overflow: hidden;
        }}

        /* Subtle grid background */
        body::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: 
                linear-gradient(var(--border-color) 1px, transparent 1px),
                linear-gradient(90deg, var(--border-color) 1px, transparent 1px);
            background-size: 50px 50px;
            opacity: 0.2;
            z-index: 1;
        }}

        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 40px;
            width: 100%;
            height: 100%;
            padding: 100px 80px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            position: relative;
            z-index: 2;
            box-shadow: 0 30px 60px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1);
            backdrop-filter: blur(20px);
        }}

        .glow-orb {{
            position: absolute;
            width: 400px;
            height: 400px;
            background: var(--neon-green);
            filter: blur(150px);
            opacity: 0.15;
            top: -100px;
            right: -100px;
            border-radius: 50%;
            z-index: -1;
        }}

        .eyebrow {{
            color: var(--neon-green);
            font-weight: 700;
            font-size: 32px;
            letter-spacing: 6px;
            text-transform: uppercase;
            margin-bottom: 40px;
        }}

        .headline {{
            font-size: 85px;
            font-weight: 900;
            line-height: 1.1;
            margin-bottom: 60px;
            max-width: 800px;
        }}

        .highlight {{
            color: var(--neon-green);
            text-shadow: 0 0 40px rgba(0, 255, 102, 0.4);
        }}

        .pain-point {{
            font-size: 38px;
            color: var(--text-muted);
            font-weight: 400;
            line-height: 1.4;
            max-width: 700px;
            margin-bottom: 80px;
        }}

        .brand {{
            margin-top: auto;
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        
        .brand-logo {{
            width: 50px;
            height: 50px;
            background: var(--neon-green);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 30px rgba(0, 255, 102, 0.4);
        }}

        .brand-logo::after {{
            content: '';
            width: 20px;
            height: 20px;
            background: var(--bg-color);
            border-radius: 4px;
        }}

        .brand-text {{
            font-size: 36px;
            font-weight: 700;
            letter-spacing: 2px;
        }}

        .button-mock {{
            background: var(--neon-green);
            color: #000;
            padding: 30px 60px;
            border-radius: 20px;
            font-size: 36px;
            font-weight: 700;
            margin-top: 40px;
            box-shadow: 0 10px 30px rgba(0, 255, 102, 0.3);
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="glow-orb"></div>
        <div class="eyebrow">Enterprise Automation</div>
        <div class="headline">The Ultimate Lead System for <span class="highlight">{industry}</span></div>
        <div class="pain-point">Stop struggling with {pain_point}. Automate your entire workflow.</div>
        <div class="button-mock">See Architecture</div>
        <div class="brand">
            <div class="brand-logo"></div>
            <div class="brand-text">CRM INDEX</div>
        </div>
    </div>
</body>
</html>
"""

def generate_batch(batch_size=100):
    all_rows = []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_rows.append(row)
            
    # Find ones we haven't rendered yet
    to_render = []
    for row in all_rows:
        img_path = os.path.join(OUTPUT_DIR, f"pin-{row['slug']}.png")
        if not os.path.exists(img_path):
            to_render.append(row)
            
    to_render = to_render[:batch_size]
    
    if not to_render:
        console.print("[bold green]All pins have been generated![/bold green]")
        return
        
    console.print(f"[bold cyan]Rendering {len(to_render)} new Enterprise Pins...[/bold cyan]")
    
    for row in to_render:
        industry = row['industry'].upper()
        pain = row['pain_point']
        slug = row['slug']
        
        html_content = HTML_TEMPLATE.format(
            industry=industry,
            pain_point=pain
        )
        
        html_file = os.path.join(BASE_DIR, f"temp_{slug}.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        output_filename = f"pin-{slug}.png"
        
        try:
            h2i.screenshot(
                html_file=html_file,
                save_as=output_filename
            )
            # html2image saves to current working dir, so we move it to premium_pins
            if os.path.exists(output_filename):
                os.replace(output_filename, os.path.join(OUTPUT_DIR, output_filename))
            console.print(f"[green]✓ Generated: {output_filename}[/green]")
        except Exception as e:
            console.print(f"[red]Error rendering {slug}: {e}[/red]")
        finally:
            if os.path.exists(html_file):
                os.remove(html_file)
                
    console.print(f"[bold green]Batch complete! Generated {len(to_render)} pins.[/bold green]")

if __name__ == "__main__":
    console.print("[bold yellow]Starting Enterprise Pin Generator[/bold yellow]")
    generate_batch(100)
