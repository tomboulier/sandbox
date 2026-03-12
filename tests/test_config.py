"""Tests pour sandbox.config."""

from pathlib import Path

import pytest

from sandbox.config import Config


def test_default_sandbox_path() -> None:
    """Le chemin sandbox par défaut pointe vers Expérimentations."""
    config = Config()
    expected = Path.home() / "Documents/03-Ressources/Expérimentations"
    assert config.sandbox_path == expected


def test_default_projects_path() -> None:
    """Le chemin projets par défaut pointe vers 01-Projets."""
    config = Config()
    assert config.projects_path == Path.home() / "Documents/01-Projets"


def test_sandbox_path_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """SANDBOX_PATH surcharge le chemin par défaut."""
    monkeypatch.setenv("SANDBOX_PATH", "/tmp/my-sandbox")
    config = Config()
    assert config.sandbox_path == Path("/tmp/my-sandbox")


def test_projects_path_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """SANDBOX_PROJECTS_PATH surcharge le chemin projets par défaut."""
    monkeypatch.setenv("SANDBOX_PROJECTS_PATH", "/tmp/my-projects")
    config = Config()
    assert config.projects_path == Path("/tmp/my-projects")


def test_paths_are_expanded(monkeypatch: pytest.MonkeyPatch) -> None:
    """Les chemins avec ~ sont expandés."""
    monkeypatch.setenv("SANDBOX_PATH", "~/experiments")
    config = Config()
    assert config.sandbox_path == Path.home() / "experiments"
    assert not str(config.sandbox_path).startswith("~")
