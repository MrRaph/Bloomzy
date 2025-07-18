import os
import tempfile
import subprocess
import pytest

DB_PATH = "/data/bloomzy.db"

@pytest.fixture
def temp_db(monkeypatch):
    # Utilise un fichier temporaire pour simuler la DB
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        monkeypatch.setenv("SQLALCHEMY_DATABASE_URI", f"sqlite:///{tmp.name}")
        yield tmp.name


def test_db_init_when_missing(tmp_path, monkeypatch):
    db_path = tmp_path / "bloomzy.db"
    monkeypatch.setenv("SQLALCHEMY_DATABASE_URI", f"sqlite:///{db_path}")
    # Simule l'absence de la DB
    assert not db_path.exists()
    # Lance le script entrypoint.sh
    result = subprocess.run([
        "sh", "entrypoint.sh", "echo", "test"
    ], capture_output=True, text=True)
    assert "Initialisation de la base de données" in result.stdout
    # La DB doit être créée
    assert db_path.exists() or "Base de données initialisée" in result.stdout


def test_db_no_init_if_exists(tmp_path, monkeypatch):
    db_path = tmp_path / "bloomzy.db"
    db_path.write_text("")  # Crée un fichier vide
    monkeypatch.setenv("SQLALCHEMY_DATABASE_URI", f"sqlite:///{db_path}")
    assert db_path.exists()
    result = subprocess.run([
        "sh", "entrypoint.sh", "echo", "test"
    ], capture_output=True, text=True)
    assert "pas d'initialisation nécessaire" in result.stdout
