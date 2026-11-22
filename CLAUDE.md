# Kestrel

- Run: `make run_docker` (needs a venv: `pip install --requirement requirements.txt` runs inside `make`).
- Test: `make lint test e2e_test`. All three run in CI.
- Docs: `README.md` for setup, `data/SOURCES.md` for data sources.
- Pin only direct dependencies in `requirements.txt`. Keep the CI job name `build-image-and-publish`: branch protection requires it.
- Before each commit, check the staged diff for secrets. The pre-commit hook needs `git config core.hooksPath .githooks`.
