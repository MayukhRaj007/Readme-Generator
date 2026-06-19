"""
README Generator
----------------
Run:  python readme_gen.py
      python readme_gen.py --output MY_PROJECT/README.md
"""

import argparse
import os
from datetime import datetime


# ─────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────

def ask(prompt, default=""):
    """Ask a question; return default silently if user hits Enter."""
    suffix = f" [{default}]" if default else ""
    answer = input(f"{prompt}{suffix}: ").strip()
    return answer if answer else default


def ask_list(prompt, example=""):
    """Collect a comma-separated list, return as Python list."""
    hint = f" (comma-separated, e.g. {example})" if example else " (comma-separated)"
    raw = input(f"{prompt}{hint}: ").strip()
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def ask_yn(prompt, default="y"):
    """Yes/no question. Returns True for yes."""
    suffix = " [Y/n]" if default == "y" else " [y/N]"
    answer = input(f"{prompt}{suffix}: ").strip().lower()
    if not answer:
        return default == "y"
    return answer in ("y", "yes")


def badge(label, value, color="blue"):
    """Generate a shields.io badge in Markdown."""
    label_enc = label.replace(" ", "_").replace("-", "--")
    value_enc = value.replace(" ", "_").replace("-", "--")
    return f"![{label}](https://img.shields.io/badge/{label_enc}-{value_enc}-{color})"


# ─────────────────────────────────────────
#  Section builders
# ─────────────────────────────────────────

def build_badges(data):
    badges = []
    if data.get("language"):
        lang = data["language"]
        color_map = {
            "Python": "3776AB", "JavaScript": "F7DF1E",
            "TypeScript": "3178C6", "HTML": "E34F26",
            "Rust": "000000", "Go": "00ADD8",
        }
        color = color_map.get(lang, "blue")
        badges.append(f"![Language](https://img.shields.io/badge/language-{lang}-{color}?logo={lang.lower()})")
    badges.append("![License](https://img.shields.io/badge/license-MIT-green)")
    badges.append("![Status](https://img.shields.io/badge/status-active-brightgreen)")
    return "  ".join(badges)


def build_features(features):
    if not features:
        return ""
    lines = "\n".join(f"- {f}" for f in features)
    return f"""
## Features

{lines}
"""


def build_installation(data):
    lang = data.get("language", "Python")
    repo = data.get("repo_name", "your-repo")
    install_cmd = data.get("install_cmd", "")

    clone_block = f"""```bash
git clone https://github.com/{data.get('github_user', 'YOUR_USERNAME')}/{repo}.git
cd {repo}
```"""

    install_block = ""
    if install_cmd:
        install_block = f"""
Install dependencies:

```bash
{install_cmd}
```"""

    return f"""
## Installation

{clone_block}{install_block}
"""


def build_usage(usage_examples):
    if not usage_examples:
        return ""
    examples = "\n".join(f"  {ex}" for ex in usage_examples)
    return f"""
## Usage

```bash
{examples}
```
"""


def build_tech_stack(stack):
    if not stack:
        return ""
    lines = "\n".join(f"- {t}" for t in stack)
    return f"""
## Tech Stack

{lines}
"""


def build_tests(test_cmd):
    if not test_cmd:
        return ""
    return f"""
## Running Tests

```bash
{test_cmd}
```
"""


def build_contributing(repo_name, github_user):
    return f"""
## Contributing

Pull requests are welcome. For major changes, please open an issue first.

1. Fork the repo
2. Create your branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request
"""


def build_license(author):
    year = datetime.now().year
    return f"""
## License

[MIT](LICENSE) © {year} {author}
"""


def build_portfolio_footer(github_user):
    return f"""
---

Part of my [50 GitHub Projects](https://github.com/{github_user}) portfolio challenge.
"""


# ─────────────────────────────────────────
#  Template assembler
# ─────────────────────────────────────────

def generate_readme(data):
    """Assemble all sections into a final README string."""

    badges = build_badges(data)
    features = build_features(data.get("features", []))
    installation = build_installation(data)
    usage = build_usage(data.get("usage_examples", []))
    tech_stack = build_tech_stack(data.get("tech_stack", []))
    tests = build_tests(data.get("test_cmd", ""))
    contributing = build_contributing(data["repo_name"], data["github_user"]) if data.get("include_contributing") else ""
    license_section = build_license(data.get("author", "")) if data.get("include_license") else ""
    footer = build_portfolio_footer(data["github_user"]) if data.get("include_footer") else ""

    readme = f"""# {data['project_name']}

{badges}

{data['description']}
{features}{installation}{usage}{tech_stack}{tests}{contributing}{license_section}{footer}"""

    return readme.strip() + "\n"


# ─────────────────────────────────────────
#  Interview (collect all data)
# ─────────────────────────────────────────

def run_interview():
    """Walk the user through all prompts. Returns a data dict."""

    print("\n" + "═" * 50)
    print("  🛠️  README Generator")
    print("  Answer the prompts. Press Enter to skip optional ones.")
    print("═" * 50 + "\n")

    data = {}

    # Core
    data["project_name"]  = ask("Project name", "My Awesome Project")
    data["repo_name"]     = ask("GitHub repo name (slug)", data["project_name"].lower().replace(" ", "-"))
    data["github_user"]   = ask("Your GitHub username")
    data["description"]   = ask("One-line description", "A Python project built to solve a real problem.")
    data["language"]      = ask("Primary language", "Python")
    data["author"]        = ask("Your name (for license)", data["github_user"])

    print()

    # Features
    data["features"] = ask_list(
        "Key features",
        "Add tasks, List tasks, Delete tasks"
    )

    # Usage examples
    print("\n  Usage examples — type each command on one line, comma-separated")
    raw_usage = ask_list(
        "Usage examples",
        'python app.py run, python app.py --help'
    )
    data["usage_examples"] = raw_usage

    # Tech stack
    data["tech_stack"] = ask_list(
        "Tech stack",
        "Python 3.11, FastAPI, SQLite"
    )

    # Install command
    data["install_cmd"] = ask(
        "Install command (optional)",
        "pip install -r requirements.txt"
    )

    # Test command
    data["test_cmd"] = ask("Test command (optional)", "python -m pytest tests/")

    print()

    # Optional sections
    data["include_contributing"] = ask_yn("Include Contributing section?")
    data["include_license"]      = ask_yn("Include MIT License section?")
    data["include_footer"]       = ask_yn("Include portfolio footer?")

    print()
    return data


# ─────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate a GitHub README.md from prompts")
    parser.add_argument(
        "--output", "-o",
        default="README.md",
        help="Output file path (default: README.md)"
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Print the README to terminal instead of saving"
    )
    args = parser.parse_args()

    data = run_interview()
    readme = generate_readme(data)

    if args.preview:
        print("\n" + "─" * 50)
        print(readme)
        print("─" * 50)
        print("\n👀 Preview mode — file not saved. Remove --preview to save.")
        return

    # Ensure output directory exists
    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(readme)

    print(f"✅ README saved to: {args.output}")
    print(f"   Characters : {len(readme)}")
    print(f"   Lines      : {readme.count(chr(10))}")
    print("\n💡 Next step: copy this file into your GitHub repo and commit it.")


if __name__ == "__main__":
    main()
