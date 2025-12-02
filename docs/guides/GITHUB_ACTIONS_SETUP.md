# 🤖 GitHub Actions Setup Guide

This guide explains how to set up and customize the automated CI/CD pipelines for this project.

## 📋 Overview

We use GitHub Actions to automate:
1. **Continuous Integration (CI)**: Testing, linting, and type checking on every push.
2. **Continuous Deployment (CD)**: Automated releases when a version tag is pushed.

## 🛠️ Workflows

### 1. CI Workflow (`.github/workflows/ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull Requests to `main` or `develop`

**Jobs:**
- **Linting**: Checks code style with `flake8` and `black`
- **Type Checking**: Verifies types with `mypy`
- **Testing**: Runs `pytest` across Python 3.8 - 3.12
- **Coverage**: Uploads reports to Codecov

### 2. Release Workflow (`.github/workflows/release.yml`)

**Triggers:**
- Push of any tag starting with `v` (e.g., `v1.0.0`)

**Jobs:**
- **Build**: Creates source distribution and wheel
- **Publish**: Uploads to PyPI (requires secret)
- **Release**: Creates a GitHub Release with auto-generated notes

## ⚙️ Configuration

### Required Secrets

To enable full functionality, add these secrets in your GitHub repository settings (`Settings > Secrets and variables > Actions`):

| Secret Name | Description | Required For |
|-------------|-------------|--------------|
| `CODECOV_TOKEN` | Token from Codecov.io | Coverage reporting |
| `PYPI_API_TOKEN` | API token from PyPI | Publishing to PyPI |

### Customizing Triggers

To change when workflows run, edit the `on:` section in the YAML files:

```yaml
on:
  push:
    branches: [ "main" ]  # Only run on main
  schedule:
    - cron: '0 0 * * 0'   # Run weekly on Sunday
```

## 🐛 Troubleshooting

### Workflow Failed?

1. Go to the **Actions** tab in your repository.
2. Click on the failed run.
3. Click on the failed job (e.g., `test (3.10)`).
4. Expand the failed step to see the error log.

### Common Issues

- **Linting Errors**: Run `black .` and `flake8 .` locally to fix.
- **Test Failures**: Run `pytest` locally to debug.
- **Missing Secrets**: Ensure secrets are added in GitHub settings.

---

## 🔗 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python in GitHub Actions](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
