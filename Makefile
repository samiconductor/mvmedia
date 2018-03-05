dist : check clean sdist bdist

check :
	python3 setup.py check -r -s

clean :
	rm -rf build/ dist/

sdist :
	python3 setup.py sdist

bdist :
	python3 setup.py bdist_wheel

venv :
	python3 -m venv mvmedia.venv

dev :
	pip3 install --editable .[dev]
