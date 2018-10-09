# Contributing

We follow the [IPython Contributing Guide](https://github.com/ipython/ipython/blob/master/CONTRIBUTING.md).

## To set up a development environment

Fork the repository and clone the forked repository locally.

Use Conda to install dependencies and activate the development environment.

```
    conda create -n qtdev python=3
    conda activate qtdev
    conda install pyqt
```
Setup **qtconsole** to run on the development environment:

```
  python setup.py develop
```

To run after the changes have been made to source:
```
  pip install -e .
```

Running the tests:

```
nosetests
```
