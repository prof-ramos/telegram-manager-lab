#!/usr/bin/env python3
"""
Telegram Manager - Cyber Management Suite
Interface CLI com Synthwave/Cyberpunk aesthetics
"""

import asyncio
import logging
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

from telegram_manager.core.client import TelegramClientManager
from telegram_manager.core.scanner import TelegramScanner
from telegram_manager.core.exporter import DialogExporter
from telegram_manager.ui.components import UIComponents
from telegram_manager.utils.config import TelegramConfig

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

console = Console()


async def main():
    """Ponto de entrada principal"""
    try:
        # Mostrar banner
        console.print(UIComponents.create_header(
            "TELEGRAM MANAGER",
            "Cyber Management Suite v2.0.0"
        ))
        
        # Carregar configuracao
        console.print("\n[yellow]Loading configuration...[/yellow]")
        config = TelegramConfig.from_env()
        
        if not config.validate():
            console.print(UIComponents.create_error_panel(
                "Invalid configuration in .env file"
            ))
            return
        
        # Conectar ao Telegram
        client_manager = TelegramClientManager(config)
        
        async with client_manager.get_client() as client:
            console.print(UIComponents.create_info_panel(
                "Connected to Telegram successfully!"
            ))
            
            # Escanear dialogos
            scanner = TelegramScanner(client)
            
            console.print("\n[yellow]Scanning all dialogs...[/yellow]")
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            ) as progress:
                task = progress.add_task("Scanning...", total=None)
                result = await scanner.scan_all_dialogs()
                progress.update(task, completed=True)
            
            # Mostrar resultados
            console.print("\n")
            console.print(UIComponents.create_stats_table(result.stats))
            
            # Exportar dados
            console.print("\n[yellow]Exporting data...[/yellow]")
            exporter = DialogExporter()
            json_path = exporter.export_to_json(result)
            csv_path = exporter.export_to_csv(result)
            
            console.print(UIComponents.create_success_panel(
                "Export completed successfully!",
                {
                    "JSON file": str(json_path),
                    "CSV file": str(csv_path)
                }
            ))
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation canceled by user[/yellow]")
    except ValueError as e:
        console.print(UIComponents.create_error_panel(str(e)))
    except Exception as e:
        console.print(UIComponents.create_error_panel(
            "Fatal error in application",
            error=e
        ))
        raise


if __name__ == "__main__":
    asyncio.run(main())
