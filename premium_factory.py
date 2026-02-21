import csv
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ⚡ CONFIGURATION ⚡
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'data.csv')
OUTPUT_DIR = os.path.join(BASE_DIR, 'premium_pins')
FAVICON_PATH = os.path.join(BASE_DIR, 'favicon.png')

# DESIGN SETTINGS
WIDTH = 1000
HEIGHT = 1500
PRIMARY_COLOR = "#2563eb"  # Royal Blue
SECONDARY_COLOR = "#1e4bb5"
WHITE = "#ffffff"
GRAY_TEXT = "#e0e7ff"

FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REGULAR = r"C:\Windows\Fonts\segoeui.ttf"

def create_gradient(width, height, color1, color2):
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def draw_glassmorphism_card(draw, x, y, w, h, radius=20):
    # Simulated glassmorphism: a semi-transparent white box with a light border
    # Note: True blurring is expensive/complex in basic PIL without sub-rendering,
    # so we'll use a semi-transparent layer.
    
    # Draw card background (semi-transparent white)
    overlay = Image.new('RGBA', (w, h), (255, 255, 255, 30))
    return overlay

def create_pin(row):
    industry = row['industry'].strip().upper()
    pain = row['pain_point'].strip()
    slug = row['slug'].strip()

    # 1. Create Canvas with Gradient
    img = create_gradient(WIDTH, HEIGHT, "#1e3a8a", "#1e40af") # Deep blue to slightly lighter blue
    
    # Add some abstract shapes for "Aura"
    draw = ImageDraw.Draw(img, 'RGBA')
    draw.ellipse([WIDTH*0.6, -200, WIDTH*1.2, 400], fill=(37, 99, 235, 100))
    draw.ellipse([-200, HEIGHT*0.7, 400, HEIGHT+200], fill=(37, 99, 235, 80))

    # 2. Load Fonts
    try:
        font_headline = ImageFont.truetype(FONT_BOLD, 90)
        font_sub = ImageFont.truetype(FONT_REGULAR, 45)
        font_body = ImageFont.truetype(FONT_REGULAR, 55)
        font_button = ImageFont.truetype(FONT_BOLD, 50)
        font_logo = ImageFont.truetype(FONT_BOLD, 40)
    except IOError:
        font_headline = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_button = ImageFont.load_default()
        font_logo = ImageFont.load_default()

    # 3. Draw LOGO
    if os.path.exists(FAVICON_PATH):
        logo = Image.open(FAVICON_PATH).convert("RGBA")
        logo = logo.resize((80, 80))
        img.paste(logo, (WIDTH // 2 - 140, 100), logo)
    
    draw.text((WIDTH // 2 - 40, 115), "CRM INDEX", font=font_logo, fill=WHITE)

    # 4. Draw Headline Info
    top_text = "BEST SOFTWARE FOR"
    bbox = draw.textbbox((0, 0), top_text, font=font_sub)
    draw.text(((WIDTH - (bbox[2]-bbox[0])) / 2, 250), top_text, font=font_sub, fill=GRAY_TEXT)

    # 5. Draw INDUSTRY (Big & Premium)
    wrapped_industry = textwrap.wrap(industry, width=14)
    y_text = 350
    for line in wrapped_industry:
        bbox = draw.textbbox((0, 0), line, font=font_headline)
        draw.text(((WIDTH - (bbox[2]-bbox[0])) / 2, y_text), line, font=font_headline, fill=WHITE)
        y_text += 110

    # 6. Glassmorphism-style card for Pain Point
    card_w, card_h = 850, 280
    card_x, card_y = (WIDTH - card_w) // 2, 800
    
    # Draw subtle background for card
    card_overlay = Image.new('RGBA', (card_w, card_h), (255, 255, 255, 20))
    img.paste(card_overlay, (card_x, card_y), card_overlay)
    
    # Draw card border
    draw.rectangle([card_x, card_y, card_x + card_w, card_y + card_h], outline=(255, 255, 255, 80), width=2)

    pain_text = f"Stop struggling with {pain}"
    wrapped_pain = textwrap.wrap(pain_text, width=32)
    y_pain = card_y + 60
    for line in wrapped_pain:
        bbox = draw.textbbox((0, 0), line, font=font_body)
        draw.text(((WIDTH - (bbox[2]-bbox[0])) / 2, y_pain), line, font=font_body, fill=WHITE)
        y_pain += 70

    # 7. Draw CTA Button
    btn_w, btn_h = 450, 120
    btn_x, btn_y = (WIDTH - btn_w) // 2, 1200
    
    # Button Shadow
    draw.rectangle([btn_x+5, btn_y+5, btn_x + btn_w+5, btn_y + btn_h+5], fill=(0, 0, 0, 80))
    # Button Body
    draw.rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], fill=WHITE)
    
    btn_text = "READ REVIEW"
    bbox = draw.textbbox((0, 0), btn_text, font=font_button)
    draw.text(((WIDTH - (bbox[2]-bbox[0])) / 2, btn_y + (btn_h - (bbox[3]-bbox[1])) / 2 - 5), 
              btn_text, font=font_button, fill=PRIMARY_COLOR)

    # 8. Save
    filename = f"pin-{slug}.png"
    img.save(os.path.join(OUTPUT_DIR, filename))
    print(f"💎 Premium Pin Generated: {filename}")

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print("--- STARTING PREMIUM FORGE ---")
    print("Generating ALL pin images...")
    
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            if row['industry']:
                create_pin(row)
                count += 1
                if count % 50 == 0:
                    print(f"Progress: {count} pins generated...")
                    
    print(f"--- COMPLETE. {count} PREMIUM PINS SAVED IN {OUTPUT_DIR} ---")
