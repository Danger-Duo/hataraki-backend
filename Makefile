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

test-app: 
	docker compose -f tests/docker-compose.yml build test_app -q
	docker compose -f tests/docker-compose.yml run --rm --quiet-pull test_app pytest -v
	docker compose -f tests/docker-compose.yml down -v

clean:
	rm -rf __pycache__
	rm -rf venv
