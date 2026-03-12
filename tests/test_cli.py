"""Tests pour sandbox.cli."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from sandbox.cli import (
    _build_parser,
    _handle_demote,
    _handle_find,
    _handle_graduate,
    _handle_init,
    _handle_ls,
    _handle_new,
)
from sandbox.config import Config


@pytest.fixture
def config(tmp_path: Path) -> Config:
    sandbox_dir = tmp_path / "experiments"
    projects_dir = tmp_path / "projects"
    sandbox_dir.mkdir()
    projects_dir.mkdir()
    return Config(sandbox_path=sandbox_dir, projects_path=projects_dir)


def test_new_prints_created_path(
    config: Config, capsys: pytest.CaptureFixture[str]
) -> None:
    """new imprime le chemin du répertoire créé."""
    args = _build_parser().parse_args(["new", "redis"])
    _handle_new(args, config)
    output = capsys.readouterr().out.strip()
    assert output.endswith(f"{date.today().isoformat()}-redis")


def test_new_returns_error_if_exists(
    config: Config, capsys: pytest.CaptureFixture[str]
) -> None:
    """new retourne 1 si le répertoire existe déjà."""
    args = _build_parser().parse_args(["new", "redis"])
    _handle_new(args, config)
    code = _handle_new(args, config)
    assert code == 1


def test_ls_prints_experiments(
    config: Config, capsys: pytest.CaptureFixture[str]
) -> None:
    """ls liste les expérimentations."""
    (config.sandbox_path / "2026-03-12-alpha").mkdir()
    args = _build_parser().parse_args(["ls"])
    _handle_ls(args, config)
    output = capsys.readouterr().out
    assert "alpha" in output


def test_ls_empty_prints_message(
    config: Config, capsys: pytest.CaptureFixture[str]
) -> None:
    """ls affiche un message si aucune expérimentation."""
    args = _build_parser().parse_args(["ls"])
    _handle_ls(args, config)
    assert "No experiments" in capsys.readouterr().out


def test_graduate_prints_destination(
    config: Config, capsys: pytest.CaptureFixture[str]
) -> None:
    """graduate imprime le chemin de destination."""
    (config.sandbox_path / "2026-03-12-redis").mkdir()
    args = _build_parser().parse_args(["graduate", "redis"])
    _handle_graduate(args, config)
    output = capsys.readouterr().out.strip()
    assert str(config.projects_path) in output


def test_demote_prints_destination(
    config: Config, capsys: pytest.CaptureFixture[str]
) -> None:
    """demote imprime le chemin de destination."""
    (config.projects_path / "my-project").mkdir()
    args = _build_parser().parse_args(["demote", "my-project"])
    _handle_demote(args, config)
    output = capsys.readouterr().out.strip()
    assert str(config.sandbox_path) in output


def test_find_prints_results(
    config: Config, capsys: pytest.CaptureFixture[str]
) -> None:
    """find affiche les résultats des deux espaces."""
    (config.sandbox_path / "2026-03-12-redis-exp").mkdir()
    (config.projects_path / "redis-prod").mkdir()
    args = _build_parser().parse_args(["find", "redis"])
    _handle_find(args, config)
    output = capsys.readouterr().out
    assert "exp" in output
    assert "proj" in output


def test_init_prints_shell_function(capsys: pytest.CaptureFixture[str]) -> None:
    """init affiche la fonction shell."""
    config = Config()
    args = _build_parser().parse_args(["init"])
    _handle_init(args, config)
    output = capsys.readouterr().out
    assert "cd" in output
    assert "sandbox()" in output
