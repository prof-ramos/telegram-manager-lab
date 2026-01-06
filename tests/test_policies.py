from telegram_manager.domain.policies.bot_classification import (
    is_official_bot,
    OFFICIAL_BOTS,
)


def test_is_official_bot_case_insensitive():
    """Verify official bot check deals with case."""
    assert is_official_bot("BotFather") is True
    assert is_official_bot("botfather") is True
    assert is_official_bot("telegramsupport") is True


def test_is_official_bot_whitespace():
    """Verify whitespace handling."""
    assert is_official_bot(" BotFather ") is True


def test_is_official_bot_negative():
    """Verify non-official bots are rejected."""
    assert is_official_bot("random_bot") is False
    assert is_official_bot(None) is False
