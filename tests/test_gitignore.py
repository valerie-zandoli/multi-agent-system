"""Model-free check that the "never commit keys" rule in AGENTS.md is enforced by code.

This repository is public, so key files and .env files must never be tracked.
"""
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent

MUST_BE_IGNORED = [
    ".env",
    ".env.local",
    ".env.production",
    "agents/.env",
    "server.pem",
    "api.key",
    "token.json",
    "credentials.json",
]
MUST_STAY_TRACKED = [".env.example"]


def git(*args, repo=REPO):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)


def is_ignored(path, repo=REPO):
    result = git("check-ignore", "-q", path, repo=repo)
    assert result.returncode in (0, 1), result.stderr
    return result.returncode == 0


@pytest.mark.parametrize("path", MUST_BE_IGNORED)
def test_secret_paths_are_ignored(path):
    assert is_ignored(path), f"{path} is not ignored; add it to .gitignore"


@pytest.mark.parametrize("path", MUST_STAY_TRACKED)
def test_example_env_file_stays_trackable(path):
    assert not is_ignored(path), f"{path} must stay trackable so setup steps can name it"


def test_no_secret_file_is_tracked():
    result = git("ls-files")
    assert result.returncode == 0, result.stderr
    tracked = result.stdout.splitlines()
    secret_suffixes = (".pem", ".key")
    secret_names = {".env", "token.json", "credentials.json"}
    bad = [
        name
        for name in tracked
        if Path(name).name in secret_names
        or (Path(name).name.startswith(".env.") and Path(name).name != ".env.example")
        or name.endswith(secret_suffixes)
    ]
    assert not bad, f"secret files are tracked: {bad}"
