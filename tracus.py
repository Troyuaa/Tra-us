from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
import requests
from bs4 import BeautifulSoup
import socket
from datetime import datetime
import os

console = Console()

def show_banner():
    banner = r"""
 _______                     _____  
|__   __|                   / ____| 
   | | ___  __ _ _ __ ___  | (___   
   | |/ _ \/ _` | '_ ` _ \  \___ \  
   | |  __/ (_| | | | | | | ____) | 
   |_|\___|\__,_|_| |_| |_| |_____/  
                                    
    """
    text_banner = Text(banner, style="bold bright_cyan")
    console.print(Align.center(text_banner))

def count_pages(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        links = set()
        for link in soup.find_all("a", href=True):
            href = link['href']
            if href.startswith("/") or href.startswith(url):
                links.add(href)
        return len(links) if links else 1
    except Exception as e:
        console.print(f"[red]Error counting pages: {e}[/red]")
        return 0

def get_ip(url):
    try:
        hostname = url.split("//")[-1].split("/")[0]
        ip = socket.gethostbyname(hostname)
        return ip
    except Exception as e:
        console.print(f"[red]Error getting IP: {e}[/red]")
        return "Unknown"

def check_basic_vulnerabilities(url):
    vulns = []
    try:
        response = requests.get(url, timeout=10)
        content = response.text.lower()
        if "admin" in content:
            vulns.append("Page may contain exposed admin area")
        if "password" in content:
            vulns.append("Possible password exposure in text")
        if "error" in content:
            vulns.append("Pages with visible error messages")
        if not vulns:
            vulns.append("No basic vulnerabilities detected")
    except Exception as e:
        vulns.append(f"Error checking vulnerabilities: {e}")
    return vulns

def get_owner_info(url):
    try:
        hostname = url.split("//")[-1].split("/")[0]
        response = requests.get(f"https://whoisjsonapi.com/api/v1/whois?domain={hostname}")
        data = response.json()
        info = {
            "Domain": data.get("domainName", "Unknown"),
            "Registrar": data.get("registrarName", "Unknown"),
            "Creation Date": data.get("creationDate", "Unknown"),
            "Expiration Date": data.get("expirationDate", "Unknown"),
            "Name Servers": ", ".join(data.get("nameServers", [])) if data.get("nameServers") else "Unknown",
            "Status": ", ".join(data.get("status", [])) if data.get("status") else "Unknown",
        }
        return info
    except Exception as e:
        return {"Error": f"Could not fetch owner info: {e}"}

def generate_report(url, pages, ip, vulns, owner):
    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"TraçuS Report - {datetime.now()}\n")
        f.write(f"URL analyzed: {url}\n")
        f.write(f"Number of pages found: {pages}\n")
        f.write(f"Site IP: {ip}\n\n")
        f.write("Detected vulnerabilities:\n")
        for v in vulns:
            f.write(f"- {v}\n")
        f.write("\nOwner information:\n")
        for k, v in owner.items():
            f.write(f"{k}: {v}\n")
    console.print(f"\n[bold green]Report saved at {os.path.abspath(filename)}[/bold green]")

def menu():
    while True:
        console.clear()
        show_banner()

        menu_title = Text("⚡️ [bold underline bright_yellow]MAIN MENU TraçuS[/bold underline bright_yellow] ⚡️", justify="center")
        panel = Panel(menu_title, style="bold blue", padding=(1, 4))
        console.print(panel)

        options = [
            ("1", "[green]🔍 Count Pages[/green]"),
            ("2", "[cyan]🌐 Show Site IP[/cyan]"),
            ("3", "[red]⚠️ Check Basic Vulnerabilities[/red]"),
            ("4", "[magenta]👤 Owner Information[/magenta]"),
            ("5", "[yellow]📝 Generate Full Report[/yellow]"),
            ("0", "[bold red]❌ Exit[/bold red]"),
        ]

        for key, desc in options:
            console.print(f"  [bold bright_white]{key}[/bold bright_white] → {desc}")

        choice = Prompt.ask("\n[bold bright_cyan]Choose an option[/bold bright_cyan]", choices=[k for k, _ in options])

        if choice == '0':
            console.print("\n[bold green]Exiting TraçuS... See you soon![/bold green]")
            break

        url = Prompt.ask("\n[bright_white]Enter the website URL (e.g., https://example.com)[/bright_white]").strip()
        if not url.startswith('http'):
            url = 'https://' + url

        if choice == '1':
            pages = count_pages(url)
            console.print(f"\n🔢 Pages found: [bold green]{pages}[/bold green]")
            input("\nPress Enter to continue...")
        elif choice == '2':
            ip = get_ip(url)
            console.print(f"\n🌍 Site IP: [bold green]{ip}[/bold green]")
            input("\nPress Enter to continue...")
        elif choice == '3':
            vulns = check_basic_vulnerabilities(url)
            console.print("\n⚠️ [bold red]Basic vulnerabilities detected:[/bold red]")
            for v in vulns:
                console.print(f"- {v}")
            input("\nPress Enter to continue...")
        elif choice == '4':
            owner = get_owner_info(url)
            table = Table(title="👤 Owner Information", style="bright_magenta")
            table.add_column("Field", style="cyan", no_wrap=True)
            table.add_column("Value", style="magenta")
            for k, v in owner.items():
                table.add_row(k, str(v))
            console.print(table)
            input("\nPress Enter to continue...")
        elif choice == '5':
            pages = count_pages(url)
            ip = get_ip(url)
            vulns = check_basic_vulnerabilities(url)
            owner = get_owner_info(url)
            generate_report(url, pages, ip, vulns, owner)
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    menu()
