#!/usr/bin/env python3
"""
Quick script to run the Pinterest bot and post the next batch of 15 pins.
This will use the fixed link injection code.
"""
import sys
import os

# Change to the project directory
os.chdir(r'C:\Projects\the-index')

# Run the main bot
from pin_bot import main

if __name__ == "__main__":
    print("=" * 60)
    print("PINTEREST BOT - BATCH RUN")
    print("=" * 60)
    print("\nThis will post up to 15 pins with proper links to crmindex.net")
    print("The bot will use your saved Pinterest login.\n")
    
    main()
