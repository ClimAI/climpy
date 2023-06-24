# Contributing Guide

## Development Setup

**Step 1: Clone the repository**

```
git clone https://github.com/ClimAI/climpy
```

**Step 2: Crete a dev environment and activate**

```
conda create -n climpy-dev python=3.11
conda activate climpy-dev
```

**Step 3: Add libgeos_dev**
```
conda install geos
```

**Step 4: Install poetry**
```
curl -sSL https://install.python-poetry.org | python3 -
```

**Step 5: Install dev dependencies**
```
poetry install
```

**Step 6: Install pre-commit**
```
pre-commit install
```
**Step 7: Check everything is setup correctly**
```
pytest --cov tests
```
> **_NOTE:_**  Remeber to change to the `issue` branch before contributing. No code can be pushed to main and develop.

## Structure of the package

### `transform` module

### `ml_data` module

### `metric` module


