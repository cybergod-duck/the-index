#!/usr/bin/env python3
"""
ULTRA SIMPLE BOT - Uses keyboard navigation instead of selectors
"""
import time
import csv
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

BASE_DIR = Path(r'C:\Projects\the-index')
PROFILE_DIR = BASE_DIR / 'chrome_profile_final'

# Setup
chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={PROFILE_DIR}")
chrome_options.add_argument("--profile-directory=Default")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Data
slug = 'best-crm-accountants'
title = "Best CRM for Accountants (2026) #Accountants"
description = "Stop struggling with tracking time spent on tasks and client financial reporting. We compared the top software solutions for Accountants. See the full review on THE INDEX. #CRM #Accountants #Software #BusinessAutomation"
link = "https://crmindex.net/best-crm-accountants/"
image = BASE_DIR / 'premium_pins' / f'pin-{slug}.png'

print("🚀 ULTRA SIMPLE BOT")
print("="*60)

driver.get("https://www.pinterest.com/pin-builder/")
print("⏳ Waiting 15 seconds for page to load...")
time.sleep(15)

print("📝 Filling fields with TAB navigation...")

# Click anywhere on the page to focus
driver.find_element(By.TAG_NAME, "body").click()
time.sleep(2)

# TAB to title
for _ in range(3):  # May need a few TABs to get to title
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.TAB)
    time.sleep(0.5)

driver.switch_to.active_element.send_keys(title)
print(f"   ✅ Title: {title[:50]}...")
time.sleep(2)

# TAB to description
driver.find_element(By.TAG_NAME, "body").send_keys(Keys.TAB)
time.sleep(1)
driver.switch_to.active_element.send_keys(description)
print(f"   ✅ Description: {description[:50]}...")
time.sleep(2)

# TAB to link
driver.find_element(By.TAG_NAME, "body").send_keys(Keys.TAB)
time.sleep(1)
driver.switch_to.active_element.send_keys(link)
print(f"   ✅ Link: {link}")
time.sleep(2)

# Upload image
print("📤 Uploading image...")
file_input = driver.find_element(By.XPATH, "//input[@type='file']")
file_input.send_keys(str(image))
print("   ✅ Image uploaded")
time.sleep(8)  # Wait longer for image to process

# Click Publish
print("🔴 Clicking Publish...")
publish_selectors = [
    "//button[text()='Publish']",
    "//button[contains(text(), 'Publish')]",
    "//button[@data-test-id='board-dropdown-save-button']",
    "//div[contains(text(), 'Publish')]//ancestor::button"
]

published = False
for selector in publish_selectors:
    try:
        publish_button = driver.find_element(By.XPATH, selector)
        if publish_button.is_displayed():
            publish_button.click()
            print("   ✅ Published!")
            published = True
            break
    except:
        continue

if not published:
    print("   ⚠️ Could not find Publish button - check manually")

time.sleep(3)

print("\n✅ PIN POSTED! Check your Pinterest profile.")
print("Press ENTER to close browser...")
input()

driver.quit()
