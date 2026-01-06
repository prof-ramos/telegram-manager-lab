import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from telegram_manager.infrastructure.storage.dialog_exporter import DialogExporter
from telegram_manager.domain.entities.dialog import ScanResult, DialogInfo


@pytest.fixture
def sample_scan_result():
    users = [DialogInfo(id=1, name="User1", type="user")]
    bots = [DialogInfo(id=2, name="Bot1", type="bot")]
    groups = []
    channels = []
    return ScanResult(users=users, bots=bots, groups=groups, channels=channels)


def test_export_to_json(tmp_path, sample_scan_result):
    exporter = DialogExporter(output_dir=tmp_path)
    path = exporter.export_to_json(sample_scan_result)

    assert path.exists()
    assert path.suffix == ".json"


def test_export_to_csv(tmp_path, sample_scan_result):
    exporter = DialogExporter(output_dir=tmp_path)
    path = exporter.export_to_csv(sample_scan_result)

    assert path.exists()
    assert path.suffix == ".csv"


def test_export_structure(tmp_path, sample_scan_result):
    exporter = DialogExporter(output_dir=tmp_path)
    path = exporter.export_to_csv(sample_scan_result)

    # Read CSV content to verify structure
    content = path.read_text("utf-8")
    assert "id,name,type,username" in content
    assert "User1" in content
    assert "Bot1" in content
