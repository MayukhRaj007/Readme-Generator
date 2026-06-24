# README Generator

![Language](https://img.shields.io/badge/language-Python-3776AB?logo=python)  ![License](https://img.shields.io/badge/license-MIT-green)  ![Status](https://img.shields.io/badge/status-active-brightgreen)

CLI tool that generates a professional GitHub README.md from interactive prompts. No templates to edit — just answer questions and get a polished README instantly.

## Features

- Interactive prompt-driven workflow
- Auto-generates badges (language, license, status)
- Conditional sections — include only what you need
- Outputs clean Markdown ready for GitHub
- Preview mode — print to terminal before saving

## Installation

```bash
git clone https://github.com/mayukh/readme-generator.git
cd readme-generator
```

## Usage

```bash
  python readme_gen.py
  python readme_gen.py --output projects/MyApp/README.md
  python readme_gen.py --preview
```

## Tech Stack

- Python 3.8+
- argparse (stdlib)
- No external dependencies

## Running Tests

```bash
python -m pytest tests/
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

1. Fork the repo
2. Create your branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

## License

[MIT](LICENSE) © 2026 Mayukh

---

Part of my [50 GitHub Projects](https://github.com/mayukh) portfolio challenge.
