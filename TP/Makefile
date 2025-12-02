test:
	pytest tests

unit_test:
	pytest tests/unit -m "not perf"

perf_test:
	pytest tests/performance -m "perf"

coverage:
	coverage run -m pytest tests

lint:
	ruff check src tests

doc:
	pdoc --html docs --output-dir docs --force