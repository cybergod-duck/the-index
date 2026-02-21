#!/usr/bin/env python3
"""
PAGE DUMP - Show ALL text on pin-builder page after 10 seconds
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir=C:\\Projects\\the-index\\chrome_profile_final")
chrome_options.add_argument("--profile-directory=Default")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.pinterest.com/pin-builder/")
print("Waiting 10 seconds for page to load...")
time.sleep(10)

print("\n" + "="*60)
print("ALL TEXT ON PAGE:")
print("="*60)

# Get all text from the page
all_text = driver.execute_script("return document.body.innerText;")
print(all_text)

print("\n" + "="*60)
print("ELEMENTS CONTAINING 'link' (case insensitive):")
print("="*60)

script = """
    const allElements = Array.from(document.querySelectorAll('*'));
    return allElements
        .filter(el => el.textContent && el.textContent.toLowerCase().includes('link'))
        .slice(0, 20)
        .map(el => ({
            tag: el.tagName,
            text: el.textContent.substring(0, 150),
            id: el.id,
            class: el.className
        }));
"""
elements = driver.execute_script(script)
for i, el in enumerate(elements):
    print(f"\n{i+1}. {el['tag']}")
    print(f"   Text: {el['text']}")
    print(f"   ID: {el['id']}")
    print(f"   Class: {el['class']}")

print("\n" + "="*60)
print("Press ENTER to close...")
input()
driver.quit()
