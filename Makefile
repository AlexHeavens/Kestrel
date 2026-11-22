PROJECT_DIR := $(CURDIR)
DOCKER_DIR := "$(PROJECT_DIR)/docker"
HOST_WEB_SERVER_PORT := 8080

build_docker: generate_interactive_page
	docker build --tag kestrel:local "$(DOCKER_DIR)"

run_docker: build_docker
	docker run \
		--publish $(HOST_WEB_SERVER_PORT):8080 \
		kestrel:local

generate_interactive_page: install_dependencies
	python src/kestrel.py --build-dir "$(DOCKER_DIR)"

install_dependencies:
	pip install --requirement requirements.txt

install_dev_dependencies:
	pip install --requirement requirements-dev.txt

# Static checks. Run the same command locally and in CI.
lint: install_dev_dependencies
	actionlint
	shellcheck .githooks/pre-commit scripts/*.sh tests/*.bash
	black --check .
	isort --check .
	flake8 .

test: install_dependencies
	tests/smoke_test.bash

# Starts the real web server in the Docker image and fetches the page and the health endpoint.
e2e_test: build_docker
	tests/e2e_test.bash

clean:
	rm --recursive --force build/* tests/build/*
