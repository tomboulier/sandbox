"""Tests pour sandbox.core."""

from __future__ import annotations

import os
from datetime import date
from pathlib import Path

import pytest

from sandbox.config import Config
from sandbox.core import Space, find, ls, new


@pytest.fixture
def config(tmp_path: Path) -> Config:
    """Config pointant vers des répertoires temporaires."""
    sandbox_dir = tmp_path / "experiments"
    projects_dir = tmp_path / "projects"
    sandbox_dir.mkdir()
    projects_dir.mkdir()
    return Config(sandbox_path=sandbox_dir, projects_path=projects_dir)


# ---------------------------------------------------------------------------
# new
# ---------------------------------------------------------------------------


def test_new_creates_dated_directory(config: Config) -> None:
    """new() crée un répertoire préfixé par la date du jour."""
    path = new("redis", config)
    today = date.today().isoformat()
    assert path.name == f"{today}-redis"
    assert path.is_dir()
    assert path.parent == config.sandbox_path


def test_new_slugifies_name(config: Config) -> None:
    """new() convertit les espaces en tirets et met en minuscules."""
    path = new("Mon Super Projet", config)
    today = date.today().isoformat()
    assert path.name == f"{today}-mon-super-projet"


def test_new_raises_if_already_exists(config: Config) -> None:
    """new() lève une erreur si le répertoire existe déjà."""
    new("redis", config)
    with pytest.raises(FileExistsError):
        new("redis", config)


# ---------------------------------------------------------------------------
# ls
# ---------------------------------------------------------------------------


def test_ls_returns_all_experiments(config: Config) -> None:
    """ls() liste toutes les expérimentations."""
    new("alpha", config)
    new("beta", config)
    entries = ls(config=config)
    names = [e.path.name for e in entries]
    assert any("alpha" in n for n in names)
    assert any("beta" in n for n in names)


def test_ls_filters_by_query(config: Config) -> None:
    """ls() filtre par sous-chaîne si query est fourni."""
    new("redis-server", config)
    new("postgres", config)
    entries = ls(query="redis", config=config)
    assert len(entries) == 1
    assert "redis" in entries[0].path.name


def test_ls_returns_empty_when_no_experiments(config: Config) -> None:
    """ls() retourne une liste vide si aucune expérimentation n'existe."""
    assert ls(config=config) == []


def test_ls_sorts_by_most_recent(config: Config, tmp_path: Path) -> None:
    """ls() trie par date de modification décroissante."""
    old = config.sandbox_path / "2024-01-01-old"
    old.mkdir()
    os.utime(old, (0, 0))  # force mtime à l'époque Unix (très ancien)
    new("recent", config)
    entries = ls(config=config)
    assert "recent" in entries[0].path.name


# ---------------------------------------------------------------------------
# find
# ---------------------------------------------------------------------------


def test_find_searches_in_both_spaces(config: Config) -> None:
    """find() retourne des résultats depuis sandbox et projects."""
    new("redis-exp", config)
    (config.projects_path / "redis-prod").mkdir()

    results = find("redis", config)
    spaces = {r.space for r in results}
    assert Space.SANDBOX in spaces
    assert Space.PROJECT in spaces


def test_find_no_results(config: Config) -> None:
    """find() retourne une liste vide si rien ne correspond."""
    assert find("nonexistent", config) == []
