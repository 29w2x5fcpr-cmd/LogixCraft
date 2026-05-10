# LogixCraft

LogixCraft is a Windows-focused desktop engineering workspace for industrial automation work. It is being built as a practical toolset for PLC systems, HMI/SCADA platforms, industrial networks, commissioning, diagnostics, documentation, and day-to-day engineering workflows.

The application is currently in early development. The foundation is a Python and PySide6 desktop app with theme management, font handling, preferences, startup validation, logging, global error handling, help/about dialogs, and a growing navigation structure for engineering tools.

## Current Capabilities

- PySide6 desktop shell with Qt Designer based main window.
- Theme system with multiple selectable themes.
- Font loading and user-selectable application font.
- Preferences dialog for appearance, window, and advanced settings.
- Splash screen and startup validation.
- Rotating application logs and an Open Logs Folder action.
- User-facing error dialog with technical details.
- Terminal/log viewer dialog.
- License, About, and Help Viewer placeholder dialogs.
- Collapsible animated navigation bar.
- Basic automated test runner and regression tests.

## Planned Areas

- PLC tooling and tag workflows.
- HMI/SCADA support utilities.
- Industrial network helpers.
- Commissioning and diagnostic workflows.
- Documentation and report generation tools.
- Searchable in-app help content.
- Packaging and release automation.

## Project Documentation

Documentation starts in the [docs](docs/README.md) folder:

- [Project Overview](docs/overview.md)
- [Architecture](docs/architecture.md)
- [Development Setup](docs/development.md)
- [Testing](docs/testing.md)
- [Roadmap](docs/roadmap.md)

## Requirements

- Windows
- Python 3.12 or newer
- Virtual environment recommended

Install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Running

From the repository root:

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m logixcraft.main
```

## Testing

Fast checks:

```powershell
powershell -ExecutionPolicy Bypass -File tools\run_tests.ps1 -Fast
```

Full test runner:

```powershell
powershell -ExecutionPolicy Bypass -File tools\run_tests.ps1
```

The full runner executes test files separately because Qt tests can leave process state behind when everything runs in one Python process.

## Repository Layout

```text
assets/          Application icons, fonts, and visual assets
config/          Default configuration files
docs/            Project documentation
src/logixcraft/  Application source code
tests/           Automated tests
tools/           Developer scripts
ui/              Qt Designer .ui files
```

## Versioning

The application resolves its version from Git tags when running from source. Release tags use the `vMAJOR.MINOR.PATCH` format, for example `v0.1.1`.
