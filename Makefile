.PHONY: all clean build dev

all: build

build:
	python setup.py build bdist sdist

dev:
	python setup.py develop

clean:
	rm -rf .tox
	find . -name *.pyc -exec rm -rf {} \;
	find . -name __pycache__ -exec rm -rf {} \;
