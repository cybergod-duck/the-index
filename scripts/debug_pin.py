#!/usr/bin/env python3
"""
DEBUG SCRIPT - Post ONE pin and LEAVE BROWSER OPEN so we can inspect what's happening
"""
import sys
import os
import time

# Change to the project directory
os.chdir(r'C:\Projects\the-index')

from pin_bot import setup_driver, post_pin, load_data, load_state

if __name__ == "__main__":
    print("=" * 60)
    print("DEBUG MODE - Browser will stay open after posting")
    print("=" * 60)
    
    state = load_state()
    data = load_data()
    
    # Get the first unpublished pin
    if not state["remaining"]:
        print("No pins left to post!")
        exit(1)
    
    slug = state["remaining"][0]
    print(f"\nPosting: {slug}")
    print(f"Data: {data[slug]}")
    
    driver = setup_driver()
    driver.get("https://www.pinterest.com/pin-builder/")
    time.sleep(8)
    
    print("\n🔴 BROWSER IS OPEN - Check the page manually")
    print("Press ENTER when ready to try posting...")
    input()
    
    # Try to post
    result = post_pin(driver, slug, data[slug])
    
    print(f"\n{'✅ SUCCESS' if result else '❌ FAILED'}")
    print("\n🔴 BROWSER STAYING OPEN - Inspect the page to see what happened")
    print("Press ENTER to close browser...")
    input()
    
    driver.quit()
