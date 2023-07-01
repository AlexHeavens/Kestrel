# Kestrel

Welcome to the Kestrel repository, a tool for visualizing electoral results in Edinburgh, Scotland.

This tool generates an interactive map of the city, with each council ward colored according to the party that won the most votes in the 2022 Council Election. By hovering over each ward, you can see detailed information about the election results in that area.

## Contents

- `data`: Input data and a list of [sources](data/SOURCES.md).
- `src`: Source code for processing and generating the final map.
- `tests`: Test scripts.
- `docker`: Packaging as a web server.

## Setting Up For Development

It is recommended to use a virtual environment with Python 3.11.

You can build and run a local copy of the web server:

```
python3.11 -m venv venv
. ./venv/bin/activate

pre-commit run --all-files &&
make test &&

make run_docker
```
Then open  http://localhost:8080 in a web browser


You can clean all build artifacts with:

```
make clean
```

## Publishing Site
A docker image `kestrel:local` can be generated by running:
```
python3.11 -m venv venv
. ./venv/bin/activate

make
```