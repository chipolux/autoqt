clean:
	rm -rf dist
	rm -rf build
	rm -rf autoqt.egg-info
	rm -rf __pycache__
	rm -rf *.pyc

test:
	python -m unittest

build: clean
	python setup.py sdist bdist_wheel

upload_test: build
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload: build
	twine upload dist/*
