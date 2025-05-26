import requests
from bs4 import BeautifulSoup
import socket
import json
from datetime import datetime
import os

from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table

console = Console()

def mostrar_banner():
    banner = r"""
 _______                     _____  
|__   __|                   / ____| 
   | | ___  __ _ _ __ ___  | (___   
   | |/ _ \/ _` | '_ ` _ \  \___ \  
   | |  __/ (_| | | | | | | ____) | 
   |_|\___|\__,_|_| |_| |_| |_____/  
                                    
    """
    texto_banner = Text(banner, style="bold bright_cyan")
    console.print(Align.center(texto_banner))

def contar_paginas(url):
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
        console.print(f"[red]Erro ao contar páginas: {e}[/red]")
        return 0

def pegar_ip(url):
    try:
        hostname = url.split("//")[-1].split("/")[0]
        ip = socket.gethostbyname(hostname)
        return ip
    except Exception as e:
        console.print(f"[red]Erro ao pegar IP: {e}[/red]")
        return "Desconhecido"

def verificar_falhas_simples(url):
    # Apenas uma simulação simples para demo:
    falhas = []
    try:
        response = requests.get(url, timeout=10)
        content = response.text.lower()
        if "admin" in content:
            falhas.append("Página pode conter área administrativa exposta")
        if "password" in content:
            falhas.append("Possível exposição de senha em texto")
        if "error" in content:
            falhas.append("Páginas com mensagens de erro visíveis")
        if not falhas:
            falhas.append("Nenhuma falha simples detectada")
    except Exception as e:
        falhas.append(f"Erro ao verificar falhas: {e}")
    return falhas

def info_responsavel(url):
    # Para demo, usando whois via API pública (json whois):
    try:
        hostname = url.split("//")[-1].split("/")[0]
        response = requests.get(f"https://whoisjsonapi.com/api/v1/whois?domain={hostname}")
        data = response.json()
        info = {
            "Domain": data.get("domainName", "Desconhecido"),
            "Registrar": data.get("registrarName", "Desconhecido"),
            "Creation Date": data.get("creationDate", "Desconhecido"),
            "Expiration Date": data.get("expirationDate", "Desconhecido"),
            "Name Servers": ", ".join(data.get("nameServers", [])) if data.get("nameServers") else "Desconhecido",
            "Status": ", ".join(data.get("status", [])) if data.get("status") else "Desconhecido",
        }
        return info
    except Exception as e:
        return {"Erro": f"Não foi possível obter informações do responsável: {e}"}

def gerar_relatorio(url, paginas, ip, falhas, responsavel):
    filename = f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Relatório TraçuS - {datetime.now()}\n")
        f.write(f"URL analisada: {url}\n")
        f.write(f"Número de páginas encontradas: {paginas}\n")
        f.write(f"IP do site: {ip}\n\n")
        f.write("Falhas detectadas:\n")
        for f_ in falhas:
            f.write(f"- {f_}\n")
        f.write("\nInformações do responsável:\n")
        for k, v in responsavel.items():
            f.write(f"{k}: {v}\n")
    console.print(f"\n[bold green]Relatório salvo em {os.path.abspath(filename)}[/bold green]")

def menu():
    while True:
        console.clear()
        mostrar_banner()

        titulo_menu = Text("⚡️ [bold underline bright_yellow]MENU PRINCIPAL TraçuS[/bold underline bright_yellow] ⚡️", justify="center")
        painel = Panel(titulo_menu, style="bold blue", padding=(1, 4))
        console.print(painel)

        opcoes = [
            ("1", "[green]🔍 Contar páginas[/green]"),
            ("2", "[cyan]🌐 Mostrar IP do site[/cyan]"),
            ("3", "[red]⚠️ Verificar falhas simples[/red]"),
            ("4", "[magenta]👤 Informações do responsável[/magenta]"),
            ("5", "[yellow]📝 Gerar relatório completo[/yellow]"),
            ("0", "[bold red]❌ Sair[/bold red]"),
        ]

        for key, desc in opcoes:
            console.print(f"  [bold bright_white]{key}[/bold bright_white] → {desc}")

        opc = Prompt.ask("\n[bold bright_cyan]Escolha uma opção[/bold bright_cyan]", choices=[k for k, _ in opcoes])

        if opc == '0':
            console.print("\n[bold green]Saindo do TraçuS... Até logo![/bold green]")
            break

        url = Prompt.ask("\n[bright_white]Digite a URL do site (ex: https://inovetoldos.com.br)[/bright_white]").strip()
        if not url.startswith('http'):
            url = 'https://' + url

        if opc == '1':
            paginas = contar_paginas(url)
            console.print(f"\n🔢 Páginas encontradas: [bold green]{paginas}[/bold green]")
            input("\nPressione Enter para continuar...")
        elif opc == '2':
            ip = pegar_ip(url)
            console.print(f"\n🌍 IP do site: [bold green]{ip}[/bold green]")
            input("\nPressione Enter para continuar...")
        elif opc == '3':
            falhas = verificar_falhas_simples(url)
            console.print("\n⚠️ [bold red]Falhas simples detectadas:[/bold red]")
            for f_ in falhas:
                console.print(f"- {f_}")
            input("\nPressione Enter para continuar...")
        elif opc == '4':
            responsavel = info_responsavel(url)
            table = Table(title="👤 Informações do Responsável", style="bright_magenta")
            table.add_column("Campo", style="cyan", no_wrap=True)
            table.add_column("Valor", style="magenta")
            for k, v in responsavel.items():
                table.add_row(k, str(v))
            console.print(table)
            input("\nPressione Enter para continuar...")
        elif opc == '5':
            paginas = contar_paginas(url)
            ip = pegar_ip(url)
            falhas = verificar_falhas_simples(url)
            responsavel = info_responsavel(url)
            gerar_relatorio(url, paginas, ip, falhas, responsavel)
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    menu()
