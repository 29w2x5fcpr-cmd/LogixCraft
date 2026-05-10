# Project Overview

LogixCraft is intended to become a professional desktop workspace for automation engineers. The project is not limited to one PLC vendor; the long-term scope includes PLC tools, HMI/SCADA utilities, industrial networking helpers, commissioning workflows, diagnostics, reporting, and engineering documentation.

## Goals

- Provide a practical offline-first desktop app for engineering work.
- Keep common workflows fast, visible, and easy to repeat.
- Use a consistent theme and preferences system instead of hard-coded styling.
- Add safety features early: startup validation, asset checks, logging, and user-friendly error dialogs.
- Build a foundation that can support future automation-specific modules.

## Current State

The project currently has the base application shell and supporting infrastructure:

- Main PySide6 window loaded from `ui/main_window.ui`.
- Theme and font management.
- Preferences dialog.
- Logging and log rotation.
- Startup validation.
- Global exception handling.
- License, About, Help Viewer, Terminal, and Preferences dialogs.
- Animated collapsible navigation bar.
- Basic automated tests and a PowerShell test runner.

## Non-Goals For Now

- Production PLC communication.
- Licensing enforcement.
- Installer packaging.
- Full in-app documentation content.
- Plugin or module marketplace.
