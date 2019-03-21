#export PYTHONPATH=$PYTHONPATH:`pwd`/src
test:
	pytest -q tests

libs: clean lib/magic.c
	python3 setup.py build_ext --inplace
	mv magic.*.so src

clean:
	rm -rf src/magic* build
	rm -rf .pytest_cache __pycache__ src/__pycache__ tests/__pycache__
