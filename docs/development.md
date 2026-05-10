# Development Setup

## Environment

Use a virtual environment from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run the app:

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m logixcraft.main
```

## Useful Commands

Fast verification:

```powershell
powershell -ExecutionPolicy Bypass -File tools\run_tests.ps1 -Fast
```

Full verification:

```powershell
powershell -ExecutionPolicy Bypass -File tools\run_tests.ps1
```

Lint only:

```powershell
.\.venv\Scripts\python.exe -m ruff check src\logixcraft tests
```

## Editing Guidelines

- Keep UI behavior in Python controllers rather than embedding it in the `.ui` file.
- Prefer theme tokens and generated stylesheets over one-off widget styling.
- Add focused tests for new behavior.
- Avoid committing generated logs, local settings, backups, or virtual environments.
- Keep runtime user settings outside the repository.
