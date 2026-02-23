import time
import csv
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Setup
BASE_DIR = Path(r'C:\Projects\the-index')
CSV_FILE = BASE_DIR / 'data.csv'
PIN_DIR = BASE_DIR / 'premium_pins'
PROFILE_DIR = BASE_DIR / 'chrome_profile_final'

# Load data
data = {}
with CSV_FILE.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data[row['slug']] = row

# Get first unpublished pin
slug = 'best-crm-accountants'
row = data[slug]
industry = row['industry'].strip()
pain = row['pain_point'].strip()
hashtag_industry = industry.replace(" ", "")
title = f"Best CRM for {industry} (2026) #{hashtag_industry}"
description = f"Stop struggling with {pain}. We compared the top software solutions for {industry}. See the full review on THE INDEX. #CRM #{hashtag_industry} #Software #BusinessAutomation"
link = f"https://crmindex.net/{slug}/"
image_path = PIN_DIR / f"pin-{slug}.png"

print(f"Title: {title}")
print(f"Link: {link}")
print(f"Image: {image_path}")

# Setup Chrome
chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={PROFILE_DIR}")
chrome_options.add_argument("--profile-directory=Default")
chrome_options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.pinterest.com/pin-builder/")
print("\n🔴 PAUSED - Browser is open on pin-builder page")
print("Press ENTER to continue with automated posting...")
input()

# Upload image
print("Uploading image...")
file_input = driver.find_element(By.XPATH, "//input[@type='file']")
file_input.send_keys(str(image_path))
time.sleep(5)

# Enter title
print("Entering title...")
title_box = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Add your title')]")
title_box.send_keys(title)
time.sleep(2)

# Enter description  
print("Entering description...")
desc_box = driver.find_element(By.XPATH, "//div[@role='textbox' and contains(., 'Tell everyone')]")
desc_box.send_keys(description)
time.sleep(2)

print("\n🔴 PAUSED - Metadata entered")
print("Now YOU manually click 'Add a destination link' and enter the URL:")
print(f"   {link}")
print("\nPress ENTER once you've added the link...")
input()

# Click publish
print("Clicking publish...")
publish_button = driver.find_element(By.XPATH, "//button[contains(., 'Publish')]")
publish_button.click()

print("\n✅ DONE! Press ENTER to close browser...")
input()
driver.quit()
