# Legend AI - Development Makefile

.PHONY: help install install-dev install-cli test lint format clean build docker run-api run-cli

help:
	@echo "Legend AI - Available commands:"
	@echo ""
	@echo "Installation:"
	@echo "  make install        Install package and dependencies"
	@echo "  make install-dev    Install with development dependencies"
	@echo "  make install-cli    Install CLI dependencies only"
	@echo ""
	@echo "Development:"
	@echo "  make test          Run tests"
	@echo "  make lint          Run linters"
	@echo "  make format        Format code"
	@echo "  make clean         Clean build artifacts"
	@echo ""
	@echo "Build & Deploy:"
	@echo "  make build         Build distribution packages"
	@echo "  make docker        Build Docker images"
	@echo "  make publish-pypi  Publish to PyPI"
	@echo ""
	@echo "Run:"
	@echo "  make run-api       Start API server"
	@echo "  make run-cli       Run CLI in interactive mode"
	@echo "  make run-tui       Run TUI interface"
	@echo ""

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[all]"

install-cli:
	pip install typer[all] rich pyyaml textual

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=app --cov=legend_cli --cov-report=html

test-cli:
	@echo "Testing CLI commands..."
	legend --version
	legend --help
	legend config show

# Linting & Formatting
lint:
	ruff check app/ legend_cli/
	mypy app/ legend_cli/

format:
	black app/ legend_cli/ tests/
	ruff check --fix app/ legend_cli/

# Build
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

# Docker
docker:
	docker build -t legend-ai:latest .
	docker build -f Dockerfile.cli -t legend-ai-cli:latest .

docker-run-api:
	docker run -p 8000:8000 -e REDIS_URL=redis://host.docker.internal:6379 legend-ai:latest

docker-run-cli:
	docker run -it --rm legend-ai-cli:latest legend --help

# Run
run-api:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-cli:
	@python -m legend_cli

run-tui:
	@python -m legend_cli tui

# Publishing
publish-test:
	python -m twine upload --repository testpypi dist/*

publish-pypi:
	python -m twine upload dist/*

# Development helpers
dev-setup:
	@echo "Setting up development environment..."
	pip install -e ".[all]"
	pre-commit install
	@echo "Creating .env from .env.example..."
	cp -n .env.example .env || true
	@echo ""
	@echo "Setup complete! Next steps:"
	@echo "  1. Edit .env with your API keys"
	@echo "  2. Start Redis: docker run -p 6379:6379 redis"
	@echo "  3. Run API: make run-api"
	@echo "  4. Test CLI: legend --help"

check-api:
	@curl -s http://localhost:8000/health | jq . || echo "API not running"

# CLI quick commands
cli-analyze:
	legend analyze AAPL

cli-scan:
	legend scan quick

cli-watchlist:
	legend watchlist list

cli-health:
	legend health

# Database
db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

db-migration:
	@read -p "Enter migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

# Monitoring
metrics:
	curl http://localhost:8000/api/metrics

logs:
	tail -f logs/legend-ai.log
