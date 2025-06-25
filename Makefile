build:
	python3 -m build

test:
	python3 -m unittest discover -v

publish:
	cp dist/* ~/Server/internAT/9_Software/Python/pyrotoolbox

doku:
	sphinx-build docs docs/_build -b simplepdf

all: test build doku publish
