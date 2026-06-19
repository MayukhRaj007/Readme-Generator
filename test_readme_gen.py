"""
Tests for readme_gen.py
Run: python -m pytest tests/ -v
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import readme_gen as rg


# ── Shared test data ──────────────────────────────────

SAMPLE = {
    "project_name": "Awesome CLI",
    "repo_name": "awesome-cli",
    "github_user": "mayukh",
    "description": "A tool that does awesome things.",
    "language": "Python",
    "author": "Mayukh",
    "features": ["Add items", "Delete items", "List items"],
    "usage_examples": ["python app.py add Task", "python app.py list"],
    "tech_stack": ["Python 3.11", "argparse", "JSON"],
    "install_cmd": "pip install -r requirements.txt",
    "test_cmd": "python -m pytest tests/",
    "include_contributing": True,
    "include_license": True,
    "include_footer": True,
}


# ── Badge tests ───────────────────────────────────────

def test_badge_python_language():
    result = rg.build_badges({"language": "Python"})
    assert "Python" in result
    assert "3776AB" in result  # Python's official blue

def test_badge_always_includes_license():
    result = rg.build_badges({})
    assert "license" in result
    assert "MIT" in result

def test_badge_always_includes_status():
    result = rg.build_badges({})
    assert "status" in result


# ── Section tests ─────────────────────────────────────

def test_features_section_renders_all_items():
    result = rg.build_features(["Feature A", "Feature B", "Feature C"])
    assert "Feature A" in result
    assert "Feature B" in result
    assert "## Features" in result

def test_features_empty_returns_empty_string():
    assert rg.build_features([]) == ""

def test_usage_section_renders_examples():
    result = rg.build_usage(["python app.py run", "python app.py --help"])
    assert "python app.py run" in result
    assert "## Usage" in result

def test_usage_empty_returns_empty_string():
    assert rg.build_usage([]) == ""

def test_tech_stack_renders_items():
    result = rg.build_tech_stack(["Python 3.11", "FastAPI"])
    assert "Python 3.11" in result
    assert "FastAPI" in result

def test_tech_stack_empty_returns_empty_string():
    assert rg.build_tech_stack([]) == ""

def test_tests_section_renders_command():
    result = rg.build_tests("python -m pytest tests/")
    assert "pytest" in result
    assert "## Running Tests" in result

def test_tests_empty_returns_empty_string():
    assert rg.build_tests("") == ""

def test_license_includes_author_and_year():
    result = rg.build_license("Mayukh")
    assert "Mayukh" in result
    assert "MIT" in result

def test_footer_includes_github_user():
    result = rg.build_portfolio_footer("mayukh")
    assert "mayukh" in result
    assert "50 GitHub Projects" in result


# ── Full README generation ────────────────────────────

def test_generate_readme_contains_project_name():
    result = rg.generate_readme(SAMPLE)
    assert "# Awesome CLI" in result

def test_generate_readme_contains_description():
    result = rg.generate_readme(SAMPLE)
    assert "A tool that does awesome things." in result

def test_generate_readme_contains_all_features():
    result = rg.generate_readme(SAMPLE)
    for feature in SAMPLE["features"]:
        assert feature in result

def test_generate_readme_contains_tech_stack():
    result = rg.generate_readme(SAMPLE)
    for tech in SAMPLE["tech_stack"]:
        assert tech in result

def test_generate_readme_includes_contributing_when_true():
    result = rg.generate_readme({**SAMPLE, "include_contributing": True})
    assert "Contributing" in result

def test_generate_readme_excludes_contributing_when_false():
    result = rg.generate_readme({**SAMPLE, "include_contributing": False})
    assert "Contributing" not in result

def test_generate_readme_includes_license_when_true():
    result = rg.generate_readme({**SAMPLE, "include_license": True})
    assert "License" in result

def test_generate_readme_excludes_license_when_false():
    # The badge always shows "license" — we check the *section heading* is absent
    result = rg.generate_readme({**SAMPLE, "include_license": False})
    assert "## License" not in result

def test_generate_readme_includes_footer_when_true():
    result = rg.generate_readme({**SAMPLE, "include_footer": True})
    assert "50 GitHub Projects" in result

def test_generate_readme_ends_with_newline():
    result = rg.generate_readme(SAMPLE)
    assert result.endswith("\n")


# ── Helper function tests ─────────────────────────────

def test_ask_list_parses_comma_separated(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Python, FastAPI, SQLite")
    result = rg.ask_list("Tech stack")
    assert result == ["Python", "FastAPI", "SQLite"]

def test_ask_list_returns_empty_on_blank(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")
    result = rg.ask_list("Tech stack")
    assert result == []

def test_ask_yn_yes(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert rg.ask_yn("Include?") is True

def test_ask_yn_no(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert rg.ask_yn("Include?") is False

def test_ask_yn_default_yes(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert rg.ask_yn("Include?", default="y") is True
