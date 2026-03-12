# sandbox

> CLI pour gérer le cycle de vie des expérimentations de développement.

![CI](https://github.com/tomboulier/sandbox/actions/workflows/ci.yml/badge.svg)

## Installation

```bash
# Avec uv (recommandé)
uv tool install git+https://github.com/tomboulier/sandbox

# Avec pipx
pipx install git+https://github.com/tomboulier/sandbox

# Sans prérequis
curl -sSf https://raw.githubusercontent.com/tomboulier/sandbox/main/install.sh | sh
```

Ajoute ensuite à ton `.zshrc` / `.bashrc` :

```bash
eval "$(sandbox init)"
```

## Usage

```bash
sandbox new <nom>          # crée ~/src/sandbox/YYYY-MM-DD-<nom>/
sandbox ls [query]         # liste les expérimentations
sandbox graduate <nom>     # promeut en projet (sandbox -> projets)
sandbox demote <nom>       # rétrograde un projet en expérimentation
sandbox find <query>       # cherche dans les deux espaces
```

## Documentation

[tomboulier.github.io/sandbox](https://tomboulier.github.io/sandbox)

## Roadmap

- [x] Structure du projet, CI/CD, conventions
- [ ] `sandbox new <nom>` — créer une expérimentation datée
- [ ] `sandbox ls [query]` — lister les expérimentations
- [ ] `sandbox graduate <nom>` — promouvoir en projet
- [ ] `sandbox demote <nom>` — rétrograder un projet en expérimentation
- [ ] `sandbox find <query>` — chercher dans les deux espaces
- [ ] `sandbox init` — intégration shell (cd automatique)
- [ ] Skill Claude Code `/sandbox`
