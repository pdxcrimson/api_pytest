# api-pytest

A robust API testing framework built with Pytest, Requests, and JSON Schema validation.

## Prerequisites

This project uses **uv** for extremely fast dependency management and Python version control. You do not need to have a specific Python version pre-installed; `uv` will handle it for you.

### Install uv
- **macOS/Linux**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Windows**: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pdxcrimson/api_pytest.git
   cd api-pytest
2. **Initialize the environment**:
   uv sync
   _This command creates a `.venv`, installs Python >=3.10, and syncs all dependencies (pytest, requests, jsonschema, etc.) to your local machine._
### Running Tests
   You can run the tests using `uv run`, which ensures the project's virtual environment is used automatically:
### Run all tests
```uv run pytest```
# Run with verbose output
```uv run pytest -v```
# Run individual tests
```uv run pytest <path> ...```
