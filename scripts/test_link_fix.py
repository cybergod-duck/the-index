import sys
sys.path.insert(0, r'C:\Projects\the-index')
from pin_bot import post_pin, setup_driver, load_data

# Load data
data = load_data()

# Use emergency plumbers - it has an image and was already posted, so we can test without affecting state
slug = "best-crm-emergency-plumbers"  # Has image, already posted
row = data.get(slug)

print(f"🧪 TESTING LINK FIX with: {slug}")
print(f"Industry: {row['industry']}")
print(f"Pain point: {row['pain_point']}")
print(f"\nThis is a TEST - we're re-posting an already posted pin to verify link injection works.\n")

# Setup driver
driver = setup_driver()

# Try to post
success = post_pin(driver, slug, row)

if success:
    print("\n✅ SUCCESS! Link injection is working!")
    print("The fix is ready. You can now run the full automation.")
else:
    print("\n❌ FAILED. Check the error screenshot.")

input("\nPress ENTER to close browser...")
driver.quit()

