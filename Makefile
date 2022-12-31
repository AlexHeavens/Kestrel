generate_interactive_page: install_dependencies
	python src/obscura.py

install_dependencies:
	pip install --requirement requirements.txt

test: install_dependencies
	./tests/smoke_test.bash

clean:
	rm --recursive --force build/* tests/build/*
