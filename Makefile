install: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -Ur requirements.txt

run:
	bash run.sh

test: venv
	. venv/bin/activate; pytest

clean:
	rm -rf venv
	find -iname "*.pyc" -delete