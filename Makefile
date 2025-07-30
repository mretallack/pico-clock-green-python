

PYTHON=python3.12

run: venv/bin/activate 
	. venv/bin/activate && ${PYTHON} run

venv/bin/activate: requirements.txt
	${PYTHON} -m venv venv
	. venv/bin/activate && ${PYTHON} -m pip install -r requirements.txt
