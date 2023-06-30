# api.fairhub.io

## Getting started

### Prerequisites/Dependencies

You will need the following installed on your system:

- Python 3.11+
- [Pip](https://pip.pypa.io/en/stable/)
- [Poetry](https://python-poetry.org/)

### Setup

If you would like to update the api, please follow the instructions below.

1. Create a local virtual environment and activate it:

   ```text
   python -m venv .venv
   source .venv/bin/activate
   ```

   If you are using Anaconda, you can create a virtual environment with:

   ```text
   conda create -n fairhub-api-dev-env python
   conda activate fairhub-api-dev-env
   ```

2. Install the dependencies for this package. We use [Poetry](https://python-poetry.org/) to manage the dependencies:

   ```text
   pip install poetry==1.3.2
   poetry install
   ```

   You can also use version 1.2.0 of Poetry, but you will need to run `poetry lock` after installing the dependencies.

3. Add your modifications and run the tests:

   ```text
   poetry run pytest
   ```

   If you need to add new python packages, you can use Poetry to add them:

   ```text
    poetry add <package-name>
   ```

4. Format the code:

   ```text
   poe format
   ```

5. Check the code quality:

   ```text
   poetry run flake8 pyfairdatatools tests
   ```

6. Run the tests and check the code coverage:

   ```text
   poe test
   poe test --cov=pyfairdatatools
   ```

7. Build the package:

   Update the version number in `pyproject.toml` and `pyfairdatatools/__init__.py` and then run:

   ```text
   poetry build
   ```

8. Publish the package:

   ```text
   poetry publish
   ```

## License

This work is licensed under
[MIT](https://opensource.org/licenses/mit). See [LICENSE](https://github.com/AI-READI/pyfairdatatools/blob/main/LICENSE) for more information.

<a href="https://aireadi.org" >
  <img src="https://www.channelfutures.com/files/2017/04/3_0.png" height="30" />
</a>
