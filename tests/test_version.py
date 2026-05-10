import subprocess

from logixcraft.core.version import (
    FALLBACK_VERSION,
    get_git_version,
    get_installed_version,
    normalize_git_version,
)


def test_normalize_git_version_removes_v_prefix() -> None:
    assert normalize_git_version("v0.1.0") == "0.1.0"
    assert normalize_git_version("v0.1.0-3-gabc1234") == "0.1.0-3-gabc1234"
    assert normalize_git_version("abc1234") == "abc1234"


def test_get_installed_version_returns_none_for_missing_package() -> None:
    assert get_installed_version("definitely-not-a-real-logixcraft-package") is None


def test_get_git_version_returns_normalized_describe(monkeypatch, tmp_path) -> None:
    def fake_run(*_args, **_kwargs):
        return subprocess.CompletedProcess(args=[], returncode=0, stdout="v0.1.0-dirty\n")

    monkeypatch.setattr("logixcraft.core.version.subprocess.run", fake_run)

    assert get_git_version(tmp_path) == "0.1.0-dirty"


def test_get_git_version_returns_none_when_git_fails(monkeypatch, tmp_path) -> None:
    def fake_run(*_args, **_kwargs):
        raise subprocess.CalledProcessError(returncode=1, cmd="git")

    monkeypatch.setattr("logixcraft.core.version.subprocess.run", fake_run)

    assert get_git_version(tmp_path) is None


def test_fallback_version_is_dev_marker() -> None:
    assert FALLBACK_VERSION == "0.0.0-dev"
