# Architecture

LogixCraft is structured as a Python package under `src/logixcraft`. The application is currently a PySide6 desktop app using Qt Designer `.ui` files for the main window and Python-built dialogs for smaller tools.

## Startup Flow

Application startup is handled by `logixcraft.app.run`:

1. Configure logging.
2. Install global Python and Qt error handlers.
3. Load settings.
4. Create the Qt application.
5. Show splash screen.
6. Run startup validation.
7. Load and apply fonts.
8. Apply selected theme.
9. Set application icon.
10. Create and show the main window.
11. Enter the Qt event loop.

## Main Areas

- `core/config.py`: application paths and version constants.
- `core/settings`: settings load, save, defaults, and corrupt-file backup.
- `core/theme`: theme catalog and stylesheet generation.
- `core/fonts.py`: bundled/system font handling.
- `core/logging_config.py`: rotating log setup.
- `core/startup_validation.py`: startup checks for runtime, settings, assets, UI, and logs.
- `ui/main_window.py`: loads and wires the main Qt window.
- `ui/navigation.py`: page navigation and navbar behavior.
- `ui/menu_actions.py`: menu action wiring and dialog launching.
- `ui/*_dialog.py`: focused dialogs such as Preferences, Terminal, License, About, Help Viewer, and Error.

## UI Pattern

The main window is loaded from `ui/main_window.ui`. Runtime logic is kept in Python controllers:

- `MainWindow` owns top-level setup.
- `NavigationController` owns page switching and navbar behavior.
- `MenuActionController` owns menus and dialogs.
- `DialogManager` keeps non-modal dialogs single-instance.

This keeps Qt Designer responsible for layout while Python remains responsible for behavior.
