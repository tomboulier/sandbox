"""Tests pour graduate et demote."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from sandbox.config import Config
from sandbox.core import demote, graduate


@pytest.fixture
def config(tmp_path: Path) -> Config:
    sandbox_dir = tmp_path / "experiments"
    projects_dir = tmp_path / "projects"
    sandbox_dir.mkdir()
    projects_dir.mkdir()
    return Config(sandbox_path=sandbox_dir, projects_path=projects_dir)


# ---------------------------------------------------------------------------
# graduate
# ---------------------------------------------------------------------------


def test_graduate_moves_to_projects(config: Config) -> None:
    """graduate() déplace l'expérimentation vers projects."""
    exp = config.sandbox_path / "2026-03-12-redis"
    exp.mkdir()
    dest = graduate("redis", config)
    assert dest == config.projects_path / "2026-03-12-redis"
    assert dest.is_dir()
    assert not exp.exists()


def test_graduate_raises_if_not_found(config: Config) -> None:
    """graduate() lève FileNotFoundError si rien ne correspond."""
    with pytest.raises(FileNotFoundError):
        graduate("nonexistent", config)


def test_graduate_raises_if_destination_exists(config: Config) -> None:
    """graduate() lève FileExistsError si la destination existe déjà."""
    exp = config.sandbox_path / "2026-03-12-redis"
    exp.mkdir()
    (config.projects_path / "2026-03-12-redis").mkdir()
    with pytest.raises(FileExistsError):
        graduate("redis", config)


def test_graduate_matches_by_substring(config: Config) -> None:
    """graduate() trouve l'expérimentation par sous-chaîne."""
    exp = config.sandbox_path / "2026-03-12-my-redis-experiment"
    exp.mkdir()
    dest = graduate("redis", config)
    assert "redis" in dest.name


# ---------------------------------------------------------------------------
# demote
# ---------------------------------------------------------------------------


def test_demote_moves_to_sandbox(config: Config) -> None:
    """demote() déplace le projet vers sandbox."""
    proj = config.projects_path / "my-project"
    proj.mkdir()
    dest = demote("my-project", config)
    today = date.today().isoformat()
    assert dest == config.sandbox_path / f"{today}-my-project"
    assert dest.is_dir()
    assert not proj.exists()


def test_demote_preserves_date_prefix_if_present(config: Config) -> None:
    """demote() ne double pas le préfixe date si déjà présent."""
    proj = config.projects_path / "2025-01-15-old-project"
    proj.mkdir()
    dest = demote("old-project", config)
    assert dest.name == "2025-01-15-old-project"


def test_demote_raises_if_not_found(config: Config) -> None:
    """demote() lève FileNotFoundError si rien ne correspond."""
    with pytest.raises(FileNotFoundError):
        demote("nonexistent", config)


def test_demote_raises_if_destination_exists(config: Config) -> None:
    """demote() lève FileExistsError si la destination existe déjà."""
    today = date.today().isoformat()
    proj = config.projects_path / "my-project"
    proj.mkdir()
    (config.sandbox_path / f"{today}-my-project").mkdir()
    with pytest.raises(FileExistsError):
        demote("my-project", config)
