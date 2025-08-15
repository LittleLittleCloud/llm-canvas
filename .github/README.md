# GitHub Actions CI/CD

This repository uses GitHub Actions for continuous integration and deployment.

## Workflows

### 🔄 Pull Request Validation (`pr.yml`)

Triggered on every pull request to `main` or `develop` branches:

- **Linting & Formatting**: Runs `ruff` check and format validation
- **Type Checking**: Runs `mypy` for static type analysis
- **Testing**: Runs pytest across Python 3.9-3.12
- **Frontend Build**: Builds the React frontend
- **Package Build**: Builds the Python package with frontend assets
- **Security Scan**: Runs safety check for known vulnerabilities

### 🚀 Release (`release.yml`)

Triggered on version tags (`v*.*.*`) or GitHub releases:

- **Testing**: Full test suite across Python versions
- **Build & Publish**: Builds and publishes to PyPI using trusted publishing
- **GitHub Release**: Creates GitHub release with auto-generated notes and artifacts

### 🔐 Security & Code Quality (`security.yml`)

Runs on pushes/PRs and weekly schedule:

- **Trivy Scanner**: Vulnerability scanning for dependencies and code
- **CodeQL Analysis**: Advanced semantic code analysis for Python and JavaScript
- **Dependency Review**: Reviews dependency changes in PRs

### 📦 Dependency Updates (`dependencies.yml`)

Weekly automated dependency updates:

- **Python Dependencies**: Updates `uv.lock` with latest compatible versions
- **Frontend Dependencies**: Updates npm packages and fixes audit issues
- **Auto PR Creation**: Creates pull requests for dependency updates

### 🏷️ Issue & PR Management (`issue-pr-management.yml`)

Automated repository management:

- **Auto-labeling**: Labels PRs based on changed files
- **Welcome Messages**: Greets new contributors
- **PR Size Labels**: Adds size labels (XS/S/M/L/XL/XXL) based on changes

## Setup Requirements

### PyPI Trusted Publishing

For releases to work, configure PyPI trusted publishing:

1. Go to [PyPI Trusted Publishers](https://pypi.org/manage/account/publishing/)
2. Add this repository with workflow: `release.yml`
3. Environment: leave blank (optional)

### GitHub Permissions

The workflows require these permissions (automatically granted):

- `contents: read/write` - For checking out code and creating releases
- `id-token: write` - For trusted publishing to PyPI
- `security-events: write` - For uploading security scan results
- `pull-requests: write` - For auto-labeling and comments
- `issues: write` - For welcome messages

## Manual Workflow Triggers

Some workflows can be triggered manually:

- **Dependency Updates**: Go to Actions → Update Dependencies → Run workflow
- **Security Scan**: Runs weekly but can be triggered manually

## Release Process

1. Update version in `pyproject.toml`
2. Create and push a git tag: `git tag v1.0.0 && git push origin v1.0.0`
3. The release workflow will automatically:
   - Run tests
   - Build the package (including frontend)
   - Publish to PyPI
   - Create GitHub release with artifacts

## Development

The CI ensures code quality through:

- **Ruff**: Fast Python linter and formatter
- **MyPy**: Static type checking
- **Pytest**: Unit and integration tests
- **Safety**: Security vulnerability scanning
- **CodeQL**: Advanced security analysis
