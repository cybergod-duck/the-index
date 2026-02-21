#!/usr/bin/env python3
"""
ELEMENT INSPECTOR - Find the "Add a destination link" element
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
time.sleep(5)

print("\n" + "="*60)
print("INSPECTING PAGE FOR 'Add a destination link' ELEMENT")
print("="*60)

# Try to find all elements containing "destination"
print("\n1. Looking for elements containing 'destination'...")
script = """
    const allElements = document.querySelectorAll('*');
    const results = [];
    allElements.forEach(el => {
        if (el.textContent && el.textContent.toLowerCase().includes('destination')) {
            results.push({
                tag: el.tagName,
                text: el.textContent.substring(0, 100),
                id: el.id,
                className: el.className,
                role: el.getAttribute('role'),
                ariaLabel: el.getAttribute('aria-label')
            });
        }
    });
    return results;
"""
elements = driver.execute_script(script)
for i, el in enumerate(elements[:10]):  # Show first 10
    print(f"\n  Element {i+1}:")
    print(f"    Tag: {el['tag']}")
    print(f"    Text: {el['text']}")
    print(f"    ID: {el['id']}")
    print(f"    Class: {el['className']}")
    print(f"    Role: {el['role']}")
    print(f"    Aria-label: {el['ariaLabel']}")

print("\n" + "="*60)
print("Press ENTER to close browser...")
input()
driver.quit()
