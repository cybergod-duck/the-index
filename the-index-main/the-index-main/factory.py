import csv
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

# ⚡ CONFIGURATION ⚡
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'data.csv')
OUTPUT_DIR = os.path.join(BASE_DIR, 'pins')

# DESIGN SETTINGS
WIDTH = 1000
HEIGHT = 1500
BG_COLOR = "#2563eb"  # Royal Blue
TEXT_COLOR = "#ffffff"
BUTTON_COLOR = "#ffffff"
BUTTON_TEXT_COLOR = "#2563eb"

def create_pin(row):
    industry = row['industry'].strip().upper()
    pain = row['pain_point'].strip()
    slug = row['slug'].strip()

    # 1. Create Canvas
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 2. Load Fonts (Using default Arial if available, otherwise default)
    try:
        font_headline = ImageFont.truetype("arial.ttf", 100)
        font_sub = ImageFont.truetype("arial.ttf", 60)
        font_body = ImageFont.truetype("arial.ttf", 50)
        font_button = ImageFont.truetype("arial.ttf", 50)
    except IOError:
        # Fallback for systems without arial in standard path
        font_headline = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_button = ImageFont.load_default()

    # 3. Draw TOP TEXT ("Best CRM Software")
    top_text = "BEST SOFTWARE FOR:"
    # Calculate text width to center it (using textbbox for newer Pillow versions)
    bbox = draw.textbbox((0, 0), top_text, font=font_sub)
    text_w = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_w) / 2, 200), top_text, font=font_sub, fill=TEXT_COLOR)

    # 4. Draw INDUSTRY (Big & Bold)
    # Wrap text if it's too long
    lines = textwrap.wrap(industry, width=12) # Break every 12 chars
    y_text = 400
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_headline)
        line_w = bbox[2] - bbox[0]
        draw.text(((WIDTH - line_w) / 2, y_text), line, font=font_headline, fill=TEXT_COLOR)
        y_text += 120 # Line height

    # 5. Draw PAIN POINT ("Stop struggling with...")
    pain_text = f"Stop struggling with\n{pain}"
    lines = textwrap.wrap(pain_text, width=30)
    y_text = 800
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_body)
        line_w = bbox[2] - bbox[0]
        draw.text(((WIDTH - line_w) / 2, y_text), line, font=font_body, fill="#e0e7ff")
        y_text += 70

    # 6. Draw BUTTON
    button_text = "READ REVIEW"
    btn_w = 400
    btn_h = 100
    btn_x = (WIDTH - btn_w) / 2
    btn_y = 1100
    
    # Draw button rectangle
    draw.rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], fill=BUTTON_COLOR)
    
    # Center button text
    bbox = draw.textbbox((0, 0), button_text, font=font_button)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    # Centering math
    text_x = btn_x + (btn_w - text_w) / 2
    text_y = btn_y + (btn_h - text_h) / 2 - 10 # slight adjustment
    draw.text((text_x, text_y), button_text, font=font_button, fill=BUTTON_TEXT_COLOR)

    # 7. Save
    filename = f"pin-{slug}.png"
    img.save(os.path.join(OUTPUT_DIR, filename))
    print(f"⚡ Generated: {filename}")

# ⚡ EXECUTION LOOP ⚡
if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print("--- STARTING PIXEL FORGE ---")
    
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['industry']:
                create_pin(row)
                
    print(f"--- COMPLETE. IMAGES SAVED IN {OUTPUT_DIR} ---")