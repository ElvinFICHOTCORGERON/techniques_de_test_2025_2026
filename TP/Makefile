test:
	python3 -m pytest tests

unit_test:
	python3 -m pytest tests/unit -m "not perf"

perf_test:
	python3 -m pytest tests/performance -m "performance"

coverage:
	python3 -m coverage run -m pytest tests
	python3 -m coverage report

lint:
	python3 -m ruff check src tests

doc:
	@mkdir -p docs
	python3 -m pdoc src --output-dir docs --force