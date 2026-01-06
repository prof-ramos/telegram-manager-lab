from telegram_manager.interface.ui.theme import ThemeStyles, SynthwaveColors
from rich.style import Style


def test_theme_styles_attributes():
    """Verify that ThemeStyles has all necessary attributes used in the UI."""
    assert hasattr(ThemeStyles, "PRIMARY")
    assert hasattr(ThemeStyles, "SECONDARY")
    assert hasattr(ThemeStyles, "HEADER")
    assert hasattr(ThemeStyles, "SUBHEADER")
    assert hasattr(ThemeStyles, "SUCCESS")
    assert hasattr(ThemeStyles, "WARNING")
    assert hasattr(ThemeStyles, "DANGER")
    assert hasattr(ThemeStyles, "DIM")
    assert hasattr(ThemeStyles, "ACCENT")


def test_theme_styles_values():
    """Verify that styles are correctly initialized."""
    assert isinstance(ThemeStyles.PRIMARY, Style)
    assert ThemeStyles.PRIMARY.color.name == SynthwaveColors.PRIMARY
    assert ThemeStyles.SECONDARY.color.name == SynthwaveColors.SECONDARY
