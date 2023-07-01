PROJECT_DIR := $(CURDIR)
DOCKER_DIR := "$(PROJECT_DIR)/docker"
TEST_WEB_SERVER_PORT := 8080

build_docker: generate_interactive_page
	docker build --tag kestrel:local "$(DOCKER_DIR)"

run_docker: build_docker
	docker run \
		--publish $(TEST_WEB_SERVER_PORT):80 \
		kestrel:local

generate_interactive_page: install_dependencies
	python src/kestrel.py --build-dir "$(DOCKER_DIR)"

install_dependencies:
	pip install --requirement requirements.txt

test: install_dependencies
	tests/smoke_test.bash

clean:
	rm --recursive --force build/* tests/build/*
