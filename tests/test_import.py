"""Premier test TDD : vérifie que le module s'importe correctement."""

import sandbox


def test_version_exists() -> None:
    """Le module expose un attribut __version__."""
    assert hasattr(sandbox, "__version__")
    assert isinstance(sandbox.__version__, str)
