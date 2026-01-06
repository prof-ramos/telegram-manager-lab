from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.text import Text
from typing import Dict, List
from .theme import ThemeStyles, SynthwaveColors


class UIComponents:
    @staticmethod
    def create_header(title: str, subtitle: str = "") -> Panel:
        content = f"[bold]{title}[/bold]"
        if subtitle:
            content += f"\n[dim]{subtitle}[/dim]"
        
        return Panel(
            Text.from_markup(content),
            border_style=ThemeStyles.HEADER,
            box=box.DOUBLE
        )
    
    @staticmethod
    def create_stats_table(stats: Dict[str, int]) -> Table:
        table = Table(
            title="Stats",
            box=box.HEAVY_HEAD,
            border_style=ThemeStyles.ACCENT
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
            'users': '👤',
            'bots': '🤖',
            'groups': '👥',
            'channels': '📢',
            'total_dialogs': '💬'
        }
        return emoji_map.get(category, '▸')
    
    @staticmethod
    def create_success_panel(message: str, details: Dict = None) -> Panel:
        content = f"[{SynthwaveColors.SUCCESS}]✓ {message}[/{SynthwaveColors.SUCCESS}]"
        
        if details:
            content += "\n\n"
            for key, value in details.items():
                content += f"[{SynthwaveColors.SECONDARY}]▸ {key}:[/{SynthwaveColors.SECONDARY}] {value}\n"
        
        return Panel(
            content,
            title="[bold green]SUCCESS[/bold green]",
            border_style=ThemeStyles.SUCCESS
        )
    
    @staticmethod
    def create_error_panel(message: str, error: Exception = None) -> Panel:
        content = f"[{SynthwaveColors.DANGER}]✗ {message}[/{SynthwaveColors.DANGER}]"
        
        if error:
            content += f"\n\n[{SynthwaveColors.DIM}]{type(error).__name__}: {str(error)}[/{SynthwaveColors.DIM}]"
        
        return Panel(
            content,
            title="[bold red]ERRO[/bold red]",
            border_style=ThemeStyles.DANGER
        )
    
    @staticmethod
    def create_info_panel(message: str) -> Panel:
        return Panel(
            f"[{SynthwaveColors.SECONDARY}]{message}[/{SynthwaveColors.SECONDARY}]",
            border_style=ThemeStyles.ACCENT
        )
