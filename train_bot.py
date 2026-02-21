#!/usr/bin/env python3
"""
INTERACTIVE TRAINER - You show me what to click, I'll record it
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path

BASE_DIR = Path(r'C:\Projects\the-index')
PROFILE_DIR = BASE_DIR / 'chrome_profile_final'

# Setup Chrome
chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={PROFILE_DIR}")
chrome_options.add_argument("--profile-directory=Default")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

print("="*70)
print("INTERACTIVE TRAINER")
print("="*70)
print("\nI'll open Pinterest pin-builder.")
print("YOU manually create a pin and I'll WATCH what elements you interact with.")
print("\nPress ENTER to start...")
input()

driver.get("https://www.pinterest.com/pin-builder/")
print("\n✅ Page loaded. Now YOU do the following:")
print("   1. Fill the title")
print("   2. Fill the description")  
print("   3. Fill the link")
print("   4. Upload the image")
print("   5. Click publish")
print("\nPress ENTER after each step so I can record what element you used...")

# Step 1: Title
input("\nPress ENTER after you've filled the TITLE...")
title_elem = driver.execute_script("""
    const activeEl = document.activeElement;
    if (!activeEl || activeEl === document.body) {
        // Try to find title field that was recently modified
        const inputs = document.querySelectorAll('input, textarea, [contenteditable="true"]');
        for (let el of inputs) {
            if (el.value && el.value.includes('CRM')) {
                return {
                    tag: el.tagName,
                    id: el.id,
                    name: el.name,
                    className: el.className,
                    placeholder: el.placeholder,
                    value: el.value,
                    role: el.getAttribute('role'),
                    ariaLabel: el.getAttribute('aria-label')
                };
            }
        }
    }
    return {
        tag: activeEl.tagName,
        id: activeEl.id,
        name: activeEl.name,
        className: activeEl.className,
        placeholder: activeEl.placeholder,
        value: activeEl.value,
        role: activeEl.getAttribute('role'),
        ariaLabel: activeEl.getAttribute('aria-label')
    };
""")
print("\n📝 TITLE ELEMENT:")
for k, v in title_elem.items():
    if v:
        print(f"   {k}: {v}")

# Step 2: Description
input("\nPress ENTER after you've filled the DESCRIPTION...")
desc_elem = driver.execute_script("""
    const activeEl = document.activeElement;
    return {
        tag: activeEl.tagName,
        id: activeEl.id,
        className: activeEl.className,
        role: activeEl.getAttribute('role'),
        ariaLabel: activeEl.getAttribute('aria-label'),
        placeholder: activeEl.placeholder,
        innerHTML: activeEl.innerHTML ? activeEl.innerHTML.substring(0, 100) : ''
    };
""")
print("\n📝 DESCRIPTION ELEMENT:")
for k, v in desc_elem.items():
    if v:
        print(f"   {k}: {v}")

# Step 3: Link
input("\nPress ENTER after you've filled the LINK...")
link_elem = driver.execute_script("""
    const activeEl = document.activeElement;
    return {
        tag: activeEl.tagName,
        id: activeEl.id,
        type: activeEl.type,
        className: activeEl.className,
        placeholder: activeEl.placeholder,
        value: activeEl.value,
        role: activeEl.getAttribute('role'),
        ariaLabel: activeEl.getAttribute('aria-label')
    };
""")
print("\n📝 LINK ELEMENT:")
for k, v in link_elem.items():
    if v:
        print(f"   {k}: {v}")

# Step 4: Image upload (file input)
input("\nPress ENTER after you've uploaded the IMAGE...")
print("✅ Image uploaded")

# Step 5: Publish button
input("\nPress ENTER after you can SEE the publish button (don't click yet)...")
publish_elem = driver.execute_script("""
    const buttons = document.querySelectorAll('button');
    for (let btn of buttons) {
        if (btn.textContent.includes('Publish')) {
            return {
                tag: btn.tagName,
                id: btn.id,
                className: btn.className,
                text: btn.textContent,
                dataTestId: btn.getAttribute('data-test-id'),
                role: btn.getAttribute('role'),
                ariaLabel: btn.getAttribute('aria-label')
            };
        }
    }
    return null;
""")
if publish_elem:
    print("\n📝 PUBLISH BUTTON:")
    for k, v in publish_elem.items():
        if v:
            print(f"   {k}: {v}")

print("\n" + "="*70)
print("TRAINING COMPLETE!")
print("="*70)
print("\nI've recorded all the elements you used.")
print("Press ENTER to close...")
input()

driver.quit()
