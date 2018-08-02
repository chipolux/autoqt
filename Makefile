clean:
	rm -rf dist
	rm -rf build
	rm -rf autoqt.egg-info
	rm -rf __pycache__

build:
	python setup.py sdist bdist_wheel

upload_test: build
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
