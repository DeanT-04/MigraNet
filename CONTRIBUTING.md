# Contributing to Migraine Network Analysis

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to this project. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## 🚀 Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/migraine-network-analysis.git
   cd migraine-network-analysis
   ```
3. **Set up the environment**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   pre-commit install
   ```
4. **Create a branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/amazing-feature
   ```

## 🧪 Running Tests

We use `pytest` for testing. Ensure all tests pass before submitting:

```bash
pytest
```

To run tests with coverage:
```bash
pytest --cov=english_version/scripts
```

## 🎨 Code Style

We use `black` for formatting and `flake8` for linting.
Run the following before committing:

```bash
black .
flake8 .
mypy .
```

Better yet, let `pre-commit` handle it for you automatically!

## 📝 Pull Request Process

1. Update the `README.md` with details of changes to the interface, if applicable.
2. Update `CHANGELOG.md` with a note about your change.
3. The PR title should follow [Conventional Commits](https://www.conventionalcommits.org/) format.
4. Ensure the CI build passes.

## 🐛 Reporting Bugs

Open a new issue and include:
- A clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)

## 💡 Suggesting Enhancements

Open a new issue and include:
- A clear title and description
- Why this enhancement would be useful
- Any implementation ideas

Thank you for contributing! ❤️
