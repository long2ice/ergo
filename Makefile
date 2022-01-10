checkfiles = ergo/ tests/ examples/ conftest.py
py_warn = PYTHONDEVMODE=1

up:
	@poetry update

deps: 
	@poetry install

style: deps
	@isort -src $(checkfiles)
	@black $(checkfiles)

check: deps
	@black --check $(checkfiles) || (echo "Please run 'make style' to auto-fix style issues" && false)
	@flake8 $(checkfiles)
	@bandit -x tests -r $(checkfiles)
	@mypy $(checkfiles)

test: deps
	$(py_warn) pytest

build: clean
	@poetry build

publish: clean
	@poetry publish --build

clean:
	@rm -rf dists

ci: check test
