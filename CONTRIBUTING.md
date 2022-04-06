# Developers Guide

## How to run

### Compiling TypeScript files

Node.js v16 is required to compile TypeScript files.

```
$ npm install
$ npm run build:dev
```

<details>
<summary>Watch for files changes</summary>

```
$ npm run watch
```

</details>

<details>
<summary>Production builds</summary>

```
$ npm run build:prd
```

</details>

### Building a Docker image

```
$ docker build -t optuna-dashboard .
```

When failed above command due to the out of heap memory error (Exit code: 137), please check "Resources" tab on your Docker engine's preference since it requires a lot of memory to compile TypeScript files.
You can use the Docker image like below:

```
# SQLite3
$ docker run -it --rm -p 8080:8080 -v `PWD`:/app -w /app sqlite:///db.sqlite3
```

### Running dashboard server

```
$ pip install -e .
$ optuna-dashboard sqlite:///db.sqlite3
```

<details>

<summary>Environment variables for development</summary>

If you set `OPTUNA_DASHBOARD_DEBUG=1`, the server will automatically restart when the source codes are changed.

```
$ OPTUNA_DASHBOARD_DEBUG=1 optuna-dashboard sqlite:///db.sqlite3
```

</details>


## Running tests, lint checks and formatters

### Run all tests and lint checks

```
$ tox -e ALL
```

### Running Python unit tests

```
$ python -m unittest
```

or

```
$ pip install tox
$ tox -e py39
```

### Running visual regression tests using pyppeteer

Please run following commands, then check screenshots in `tmp/` directory.

```
$ pip install -r requirements.txt
$ python visual_regression_test.py --output-dir tmp
```

Note: When you run pyppeteer for the first time, it downloads the latest version of Chromium (~150MB) if it is not found on your system.

### Linters (flake8, black and mypy)

```
$ pip install -r requirements.txt
$ flake8
$ black --check .
$ isort . --check
$ mypy .
```

or

```
$ pip install tox
$ tox -e flake8 -e black -e mypy
```

### Auto-formatting TypeScript files (by prettier)

```
$ npm run fmt
```

### Auto-formatting Python files (by black)

```
$ black .
```


## Release the new version

The release process(compiling TypeScript files, packaging Python distributions and uploading to PyPI) is fully automated by GitHub Actions.

1. Replace `optuna_dashboard.version.__version__` to the next version.
2. Create a git tag and push it to GitHub. If succeeded, GitHub Action will publish the new version to PyPI and create a draft GitHub release.
3. Edit a GitHub release and add change logs. Then make it publish.
4. Post an annoucement on [GitHub Discussions](https://github.com/optuna/optuna-dashboard/discussions/categories/announcements).
