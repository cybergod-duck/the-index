import pyautogui
import time
import sys
from rich.console import Console
from rich.panel import Panel

console = Console()
pyautogui.FAILSAFE = True

def print_banner():
    console.clear()
    console.print(Panel.fit("[bold red]PINTEREST BOARD PURGE V7 (BRUTE FORCE)[/bold red]\n[yellow]Status: Taking Over Mouse & Keyboard[/yellow]", border_style="bold red"))
    console.print("[bold cyan]INSTRUCTIONS:[/bold cyan]")
    console.print("1. Open Chrome and go to: https://www.pinterest.com/CRMindex/created/")
    console.print("2. Ensure the Pinterest window is maximized on your main screen.")
    console.print("3. DO NOT touch your mouse or keyboard while this runs.")
    console.print("4. Move your mouse to any of the 4 corners of your screen to emergency abort.\n")

def delete_loop(num_pins):
    console.print(f"[bold yellow]Starting deletion loop for {num_pins} pins in 10 seconds... Switch to Chrome now![/bold yellow]")
    for i in range(10, 0, -1):
        console.print(f"Starting in {i}...")
        time.sleep(1)
        
    for i in range(num_pins):
        console.print(f"\n[bold magenta]--- Deleting Pin {i+1} of {num_pins} ---[/bold magenta]")
        
        # Refresh page to ensure clean state
        pyautogui.hotkey('ctrl', 'r')
        time.sleep(5)
        
        # Click first pin (1080p center of first pin)
        pyautogui.moveTo(480, 500, duration=0.5)
        pyautogui.click()
        time.sleep(4)
        
        # Click Ellipsis
        pyautogui.moveTo(1330, 200, duration=0.5) 
        pyautogui.click()
        time.sleep(1.5)
        
        # Click 'Edit Pin'
        pyautogui.move(0, 50, duration=0.3)
        pyautogui.click()
        time.sleep(2)
        
        # Click Delete (bottom left)
        pyautogui.moveTo(650, 850, duration=0.5)
        pyautogui.click()
        time.sleep(1.5)
        
        # Confirm Delete (center right)
        pyautogui.moveTo(1100, 600, duration=0.5)
        pyautogui.click()
        time.sleep(4)
        
        console.print("[bold green]Pin destroyed.[/bold green]")
        
        # Go back to created feed
        pyautogui.hotkey('alt', 'left')
        time.sleep(3)
        pyautogui.hotkey('alt', 'left') # double back just in case
        time.sleep(3)

if __name__ == "__main__":
    print_banner()
    try:
        delete_loop(25) 
    except pyautogui.FailSafeException:
        console.print("\n[bold red]EMERGENCY ABORT TRIGGERED. User moved mouse to corner.[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]")
    
    console.print("\n[bold green]Purge sequence finished.[/bold green]")
