import asyncio
import logging
import datetime
from telethon import functions, types, errors
from telegram_manager.infrastructure.config.env import TelegramConfig
from telegram_manager.infrastructure.telethon.client import TelegramClientManager
from rich.console import Console

# Configuração de logging
logging.basicConfig(level=logging.WARNING)
console = Console()


async def archive_and_mute_bots():
    """
    Locates all Bots in dialogs, mutes notifications, and moves them to the Archive folder (Folder 1).

    Raises:
        errors.FloodWaitError: If Telegram rate limits are hit (handled internally with sleep/retry).
        ConnectionError: If connection to Telegram fails.
        Exception: For other unexpected runtime errors.
    """
    try:
        config = TelegramConfig.from_env()
        client_manager = TelegramClientManager(config)

        async with client_manager.get_client() as client:
            console.print("[bold cyan]󱚤 TELEGRAM BOT ARCHIVER[/bold cyan]")
            console.print("[dim]Conectado. Escaneando diálogos...[/dim]\n")

            bots_processed = 0

            # Loop contínuo enquanto houver bots
            while True:
                found_bot_in_this_pass = False
                try:
                    # Usando iter_dialogs para encontrar bots
                    # Note: folder=0 significa apenas os que não estão arquivados
                    async for dialog in client.iter_dialogs(folder=0):
                        entity = dialog.entity

                        # Verifica se é um Bot
                        if isinstance(entity, types.User) and entity.bot:
                            found_bot_in_this_pass = True
                            bot_name = dialog.name
                            console.print(
                                f"[yellow]󰚩 [/yellow] Processando Bot: [white]{bot_name}[/white]"
                            )

                            try:
                                # 1. Silenciar (Mute) por 10 anos
                                # Usando datetime.datetime.now(datetime.timezone.utc) para evitar erros de offset-naive/aware
                                far_future = datetime.datetime.now(
                                    datetime.timezone.utc
                                ) + datetime.timedelta(days=365 * 10)

                                await client(
                                    functions.account.UpdateNotifySettingsRequest(
                                        peer=dialog.input_entity,
                                        settings=types.InputPeerNotifySettings(
                                            mute_until=far_future
                                        ),
                                    )
                                )

                                # 2. Arquivar (Mover para folder 1)
                                await client.edit_folder(dialog.input_entity, 1)

                                console.print(
                                    f"   [green]✓[/green] Silenciado e Arquivado"
                                )
                                bots_processed += 1

                                # Rate limit to avoid FloodWait
                                await asyncio.sleep(1)

                            except errors.FloodWaitError as e:
                                if e.seconds > 3600:
                                    console.print(
                                        f"[bold red]Limit exceeded (>1h). Aborting.[/bold red]"
                                    )
                                    return

                                console.print(
                                    f"   [bold yellow]󱗗 Limite de rate atingido. Aguardando {e.seconds} segundos...[/bold yellow]"
                                )
                                await asyncio.sleep(e.seconds)
                                # Break out of iter_dialogs to restart and avoid stale iterator issues
                                break
                            except Exception as e:
                                console.print(
                                    f"   [red]✗ Erro:[/red] {type(e).__name__}: {str(e)}"
                                )

                    if not found_bot_in_this_pass:
                        try:
                            # Double check if any are left (sometimes pagination misses one)
                            # Simple sleep before final check
                            await asyncio.sleep(1)
                        except:
                            pass
                        break  # No more bots in folder 0

                except errors.FloodWaitError as e:
                    if e.seconds > 3600:
                        console.print(
                            f"[bold red]Global FloodWait > 1h. Aborting.[/bold red]"
                        )
                        return
                    console.print(
                        f"[bold yellow]󱗗 FloodWait global: Aguardando {e.seconds} segundos...[/bold yellow]"
                    )
                    await asyncio.sleep(e.seconds)
                    continue

            if bots_processed > 0:
                console.print(f"\n[bold green]󰄬 Operação concluída![/bold green]")
                console.print(
                    f"Total de bots processados: [bold white]{bots_processed}[/bold white]"
                )
            else:
                console.print(
                    "\n[yellow]Nenhum bot encontrado nos diálogos ativos.[/yellow]"
                )

    except Exception as e:
        console.print(f"\n[bold red]󰅚 Erro fatal:[/bold red] {str(e)}")


if __name__ == "__main__":
    asyncio.run(archive_and_mute_bots())
