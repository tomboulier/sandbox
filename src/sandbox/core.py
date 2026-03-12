"""Opérations principales de sandbox."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from enum import Enum
from pathlib import Path

from sandbox.config import Config


class Space(Enum):
    """Espace auquel appartient une entrée."""

    SANDBOX = "sandbox"
    PROJECT = "project"


@dataclass
class Entry:
    """Une entrée (expérimentation ou projet).

    Parameters
    ----------
    path : Path
        Chemin absolu du répertoire.
    space : Space
        Espace d'appartenance.
    """

    path: Path
    space: Space


def _slugify(name: str) -> str:
    """Convertit un nom en slug (minuscules, tirets)."""
    slug = name.lower().strip()
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"[^\w-]", "", slug)
    return slug


def new(name: str, config: Config) -> Path:
    """Crée une nouvelle expérimentation datée.

    Parameters
    ----------
    name : str
        Nom de l'expérimentation (sera slugifié).
    config : Config
        Configuration sandbox.

    Returns
    -------
    Path
        Chemin du répertoire créé.

    Raises
    ------
    FileExistsError
        Si un répertoire avec ce nom existe déjà aujourd'hui.
    """
    today = date.today().isoformat()
    slug = _slugify(name)
    target = config.sandbox_path / f"{today}-{slug}"
    if target.exists():
        raise FileExistsError(f"Already exists: {target}")
    target.mkdir(parents=True)
    return target


def ls(query: str | None = None, *, config: Config) -> list[Entry]:
    """Liste les expérimentations, triées par date de modification décroissante.

    Parameters
    ----------
    query : str, optional
        Filtre par sous-chaîne sur le nom du répertoire.
    config : Config
        Configuration sandbox.

    Returns
    -------
    list[Entry]
        Expérimentations correspondantes.
    """
    dirs = sorted(
        (p for p in config.sandbox_path.iterdir() if p.is_dir()),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    entries = [Entry(path=p, space=Space.SANDBOX) for p in dirs]
    if query:
        entries = [e for e in entries if query.lower() in e.path.name.lower()]
    return entries


def find(query: str, config: Config) -> list[Entry]:
    """Cherche dans les deux espaces (sandbox et projets).

    Parameters
    ----------
    query : str
        Sous-chaîne à rechercher dans les noms de répertoires.
    config : Config
        Configuration sandbox.

    Returns
    -------
    list[Entry]
        Résultats depuis les deux espaces.
    """
    results: list[Entry] = []
    for path in config.sandbox_path.iterdir():
        if path.is_dir() and query.lower() in path.name.lower():
            results.append(Entry(path=path, space=Space.SANDBOX))
    for path in config.projects_path.iterdir():
        if path.is_dir() and query.lower() in path.name.lower():
            results.append(Entry(path=path, space=Space.PROJECT))
    return results


def graduate(name: str, config: Config) -> Path:
    """Promeut une expérimentation en projet.

    Parameters
    ----------
    name : str
        Sous-chaîne identifiant l'expérimentation dans sandbox.
    config : Config
        Configuration sandbox.

    Returns
    -------
    Path
        Chemin de destination dans projects.

    Raises
    ------
    FileNotFoundError
        Si aucune expérimentation ne correspond.
    FileExistsError
        Si la destination existe déjà dans projects.
    """
    source = _find_unique(name, config.sandbox_path)
    dest = config.projects_path / source.name
    if dest.exists():
        raise FileExistsError(f"Already exists in projects: {dest}")
    source.rename(dest)
    return dest


def demote(name: str, config: Config) -> Path:
    """Rétrograde un projet en expérimentation.

    Parameters
    ----------
    name : str
        Sous-chaîne identifiant le projet dans projects.
    config : Config
        Configuration sandbox.

    Returns
    -------
    Path
        Chemin de destination dans sandbox.

    Raises
    ------
    FileNotFoundError
        Si aucun projet ne correspond.
    FileExistsError
        Si la destination existe déjà dans sandbox.
    """
    source = _find_unique(name, config.projects_path)
    dest_name = source.name
    if not re.match(r"^\d{4}-\d{2}-\d{2}-", dest_name):
        today = date.today().isoformat()
        dest_name = f"{today}-{dest_name}"
    dest = config.sandbox_path / dest_name
    if dest.exists():
        raise FileExistsError(f"Already exists in sandbox: {dest}")
    source.rename(dest)
    return dest


def _find_unique(query: str, directory: Path) -> Path:
    """Trouve un répertoire unique correspondant à query dans directory.

    Raises
    ------
    FileNotFoundError
        Si aucun répertoire ne correspond.
    """
    matches = [
        p for p in directory.iterdir() if p.is_dir() and query.lower() in p.name.lower()
    ]
    if not matches:
        raise FileNotFoundError(f"No match for '{query}' in {directory}")
    # Préférer la correspondance exacte, sinon la plus récente
    exact = [m for m in matches if m.name.lower() == query.lower()]
    if exact:
        return exact[0]
    return sorted(matches, key=lambda p: p.stat().st_mtime, reverse=True)[0]
