# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Telegram Manager is a production-grade CLI tool for managing Telegram conversations with a cyberpunk/synthwave aesthetic. Built with Python 3.8+, Telethon, and Rich.

## Development Commands

### Setup
```bash
# Install dependencies
uv sync

# Install in editable mode (after making changes to package structure)
uv pip install -e .
```

### Running the Application
```bash
# Main CLI entry point
uv run telegram-bot

# Alternative: direct Python execution
uv run python main.py

# Login with QR code
uv run telegram-bot --qr
```

### Code Quality
```bash
# Format code (Black)
black telegram_manager/ --line-length 100

# Sort imports (isort)
isort telegram_manager/ --profile black

# Type checking (mypy)
mypy telegram_manager/

# Linting (flake8)
flake8 telegram_manager/
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_scanner.py

# Run with asyncio support
pytest -v --asyncio-mode=auto
```

## Architecture: Clean Architecture Pattern

The codebase follows Clean Architecture (Hexagonal Architecture) with clear separation of concerns:

```
telegram_manager/
├── domain/              # Business logic (entities, policies)
│   ├── entities/       # Core domain models (DialogInfo, ScanResult)
│   └── policies/       # Business rules (bot_classification)
├── application/         # Use cases and interfaces
│   ├── use_cases/      # Application logic (scan, export, download)
│   ├── ports/          # Abstract interfaces for infrastructure
│   └── bootstrap.py    # Dependency injection container (AppContainer)
├── infrastructure/      # External integrations
│   ├── telethon/       # Telegram API implementation
│   ├── storage/        # Data persistence (JSON/CSV exporters)
│   └── config/         # Environment configuration
└── interface/          # User interface
    ├── cli.py          # CLI entry point
    └── ui/             # Rich UI components and theme
```

### Key Architectural Principles

1. **Dependency Flow**: Dependencies point inward (infrastructure → application → domain)
2. **Dependency Injection**: `AppContainer` in `bootstrap.py` wires dependencies
3. **Port-Adapter Pattern**: Use cases depend on ports (interfaces), infrastructure implements adapters
4. **Separation of Concerns**: Domain logic is isolated from framework/library details

### Bootstrap Pattern

The application uses a container-based bootstrap:

```python
# bootstrap.py creates AppContainer with all dependencies
app = build_app()  # Returns configured AppContainer

# Access dependencies through container
config = app.config
client_manager = app.client_manager

# Get use cases with runtime dependencies (client)
async with app.client_manager.get_client() as client:
    scan_use_case = app.scan_use_case(client)
    result = await scan_use_case.execute()
```

## Critical Implementation Details

### Rich Markup Syntax

**IMPORTANT**: Rich library markup has specific closing tag rules:
- ✅ Correct: `f"[{SynthwaveColors.PRIMARY}]text[/]"` (generic closing tag)
- ❌ Wrong: `f"[{SynthwaveColors.PRIMARY}]text[/{SynthwaveColors.PRIMARY}]"` (hex codes in closing tags cause errors)
- ❌ Wrong: `f"[bold]text[/bold]"` when nested inside color tags

Always use `[/]` to close Rich markup tags, never include the color code or style name in the closing tag.

### Entry Points

The package has **two** entry points:
1. `main.py` - Legacy entry point, imports from `telegram_manager.interface.cli`
2. `telegram_manager/cli.py` - Actual CLI implementation with `run()` function
3. Console script: `telegram-bot` command (defined in pyproject.toml)

All three must remain functional. The `__init__.py` imports are used by external code.

### Package Exports

`telegram_manager/__init__.py` exports public API:
- Uses **new architecture paths**: `infrastructure.telethon.*`, `infrastructure.config.*`, `domain.entities.*`
- ❌ Do NOT import from old `core.*` or `utils.*` paths (these don't exist)

### Configuration

Environment variables loaded from `.env`:
```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE=+55XXXXXXXXXX
BACKUP_DIR=./backups        # Optional
LOG_LEVEL=INFO              # Optional
```

Configuration validation happens in `TelegramConfig.from_env()` - all required vars must be present.

### Synthwave Theme

UI uses specific color palette (defined in `interface/ui/theme.py`):
- **PRIMARY**: `#ff006e` (Magenta Neon) - Headers, important text
- **SECONDARY**: `#06ffa5` (Cyan Electric) - Success, highlights
- **ACCENT**: `#8338ec` (Deep Purple) - Borders, accents
- **DANGER**: `#ff006e` (Same as primary) - Errors
- **DIM**: `#64748b` - Subdued text

UI components in `interface/ui/components.py` must maintain consistent theming.

### Session Management

Telethon session files are managed by `TelegramClientManager`:
- Session file name from config: `config.session_name` (default: "telegram_manager")
- Context manager pattern ensures proper connect/disconnect
- Handles FloodWaitError and SessionPasswordNeededError automatically
- **Database lock errors**: Close all other instances or delete session file

### Common Patterns

**Use Case Execution**:
```python
# Use cases require runtime dependencies (client) not available at bootstrap
async with app.client_manager.get_client() as client:
    use_case = app.scan_use_case(client)
    result = await use_case.execute()
```

**Progress Indication**:
```python
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
              BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%")) as progress:
    task = progress.add_task("Scanning...", total=None)
    result = await scanner.scan_all_dialogs()
    progress.update(task, completed=True)
```

## File Structure Conventions

- **Use Cases**: Single responsibility, named `{Action}{Noun}UseCase` (e.g., `ScanDialogsUseCase`)
- **Ports**: Abstract base classes defining interfaces (e.g., `DialogScannerPort`)
- **Entities**: Dataclasses with type hints (e.g., `@dataclass DialogInfo`)
- **Infrastructure**: Concrete implementations of ports, named by technology (e.g., `TelegramScanner`)

## Testing Considerations

- Tests use `pytest-asyncio` for async test support
- Set `asyncio_mode = "auto"` in pytest.ini
- Mock Telethon client for unit tests to avoid API calls
- Integration tests require valid `.env` credentials

## Package Distribution

Excluded from package (see `tool.setuptools.packages.find`):
- `backups*` - User data
- `downloads*` - Downloaded media
- `exports*` - Exported JSON/CSV files
- `benchmark_downloads*` - Performance test artifacts
- `tests*` - Test files
- `.claude*` - Claude Code configuration
