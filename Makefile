test:
	export PYTHONPATH=$PYTHONPATH:`pwd`/src
	pytest -q tests
