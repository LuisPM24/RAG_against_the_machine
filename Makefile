GREEN = \033[1;32m
YELLOW = \033[1;33m
RESET = \033[0m

MYPY_FLAGS = --warn-return-any --warn-unused-ignores \
			 --ignore-missing-imports --disallow-untyped-defs \
			 --check-untyped-defs

install:
	@echo "$(YELLOW)\nRunning 'make install' command$(RESET)\n"
	@mkdir -p data/raw
	@unzip -o vllm-0.10.1.zip -d data/raw
	@uv sync
	@echo "$(GREEN)\n'make install' command completed$(RESET)"

run:
	@echo "$(YELLOW)\nRunning 'make run' command$(RESET)\n"
	@uv run python -m src $(ARGS)
	@echo "$(GREEN)\n'make run' command completed$(RESET)"

help:
	@echo "Available commands:"
	@echo "  make install  - Install dependencies"
	@echo "  make run      - Run the application"
	@echo "  make help     - Print help sheet"
	@echo "  make debug    - Run in debug mode"
	@echo "  make clean    - Remove temporary files"
	@echo "  make lint     - Run flake8 and mypy"

debug:
	@echo "$(YELLOW)\nRunning 'make debug' command$(RESET)\n"
	@uv run python -m pdb -m src $(ARGS)
	@echo "$(GREEN)\n'make debug' command completed$(RESET)"

clean:
	@find . -type d \( \
		-name "__pycache__" -o \
		-name "*.egg-info" -o \
		-name ".mypy_cache" -o \
		-name ".pytest_cache" \
	\) -prune -exec rm -rf {} +
	@rm -rf build dist
	@echo "$(GREEN)\n'make clean' command completed$(RESET)"

test:
	@echo "$(YELLOW)\nRunning 'make test' command$(RESET)\n"
	@uv run python -m pytest -s -p no:terminal
	@echo "$(GREEN)\n'make test' command completed$(RESET)"

lint:
	@echo "$(YELLOW)\nRunning 'make lint' command$(RESET)\n"
	@uv run flake8 .
	@uv run mypy . $(MYPY_FLAGS)
	@echo "$(GREEN)\n'make lint' command completed$(RESET)"

.PHONY: install run help debug test clean lint
.DEFAULT_GOAL := help
