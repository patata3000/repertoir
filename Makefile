build-install:
	python -m build && script_pip install dist/repertoir-0.1.0-py3-none-any.whl --force

clean:
	scripts/clean_all
