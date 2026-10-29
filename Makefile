PY ?= python

setup:
	$(PY) -m venv .venv && .venv/bin/pip install -U pip && .venv/bin/pip install -e ".[dev]"
data:
	$(PY) scripts/generate_demo_data.py --rows 6000
train: data
	$(PY) scripts/train_model.py
test:
	$(PY) -m pytest -q
api:
	uvicorn sentinelai.api:app --reload --app-dir backend
dashboard:
	streamlit run dashboard/app.py
lint:
	ruff check .
