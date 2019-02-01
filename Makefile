test:
	export PYTHONPATH=$PYTHONPATH:`pwd`/src
	pytest -q tests

libs: lib/hello.c
	python3 setup.py build_ext --inplace
	mv hello.*.so src
