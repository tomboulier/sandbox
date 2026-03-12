#!/usr/bin/env sh
set -e

REPO="tomboulier/sandbox"

echo "Installation de sandbox..."

# Option 1 : uv tool install (recommandé)
if command -v uv >/dev/null 2>&1; then
    echo "uv détecté, installation via uv tool install..."
    uv tool install "git+https://github.com/$REPO"
    echo ""
    echo "sandbox installé. Ajoute ceci à ton .zshrc / .bashrc :"
    echo '  eval "$(sandbox init)"'
    exit 0
fi

# Option 2 : pipx
if command -v pipx >/dev/null 2>&1; then
    echo "pipx détecté, installation via pipx..."
    pipx install "git+https://github.com/$REPO"
    echo ""
    echo "sandbox installé. Ajoute ceci à ton .zshrc / .bashrc :"
    echo '  eval "$(sandbox init)"'
    exit 0
fi

# Option 3 : pip dans un venv dédié
echo "Ni uv ni pipx trouvé, installation via pip dans ~/.local/sandbox-venv..."
python3 -m venv "$HOME/.local/sandbox-venv"
"$HOME/.local/sandbox-venv/bin/pip" install --quiet "git+https://github.com/$REPO"
ln -sf "$HOME/.local/sandbox-venv/bin/sandbox" "$HOME/.local/bin/sandbox"

echo ""
echo "sandbox installé dans ~/.local/bin/sandbox"
echo "Ajoute ceci à ton .zshrc / .bashrc :"
echo '  eval "$(sandbox init)"'
