from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.text import Text
from rich.console import Console
from rich.markup import escape
from rich.prompt import Prompt
from typing import Dict, List, Optional, Tuple
from .theme import ThemeStyles, SynthwaveColors


class UIComponents:
    @staticmethod
    def create_header(title: str, subtitle: str = "") -> Panel:
        content = f"[bold]{title}[/bold]"
        if subtitle:
            content += f"\n[dim]{subtitle}[/dim]"

        return Panel(
            Text.from_markup(content), border_style=ThemeStyles.HEADER, box=box.DOUBLE
        )

    @staticmethod
    def create_stats_table(stats: Dict[str, int]) -> Table:
        table = Table(
            title="Stats", box=box.HEAVY_HEAD, border_style=ThemeStyles.ACCENT
        )

        table.add_column("Categoria", style=ThemeStyles.SECONDARY)
        table.add_column("Quantidade", justify="right", style=ThemeStyles.PRIMARY)

        for key, value in stats.items():
            emoji = UIComponents._get_emoji_for_category(key)
            table.add_row(f"{emoji} {key.title()}", str(value))

        return table

    @staticmethod
    def _get_emoji_for_category(category: str) -> str:
        emoji_map = {
            "users": "👤",
            "bots": "🤖",
            "groups": "👥",
            "channels": "📢",
            "total_dialogs": "💬",
        }
        return emoji_map.get(category, "▸")

    @staticmethod
    def create_success_panel(message: str, details: Dict = None) -> Panel:
        content = f"[{SynthwaveColors.SUCCESS.value}]✓ {message}[/]"

        if details:
            content += "\n\n"
            detail_lines = []
            for key, value in details.items():
                detail_lines.append(
                    f"[{SynthwaveColors.SECONDARY.value}]▸ {key}:[/] {value}"
                )
            content += "\n".join(detail_lines)

        return Panel(
            content,
            title="[bold green]SUCCESS[/bold green]",
            border_style=ThemeStyles.SUCCESS,
        )

    @staticmethod
    def create_error_panel(message: str, error: Exception = None) -> Panel:
        safe_message = escape(message)
        content = f"[{SynthwaveColors.DANGER.value}]✗ {safe_message}[/]"

        if error:
            safe_error = escape(str(error))
            content += (
                f"\n\n[{SynthwaveColors.DIM.value}]"
                f"{type(error).__name__}: {safe_error}[/]"
            )

        return Panel(
            content, title="[bold red]ERRO[/bold red]", border_style=ThemeStyles.DANGER
        )

    @staticmethod
    def create_info_panel(message: str) -> Panel:
        return Panel(
            f"[{SynthwaveColors.SECONDARY.value}]{message}[/]",
            border_style=ThemeStyles.ACCENT,
        )

    @staticmethod
    def create_selection_menu(
        console: Console,
        options: List[Tuple[str, str]],
        title: str = "Select Action",
        default: str = "1",
    ) -> Optional[str]:
        """Create a selection menu with numbered options"""
        table = Table(show_header=False, box=None, padding=(0, 2))

        choices = []
        for option_id, label in options:
            id_text = Text(f"[{option_id}]", style=ThemeStyles.ACCENT)
            table.add_row(id_text, Text(label, style="bold white"))
            choices.append(option_id)

        console.print("\n")
        console.print(f"[bold {SynthwaveColors.PRIMARY.value}]{title.upper()}[/]")
        # Calculate visual length of the title (approximate)
        if not options:
            console.print("[yellow]No options available.[/yellow]")
            return None

        # Validate default
        valid_choices = [opt[0] for opt in options]
        if default not in valid_choices:
            default = valid_choices[0] if valid_choices else None

        console.print(table)
        console.print("\n")

        try:
            # Calculate visual length of the title (approximate)
            separator_length = len(title) + 4
            console.print("─" * separator_length, style=SynthwaveColors.ACCENT.value)

            choice = Prompt.ask(
                "Select option",
                choices=valid_choices,
                default=default,
                show_choices=False,
            )
            return choice
        except (KeyboardInterrupt, EOFError):
            return None
