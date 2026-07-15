"""Regression tests for versioned release inputs."""

import re
from pathlib import Path

from scripts.check_release_consistency import release_versions


ROOT = Path(__file__).resolve().parents[1]


def test_release_versions_are_synchronized() -> None:
    versions = release_versions()
    assert len(set(versions.values())) == 1, versions


def test_semantic_release_refreshes_and_stages_lock_before_tagging() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'version_variables = ["src/openadapt_tray/__init__.py:__version__"]' in pyproject
    assert 'uv lock --upgrade-package "$PACKAGE_NAME"' in pyproject
    assert "git add uv.lock" in pyproject
    assert "uv build --wheel --sdist" in pyproject


def test_release_actions_are_pinned_to_commits() -> None:
    workflow = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
    uses = re.findall(r"^\s*uses:\s+\S+@([^\s#]+)", workflow, flags=re.MULTILINE)
    assert uses
    assert all(re.fullmatch(r"[0-9a-f]{40}", revision) for revision in uses)
