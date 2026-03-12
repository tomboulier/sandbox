"""Configuration de sandbox, chargée depuis les variables d'environnement."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


def _env_path(var: str, default: Path) -> Path:
    """Lit une variable d'environnement comme Path, avec expansion de ~."""
    raw = os.environ.get(var)
    if raw is None:
        return default
    return Path(raw).expanduser()


@dataclass
class Config:
    """Chemins de configuration de sandbox.

    Parameters
    ----------
    sandbox_path : Path
        Répertoire des expérimentations. Surchargeable via ``SANDBOX_PATH``.
    projects_path : Path
        Répertoire des projets. Surchargeable via ``SANDBOX_PROJECTS_PATH``.
    """

    sandbox_path: Path = field(
        default_factory=lambda: _env_path(
            "SANDBOX_PATH",
            Path.home() / "Documents/03-Ressources/Expérimentations",
        )
    )
    projects_path: Path = field(
        default_factory=lambda: _env_path(
            "SANDBOX_PROJECTS_PATH",
            Path.home() / "Documents/01-Projets",
        )
    )
