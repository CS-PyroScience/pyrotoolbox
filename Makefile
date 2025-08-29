build:
	python3 -m build

black:
	black --line-length 120 pyrotoolbox/*.py

test:
	python3 -m unittest discover -v

publish:
	cp dist/* ~/Server/internAT/9_Software/Python/pyrotoolbox

doku:
	sphinx-build docs docs/_build -b simplepdf

publish_pypi:
	python3 -m twine upload dist/*

all: test build doku publish
