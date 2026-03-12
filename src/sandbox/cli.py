"""Point d'entrée CLI de sandbox."""

from __future__ import annotations

import argparse
import sys

from sandbox.config import Config
from sandbox.core import Entry, Space, demote, find, graduate, ls, new

_SHELL_INIT = """\
# sandbox shell integration
# Source this in your .zshrc / .bashrc:
#   eval "$(sandbox init)"
sandbox() {{
    local cmd="${{1:-}}"
    if [[ "$cmd" == "new" || "$cmd" == "graduate" || "$cmd" == "demote" ]]; then
        local output
        output=$(command sandbox "$@")
        local exit_code=$?
        if [[ $exit_code -eq 0 && -d "$output" ]]; then
            echo "$output"
            cd "$output"
        else
            echo "$output" >&2
            return $exit_code
        fi
    else
        command sandbox "$@"
    fi
}}
"""


def _print_entries(entries: list[Entry]) -> None:
    for entry in entries:
        tag = "exp" if entry.space == Space.SANDBOX else "proj"
        print(f"[{tag}] {entry.path.name}")


def _handle_new(args: argparse.Namespace, config: Config) -> int:
    try:
        path = new(args.name, config)
        print(path)
        return 0
    except FileExistsError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def _handle_ls(args: argparse.Namespace, config: Config) -> int:
    query: str | None = getattr(args, "query", None)
    entries = ls(query=query, config=config)
    if not entries:
        print("No experiments found.")
        return 0
    _print_entries(entries)
    return 0


def _handle_graduate(args: argparse.Namespace, config: Config) -> int:
    try:
        path = graduate(args.name, config)
        print(path)
        return 0
    except (FileNotFoundError, FileExistsError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def _handle_demote(args: argparse.Namespace, config: Config) -> int:
    try:
        path = demote(args.name, config)
        print(path)
        return 0
    except (FileNotFoundError, FileExistsError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def _handle_find(args: argparse.Namespace, config: Config) -> int:
    results = find(args.query, config)
    if not results:
        print("No results.")
        return 0
    _print_entries(results)
    return 0


def _handle_init(_args: argparse.Namespace, _config: Config) -> int:
    print(_SHELL_INIT)
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sandbox",
        description="Gère le cycle de vie des expérimentations de développement.",
    )
    sub = parser.add_subparsers(dest="command", metavar="command")
    sub.required = True

    p_new = sub.add_parser("new", help="Créer une nouvelle expérimentation datée.")
    p_new.add_argument("name", help="Nom de l'expérimentation.")

    p_ls = sub.add_parser("ls", help="Lister les expérimentations.")
    p_ls.add_argument("query", nargs="?", default=None, help="Filtre optionnel.")

    p_grad = sub.add_parser("graduate", help="Promouvoir en projet.")
    p_grad.add_argument("name", help="Nom (ou sous-chaîne) de l'expérimentation.")

    p_demote = sub.add_parser(
        "demote", help="Rétrograder un projet en expérimentation."
    )
    p_demote.add_argument("name", help="Nom (ou sous-chaîne) du projet.")

    p_find = sub.add_parser("find", help="Chercher dans les deux espaces.")
    p_find.add_argument("query", help="Sous-chaîne à rechercher.")

    sub.add_parser("init", help="Afficher l'intégration shell.")

    return parser


_HANDLERS = {
    "new": _handle_new,
    "ls": _handle_ls,
    "graduate": _handle_graduate,
    "demote": _handle_demote,
    "find": _handle_find,
    "init": _handle_init,
}


def main() -> None:
    """Lancer sandbox."""
    parser = _build_parser()
    args = parser.parse_args()
    config = Config()
    handler = _HANDLERS[args.command]
    sys.exit(handler(args, config))
