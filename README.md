# Kestrel

Kestrel generates an interactive map of Edinburgh. Each council ward is coloured by the party that won the most votes in the 2022 council election. Hover over a ward to see its results. A small nginx image serves the generated page.

It is not a general election-results tool. It covers Edinburgh and the 2022 results only.

## Contents

- `src`: Python code that reads the data and writes the map (`src/kestrel.py` is the entry point).
- `data`: Input data and its [sources](data/SOURCES.md).
- `docker`: Dockerfile and nginx config that serve the generated `index.html` on port 8080, with a `/health` endpoint.
- `tests`: `smoke_test.bash` (the map builds) and `e2e_test.bash` (the image serves the map).
- `pins`, `scripts`, `.githooks`: pinned gitleaks and the pre-commit secret scan.
- `.github`: CI (`test-and-publish.yaml`, `gitleaks.yml`) and Dependabot.

## Setup

Prerequisites: Python 3.14, Docker, curl, and Chrome or Chromium (kaleido 1.x needs it to render the pie charts).

```
python3 -m venv venv
. venv/bin/activate
scripts/install-gitleaks.sh        # the pre-commit hook needs gitleaks
git config core.hooksPath .githooks
make run_docker                    # builds the map and image, serves http://localhost:8080
```

Run `make clean` to remove build artefacts.

## Tests

```
make lint          # actionlint, ShellCheck, black, isort, flake8
make test          # smoke test: builds the map
make e2e_test      # builds the image, starts it, fetches / and /health
```

CI runs all three on every push and pull request. On `main` it also pushes the image to Amazon ECR.
