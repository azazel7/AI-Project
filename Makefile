#export PYTHONPATH=$PYTHONPATH:`pwd`/src
test:
	pytest -q tests

libs: lib/magic.c
	python3 setup.py build_ext --inplace
	mv magic.*.so src
