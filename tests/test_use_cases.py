import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram_manager.application.use_cases.scan_dialogs import ScanDialogsUseCase
from telegram_manager.domain.entities.dialog import ScanResult
from telegram_manager.application.ports.dialog_scanner import DialogScanner


@pytest.mark.asyncio
async def test_scan_dialogs_use_case():
    # Mock scanner
    mock_scanner = MagicMock(spec=DialogScanner)
    expected_result = ScanResult(users=[], bots=[], groups=[], channels=[])
    mock_scanner.scan_all_dialogs = AsyncMock(return_value=expected_result)

    use_case = ScanDialogsUseCase(mock_scanner)
    result = await use_case.execute()

    assert result == expected_result
    mock_scanner.scan_all_dialogs.assert_called_once()


@pytest.mark.asyncio
async def test_scan_dialogs_failure():
    mock_scanner = MagicMock(spec=DialogScanner)
    mock_scanner.scan_all_dialogs = AsyncMock(side_effect=Exception("Scan failed"))

    use_case = ScanDialogsUseCase(mock_scanner)

    with pytest.raises(Exception):
        await use_case.execute()
