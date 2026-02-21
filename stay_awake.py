import pyautogui
import time
import sys
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def keep_alive():
    console.clear()
    console.print(Panel.fit("[bold cyan]TITAN WAKELOCK v1.0[/bold cyan]\n[yellow]Status: ACTIVE[/yellow]\n[dim]Nudging mouse and toggling F15 every 60s to prevent system lock.[/dim]", border_style="bold blue"))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Maintaining wake lock...", total=None)
        
        try:
            while True:
                # 1. Subtle mouse nudge
                pyautogui.moveRel(1, 0)
                pyautogui.moveRel(-1, 0)
                
                # 2. Key toggle (F15 is commonly used as a wake-key)
                pyautogui.press('f15')
                
                time.sleep(60)
        except KeyboardInterrupt:
            console.print("\n[bold red]🛑 Wakelock terminated.[/bold red]")

if __name__ == "__main__":
    try:
        import pyautogui
    except ImportError:
        console.print("[red]Error: pyautogui not installed. Run 'pip install pyautogui'[/red]")
        sys.exit(1)
        
    keep_alive()
