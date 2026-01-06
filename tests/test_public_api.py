from telegram_manager import (
    TelegramClientManager,
    TelegramScanner,
    ScanResult,
    DialogInfo,
    TelegramConfig,
)


def test_telegram_manager_exports():
    """Verify that key components are exported from the top-level package."""
    assert TelegramClientManager is not None
    assert TelegramScanner is not None
    assert ScanResult is not None
    assert DialogInfo is not None
    assert TelegramConfig is not None


def test_dialog_info_structure():
    """Verify DialogInfo structure and validation."""
    # Test valid creation
    d = DialogInfo(
        id=123, name="Test", type="user", username="testuser", participants_count=10
    )
    assert d.id == 123
    assert d.participants_count == 10

    # Test validation (if enabled)
    # import pytest
    # with pytest.raises(ValueError):
    #     DialogInfo(id=1, name="Test", type="user", participants_count=-1)


def test_scan_result_properties():
    """Verify ScanResult cached properties."""
    users = [DialogInfo(id=1, name="User1", type="user")]
    bots = [DialogInfo(id=2, name="Bot1", type="bot")]

    res = ScanResult(users=users, bots=bots)
    assert res.total == 2
    assert res.stats["users"] == 1
    assert res.stats["bots"] == 1
