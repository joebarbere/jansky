# Convenience targets for the jansky course. Run `make help` for the list.
# Everything goes through uv so you get the pinned Python 3.12 environment.

.DEFAULT_GOAL := help
.PHONY: help setup lab docs docs-serve test test-notebooks lint fmt fetch-data clean container

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

setup: ## Create the environment (Python 3.12 + deps)
	uv sync

lab: ## Launch JupyterLab on the notebooks
	uv run jupyter lab

docs: ## Build the MkDocs site (strict)
	uv run mkdocs build --strict

docs-serve: ## Serve the docs site with live reload at http://localhost:8000
	uv run mkdocs serve

test: ## Run the helper-package unit tests
	uv run pytest

test-notebooks: ## Smoke-test the Part I notebooks (executes them via nbmake)
	uv run pytest --nbmake \
		notebooks/01_what_is_radio_astronomy.ipynb \
		notebooks/02_physics_of_radio_emission.ipynb \
		notebooks/03_signals_noise_radiometer.ipynb

lint: ## Lint with ruff
	uv run ruff check src/ tests/

fmt: ## Auto-format with ruff
	uv run ruff format src/ tests/

fetch-data: ## List sample datasets (use ARGS="--fetch hi4pi-sample" to download)
	uv run python -m jansky.data $(ARGS) --list

container: ## Build & run the JupyterLab container (podman or docker)
	podman compose -f containers/compose.yaml up lab

clean: ## Remove build artefacts and caches
	rm -rf site/ .pytest_cache/ .ruff_cache/
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
