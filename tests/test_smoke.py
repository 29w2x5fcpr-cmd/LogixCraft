from pathlib import Path


def test_project_structure() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (root / "src").exists()
    assert (root / "ui").exists()
