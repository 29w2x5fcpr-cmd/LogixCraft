from logixcraft.core.startup_validation import StartupValidationError, run_startup_validation

StartupCheckError = StartupValidationError

__all__ = ["StartupCheckError", "run_startup_checks"]


def run_startup_checks() -> None:
    run_startup_validation()
