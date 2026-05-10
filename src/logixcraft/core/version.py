import subprocess
from functools import lru_cache
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

FALLBACK_VERSION = "0.0.0-dev"
PACKAGE_NAME = "logixcraft"


@lru_cache(maxsize=1)
def get_app_version(project_root: Path | None = None) -> str:
    installed_version = get_installed_version(PACKAGE_NAME)
    if installed_version is not None:
        return installed_version

    git_version = get_git_version(project_root)
    if git_version is not None:
        return git_version

    return FALLBACK_VERSION


def get_installed_version(package_name: str) -> str | None:
    try:
        return version(package_name)
    except PackageNotFoundError:
        return None


def get_git_version(project_root: Path | None = None) -> str | None:
    root = project_root or Path(__file__).resolve().parents[3]

    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--dirty", "--always"],
            cwd=root,
            capture_output=True,
            check=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None

    resolved = result.stdout.strip()
    return normalize_git_version(resolved) if resolved else None


def normalize_git_version(raw_version: str) -> str:
    return raw_version[1:] if raw_version.startswith("v") else raw_version
