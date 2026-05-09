from pathlib import Path


class ResourceError(RuntimeError):
    pass


def require_file(path: Path, description: str) -> Path:
    if not path.is_file():
        raise ResourceError(f"Missing {description}: {path}")
    return path


def require_directory(path: Path, description: str) -> Path:
    if not path.is_dir():
        raise ResourceError(f"Missing {description}: {path}")
    return path
