.PHONY: test lint typecheck format install all

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

lint:
	ruff check src/
	flake8 src/

typecheck:
	mypy src/

format:
	black src/
	isort src/

all: lint typecheck test