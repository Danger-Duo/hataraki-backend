VENV = venv/bin
APP = main.py
PY = python3

run: ./$(VENV)/activate
	./$(VENV)/$(PY) $(APP)

$(VENV)/activate: requirements.txt
	$(PY) -m venv venv
	./$(VENV)/pip install --upgrade pip
	./$(VENV)/pip install -r requirements.txt

install: ./$(VENV)/activate

clean:
	rm -rf __pycache__
	rm -rf venv
