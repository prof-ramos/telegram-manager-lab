from rich.style import Style
from enum import Enum


class SynthwaveColors(str, Enum):
    PRIMARY = "#ff006e"
    SECONDARY = "#06ffa5"
    ACCENT = "#8338ec"
    BG = "#1a1a2e"
    SUCCESS = "#06ffa5"
    WARNING = "#ffbe0b"
    DANGER = "#ff006e"
    DIM = "#64748b"


class ThemeStyles:
    HEADER = Style(color=SynthwaveColors.PRIMARY, bold=True)
    SUBHEADER = Style(color=SynthwaveColors.SECONDARY, italic=True)
    SUCCESS = Style(color=SynthwaveColors.SUCCESS, bold=True)
    WARNING = Style(color=SynthwaveColors.WARNING)
    DANGER = Style(color=SynthwaveColors.DANGER, bold=True)
    DIM = Style(color=SynthwaveColors.DIM, dim=True)
    ACCENT = Style(color=SynthwaveColors.ACCENT)


CYBER_SPINNER = ["[◐]", "[◓]", "[◑]", "[◒]"]
NEON_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
OFFICIAL_BOTS = ['BotFather', 'SpamBot', 'TelegramSupport', 'notifications', 'GroupAnonymousBot']
