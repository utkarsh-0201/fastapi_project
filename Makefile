.PHONY: test lint typecheck format install all

install:
	pip install -r requirements.txt

test:
	PYTHONPATH=. pytest tests/ -v

lint:
	ruff check app/
	flake8 app/

typecheck:
	PYTHONPATH=. mypy app/

format:
	black app/
	isort app/

all: lint typecheck test