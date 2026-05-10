# Testing

Tests live in the `tests` folder and use `pytest`.

## Running Tests

Fast checks:

```powershell
powershell -ExecutionPolicy Bypass -File tools\run_tests.ps1 -Fast
```

Full checks:

```powershell
powershell -ExecutionPolicy Bypass -File tools\run_tests.ps1
```

The test runner sets `QT_QPA_PLATFORM=offscreen` so PySide6 tests can run without showing application windows.

## Current Coverage Areas

- Project structure smoke test.
- Startup flow with mocked UI/event loop.
- Settings load/save and corrupt settings backup.
- Theme catalog and stylesheet rendering.
- Font manager behavior.
- Startup validation.
- Logging rotation.
- Error dialog summaries and technical detail toggle.
- Navigation and collapsible navbar behavior.
- Menu action creation.
- License, About, Help Viewer, Terminal, and Splash dialogs.

## Testing Notes

The full runner executes each test file in a fresh pytest process. This avoids cross-test process state issues that can happen with Qt widgets and application-level hooks.

When adding UI tests:

- Use `QT_QPA_PLATFORM=offscreen`.
- Build minimal fake windows when possible.
- Test controller behavior separately from visual appearance.
- Keep timing-based animation waits small and focused.
