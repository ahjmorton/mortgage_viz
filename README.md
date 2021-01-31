This repository describes the process of purchasing a property for first time buyers. It's assumed you're buying a property requiring a mortgage.

The `mortgage_viz.py` script outputs a [Graphviz](https://graphviz.org) diagram that can be turned into an image.

# Requirements

- Python 3
- [Graphiviz](https://graphviz.org)
- `make`
- `fswatch` (Optional)

# Building
Running `make` will produce a `build` directory containing the image.

Running `make watch` will watch for changes of the `mortgage_viz.py` script and automatically re-build the image.
