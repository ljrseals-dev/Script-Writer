.PHONY: help install install-models install-datasets install-dev test lint generate evaluate optimize validate clean
help:
	@printf "install install-models install-datasets install-dev test lint generate evaluate optimize validate clean\n"
install:
	pip install -e .
install-models:
	pip install -e ".[models]"
install-datasets:
	pip install -e ".[datasets]"
install-dev:
	pip install -e ".[dev]"
test:
	pytest
lint:
	ruff check muse_screenplay tests examples
generate:
	muse-screenplay generate --model script-bart --prompt "INT. COFFEE SHOP - DAY" --max-length 200
evaluate:
	muse-screenplay evaluate --dataset offline --limit 4
optimize:
	muse-screenplay optimize --dataset offline --limit 4 --rounds 3
validate:
	muse-screenplay validate --file examples/sample_scene.txt
clean:
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
