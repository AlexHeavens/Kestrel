# Camera Obscura

Welcome to the Camera Obscura repository, a tool for visualizing electoral results in Edinburgh, Scotland.

This tool generates an interactive map of the city, with each council ward colored according to the party that won the most votes in the 2022 Council Election. By hovering over each ward, you can see detailed information about the election results in that area.

## Contents

- `data`: Input data and a list of [sources](data/SOURCES.md).
- `src`: Source code for processing and generating the final map.
- `build`: Intermediate results and the final map.
- `tests`: Test scripts.

## Setting Up For Development

It is recommended to use a virtual environment with Python 3.11.

```
python3.11 -m venv venv
. ./venv/bin/activate

make &&
google-chrome build/obscura.html
```

You can clean all build artifacts with:

```
make clean
```

## Publishing Site
Simply running `make` will generate the site in the `build` directory.

For simplicity's sake, this must be manually run with changes until CI is adapted.
