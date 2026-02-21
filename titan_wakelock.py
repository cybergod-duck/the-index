import pyautogui
import time
import sys

def keep_alive():
    print("🚀 TITAN WAKELOCK ACTIVE.")
    print("   Press Ctrl+C to stop.")
    try:
        while True:
            # Subtle nudge: 1 pixel move and back
            pyautogui.moveRel(1, 0)
            pyautogui.moveRel(-1, 0)
            # Alternatively hit a harmless key like Shift
            # pyautogui.press('shift') 
            time.sleep(60) # Nudge every 60 seconds
    except KeyboardInterrupt:
        print("\n🛑 Wakelock stopped.")

if __name__ == "__main__":
    keep_alive()
