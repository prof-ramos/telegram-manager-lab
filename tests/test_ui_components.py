from telegram_manager.interface.ui.components import UIComponents
from telegram_manager.interface.ui.theme import ThemeStyles, SynthwaveColors
from rich.panel import Panel
from rich.table import Table
from rich.console import Console


def test_create_header():
    """Verify header creation."""
    panel = UIComponents.create_header("Test Title", "Subtitle")
    assert isinstance(panel, Panel)
    # Check if title is in the renderable (simplified check)
    # Note: Rich objects are complex, we just check types mostly
    assert panel.border_style == ThemeStyles.HEADER


def test_create_stats_table():
    """Verify stats table creation."""
    stats = {"users": 10, "bots": 5}
    table = UIComponents.create_stats_table(stats)
    assert isinstance(table, Table)
    assert table.title == "Stats"
    assert len(table.rows) == 2


def test_get_emoji():
    """Verify emoji mapping."""
    assert UIComponents._get_emoji_for_category("users") == "👤"
    assert UIComponents._get_emoji_for_category("unknown") == "▸"


def test_selection_menu_empty():
    """Verify empty selection menu behavior."""
    console = Console()
    result = UIComponents.create_selection_menu(console, [])
    assert result is None
