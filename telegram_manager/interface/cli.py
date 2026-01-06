#!/usr/bin/env python3
"""
Telegram Manager - Cyber Management Suite
Interface CLI com Synthwave/Cyberpunk aesthetics
"""

import argparse
import asyncio
import logging

import questionary
from questionary import Choice
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

from telegram_manager.application.bootstrap import build_app
from telegram_manager.interface.ui.components import UIComponents

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

console = Console()


async def main():
    """Ponto de entrada principal"""
    parser = argparse.ArgumentParser(description="Telegram Manager CLI")
    parser.add_argument("--qr", action="store_true", help="Login via QR Code")
    args = parser.parse_args()

    try:
        # Mostrar banner
        console.print(
            UIComponents.create_header(
                "TELEGRAM MANAGER", "Telegram Manager Lab v2.0.0"
            )
        )

        # Carregar configuracao
        console.print("\n[yellow]Loading configuration...[/yellow]")
        app = build_app()
        config = app.config

        if not config.validate():
            console.print(
                UIComponents.create_error_panel("Invalid configuration in .env file")
            )
            return

        # Conectar ao Telegram
        client_manager = app.client_manager

        if args.qr:
            await client_manager.authenticate_with_qr()
            # After login, the session is refreshed.
            # Continue to main execution flow.
            console.print(
                "[green]Authentication successful! Continuing with new session...[/green]"
            )

        async with client_manager.get_client() as client:
            console.print(
                UIComponents.create_info_panel("Connected to Telegram successfully!")
            )

            # Escanear dialogos
            console.print("\n[yellow]Scanning all dialogs...[/yellow]")
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            ) as progress:
                task = progress.add_task("Scanning...", total=None)
                scan_use_case = app.scan_use_case(client)
                result = await scan_use_case.execute()
                progress.remove_task(task)

            # Mostrar resultados
            console.print("\n")
            console.print(UIComponents.create_stats_table(result.stats))

            # Menu de Seleção
            options = [
                ("1", "Export Metadata (JSON/CSV)"),
                ("2", "Download Media"),
            ]
            choice = UIComponents.create_selection_menu(console, options)

            if choice == "1":
                # Exportar dados
                console.print("\n[yellow]Exporting data...[/yellow]")
                export_use_case = app.export_use_case()
                exported = export_use_case.execute(result)

                console.print(
                    UIComponents.create_success_panel(
                        "Export completed successfully!",
                        {
                            "JSON file": str(exported.json_path),
                            "CSV file": str(exported.csv_path),
                        },
                    )
                )

            elif choice == "2":
                # Download de Mídia

                # Combine all dialog lists for processing
                all_dialogs = (
                    result.users + result.bots + result.groups + result.channels
                )

                # Perguntar modo de download
                mode = await questionary.select(
                    "Choose download mode:",
                    choices=[
                        Choice("Download ALL Chats", value="all"),
                        Choice("Select Specific Chat", value="select"),
                    ],
                ).ask_async()

                if mode is None:
                    console.print("[yellow]Download canceled[/yellow]")
                    return

                target_dialogs = []
                if mode == "all":
                    target_dialogs = all_dialogs
                else:
                    # Preparar opções para seleção
                    # Ordenar por nome para facilitar busca
                    sorted_dialogs = sorted(
                        all_dialogs, key=lambda d: (d.name or "").lower()
                    )

                    choices = []
                    for d in sorted_dialogs:
                        d_type = d.type

                        safe_name = "".join(
                            c for c in (d.name or "Unnamed") if c.isprintable()
                        )
                        label = f"[{d_type}] {safe_name} ({d.id})"
                        choices.append(Choice(label, value=d))

                    selected = await questionary.select(
                        "Select chat to download (use arrow keys or type to filter):",
                        choices=choices,
                        use_indicator=True,
                        show_selected=True,
                    ).ask_async()

                    if selected:
                        target_dialogs = [selected]
                    else:
                        console.print("[yellow]No chat selected[/yellow]")
                        return

                console.print(
                    f"\n[yellow]Starting Media Download for {len(target_dialogs)} chats...[/yellow]"
                )
                download_use_case = app.download_use_case(client)

                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                ) as progress:
                    await download_use_case.execute(target_dialogs, progress)

                # Uses config object to get real download path
                try:
                    console.print(f"[debug] Config object type: {type(config)}")
                    console.print(f"[debug] Config object dir: {dir(config)}")
                    console.print(f"[debug] Config object repr: {config}")
                except:
                    pass

                console.print(
                    UIComponents.create_success_panel(
                        "Media download completed!",
                        {"Download path": str(config.download_dir)},
                    )
                )

            elif choice is None:
                console.print("\n[yellow]Selection canceled[/yellow]")

    except Exception as e:
        console.print(
            UIComponents.create_error_panel("Fatal error in application", error=e)
        )
        import sys

        sys.exit(1)


def run():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nOperation canceled by user")
        import sys

        sys.exit(0)


if __name__ == "__main__":
    run()
