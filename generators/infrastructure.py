"""
Infrastructure generator for monorepo bootstrap.
"""

import json
from pathlib import Path
from typing import Dict, Any


class InfrastructureGenerator:
    def __init__(self, project_name: str, project_dir: Path, features):
        self.project_name = project_name
        self.project_dir = project_dir
        self.features = features

    def create_docker_files(self):
        """Create Docker configuration files."""
        print("  🐳 Creating Docker configuration...")

        # Development docker-compose
        dev_compose = self._get_dev_compose()
        (self.project_dir / "infrastructure" / "docker" / "docker-compose.dev.yml").write_text(dev_compose)

        # Production docker-compose
        prod_compose = self._get_prod_compose()
        (self.project_dir / "infrastructure" / "docker" / "docker-compose.yml").write_text(prod_compose)

        # Backend Dockerfile for development
        backend_dockerfile_dev = self._get_backend_dockerfile_dev()
        (self.project_dir / "backend" / "Dockerfile.dev").write_text(backend_dockerfile_dev)

        # Frontend Dockerfile for development
        frontend_dockerfile_dev = self._get_frontend_dockerfile_dev()
        (self.project_dir / "frontend" / "Dockerfile.dev").write_text(frontend_dockerfile_dev)

        print("  ✓ Docker configuration created")

    def create_vscode_settings(self):
        """Create VSCode workspace settings for monorepo."""
        print("  📝 Creating VSCode workspace settings...")

        # VSCode multi-root workspace
        workspace = self._get_workspace_config()
        workspace_file = f"{self.project_name}.code-workspace"
        (self.project_dir / workspace_file).write_text(json.dumps(workspace, indent=2))

        # VSCode settings.json
        settings = self._get_vscode_settings()
        (self.project_dir / ".vscode" / "settings.json").write_text(json.dumps(settings, indent=2))

        # VSCode launch.json for debugging
        launch_config = self._get_launch_config()
        (self.project_dir / ".vscode" / "launch.json").write_text(json.dumps(launch_config, indent=2))

        # VSCode tasks.json for common development tasks
        tasks_config = self._get_tasks_config()
        (self.project_dir / ".vscode" / "tasks.json").write_text(json.dumps(tasks_config, indent=2))

        print("  ✓ VSCode workspace settings created")

    def create_github_workflows(self):
        """Create GitHub Actions workflows for monorepo CI/CD."""
        print("  🔄 Creating GitHub Actions workflows...")

        ci_workflow = self._get_ci_workflow()
        (self.project_dir / ".github" / "workflows" / "ci.yml").write_text(ci_workflow)

        print("  ✓ GitHub Actions workflows created")

    def _get_dev_compose(self) -> str:
        return f'''version: '3.8'

services:
  # Database
  db:
    image: postgres:16-alpine
    container_name: {self.project_name}_db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: {self.project_name}_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis
  redis:
    image: redis:7-alpine
    container_name: {self.project_name}_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Backend (uncomment for containerized development)
  # backend:
  #   build:
  #     context: ../../backend
  #     dockerfile: Dockerfile.dev
  #   container_name: {self.project_name}_backend
  #   ports:
  #     - "8000:8000"
  #   volumes:
  #     - ../../backend:/app
  #   environment:
  #     DATABASE_URL: postgresql+asyncpg://postgres:postgres@db:5432/{self.project_name}_db
  #     REDIS_URL: redis://redis:6379/0
  #   depends_on:
  #     db:
  #       condition: service_healthy
  #     redis:
  #       condition: service_healthy

  # Frontend (uncomment for containerized development)
  # frontend:
  #   build:
  #     context: ../../frontend
  #     dockerfile: Dockerfile.dev
  #   container_name: {self.project_name}_frontend
  #   ports:
  #     - "3000:3000"
  #   volumes:
  #     - ../../frontend:/app
  #     - /app/node_modules
  #   environment:
  #     VITE_API_URL: http://localhost:8000/api/v1

  # Adminer for database management
  adminer:
    image: adminer
    container_name: {self.project_name}_adminer
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  postgres_data:
  redis_data:
'''

    def _get_prod_compose(self) -> str:
        return f'''version: '3.8'

services:
  backend:
    build:
      context: ../../backend
      dockerfile: Dockerfile
    container_name: {self.project_name}_backend_prod
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: ${{DATABASE_URL}}
      REDIS_URL: ${{REDIS_URL}}
      SECRET_KEY: ${{SECRET_KEY}}
      ENVIRONMENT: production
    restart: unless-stopped

  frontend:
    build:
      context: ../../frontend
      dockerfile: Dockerfile
    container_name: {self.project_name}_frontend_prod
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: {self.project_name}_nginx
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped
'''

    def _get_backend_dockerfile_dev(self) -> str:
        return '''FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry==1.8.3

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.create false \\
    && poetry install --no-interaction --no-ansi

# Copy application code (in dev, we'll mount as volume)
COPY . .

# Run with reload
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
'''

    def _get_frontend_dockerfile_dev(self) -> str:
        return '''FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code (in dev, we'll mount as volume)
COPY . .

# Expose port
EXPOSE 3000

# Run development server
CMD ["npm", "run", "dev"]
'''

    def _get_workspace_config(self) -> Dict[str, Any]:
        return {
            "folders": [
                {"name": "Backend", "path": "backend"},
                {"name": "Frontend", "path": "frontend"},
                {"name": "Shared", "path": "shared"},
                {"name": "Infrastructure", "path": "infrastructure"},
                {"name": "Root", "path": "."}
            ],
            "settings": {
                "files.exclude": {
                    "**/__pycache__": True,
                    "**/*.pyc": True,
                    "**/node_modules": True,
                    "**/.pytest_cache": True,
                    "**/.mypy_cache": True
                },
                "python.linting.enabled": False,
                "python.formatting.provider": "none",
                "[python]": {
                    "editor.formatOnSave": True,
                    "editor.codeActionsOnSave": {
                        "source.organizeImports": "explicit",
                        "source.fixAll": "explicit"
                    },
                    "editor.defaultFormatter": "charliermarsh.ruff"
                },
                "[typescript]": {
                    "editor.formatOnSave": True,
                    "editor.defaultFormatter": "esbenp.prettier-vscode"
                },
                "[typescriptreact]": {
                    "editor.formatOnSave": True,
                    "editor.defaultFormatter": "esbenp.prettier-vscode"
                },
                "editor.rulers": [100],
                "files.trimTrailingWhitespace": True,
                "files.insertFinalNewline": True
            },
            "extensions": {
                "recommendations": [
                    "ms-python.python",
                    "ms-python.vscode-pylance",
                    "charliermarsh.ruff",
                    "ms-azuretools.vscode-docker",
                    "dbaeumer.vscode-eslint",
                    "esbenp.prettier-vscode",
                    "bradlc.vscode-tailwindcss",
                    "usernamehw.errorlens",
                    "eamodio.gitlens",
                    "streetsidesoftware.code-spell-checker"
                ]
            }
        }

    def _get_vscode_settings(self) -> Dict[str, Any]:
        return {
            "search.exclude": {
                "**/node_modules": True,
                "**/__pycache__": True,
                "**/dist": True,
                "**/build": True,
                "**/.venv": True
            },
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.fixAll.eslint": "explicit"
            },
            "python.defaultInterpreterPath": "./venv/bin/python",
            "typescript.tsdk": "./frontend/node_modules/typescript/lib",
            "typescript.enablePromptUseWorkspaceTsdk": True
        }

    def _get_ci_workflow(self) -> str:
        return '''name: Monorepo CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # Detect changes to optimize CI runs
  changes:
    runs-on: ubuntu-latest
    outputs:
      backend: ${{ steps.changes.outputs.backend }}
      frontend: ${{ steps.changes.outputs.frontend }}
      infrastructure: ${{ steps.changes.outputs.infrastructure }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v2
        id: changes
        with:
          filters: |
            backend:
              - 'backend/**'
              - '.github/workflows/**'
            frontend:
              - 'frontend/**'
              - '.github/workflows/**'
            infrastructure:
              - 'infrastructure/**'
              - '.github/workflows/**'

  # Backend testing
  backend:
    needs: changes
    if: needs.changes.outputs.backend == 'true'
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Poetry
        uses: snok/install-poetry@v1
        with:
          version: 1.8.3
          virtualenvs-create: true
          virtualenvs-in-project: true

      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          path: venv
          key: venv-${{ runner.os }}-py3.12-${{ hashFiles('backend/poetry.lock') }}

      - name: Install dependencies
        run: poetry install --no-dependencies --no-root

      - name: Run linters
        run: |
          poetry run ruff check src tests
          poetry run ruff format --check src tests
          poetry run mypy src

      - name: Run tests
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5432/test_db
          SECRET_KEY: test-secret-key
        run: poetry run pytest --cov=src --cov-report=xml

  # Frontend testing
  frontend:
    needs: changes
    if: needs.changes.outputs.frontend == 'true'
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: frontend

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: npm ci

      - name: Type check
        run: npm run type-check

      - name: Lint
        run: npm run lint

      - name: Test
        run: npm test

      - name: Build
        run: npm run build

  # Build Docker images
  docker:
    needs: [backend, frontend]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build Backend
        run: |
          docker build -t ${{ github.repository }}-backend:${{ github.sha }} ./backend

      - name: Build Frontend
        run: |
          docker build -t ${{ github.repository }}-frontend:${{ github.sha }} ./frontend
'''

    def _get_launch_config(self) -> Dict[str, Any]:
        """Generate VSCode launch.json configuration for FastAPI debugging."""
        return {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "FastAPI Debug",
                    "type": "python",
                    "request": "launch",
                    "program": "${workspaceFolder}/venv/bin/uvicorn",
                    "args": [
                        "src.app.main:app",
                        "--reload",
                        "--host",
                        "0.0.0.0",
                        "--port",
                        "8000"
                    ],
                    "cwd": "${workspaceFolder}/backend",
                    "env": {
                        "PYTHONPATH": "${workspaceFolder}/backend/src"
                    },
                    "console": "integratedTerminal",
                    "justMyCode": False,
                    "python": "${workspaceFolder}/venv/bin/python"
                },
                {
                    "name": "FastAPI Debug (Production Mode)",
                    "type": "python",
                    "request": "launch",
                    "program": "${workspaceFolder}/venv/bin/uvicorn",
                    "args": [
                        "src.app.main:app",
                        "--host",
                        "0.0.0.0",
                        "--port",
                        "8000"
                    ],
                    "cwd": "${workspaceFolder}/backend",
                    "env": {
                        "PYTHONPATH": "${workspaceFolder}/backend/src",
                        "ENVIRONMENT": "production"
                    },
                    "console": "integratedTerminal",
                    "justMyCode": False,
                    "python": "${workspaceFolder}/venv/bin/python"
                },
                {
                    "name": "Python: Current File",
                    "type": "python",
                    "request": "launch",
                    "program": "${file}",
                    "console": "integratedTerminal",
                    "justMyCode": False,
                    "python": "${workspaceFolder}/venv/bin/python"
                },
                {
                    "name": "Python: Backend Tests",
                    "type": "python",
                    "request": "launch",
                    "module": "pytest",
                    "args": [
                        "-v",
                        "--tb=short"
                    ],
                    "cwd": "${workspaceFolder}/backend",
                    "env": {
                        "PYTHONPATH": "${workspaceFolder}/backend/src"
                    },
                    "console": "integratedTerminal",
                    "justMyCode": False,
                    "python": "${workspaceFolder}/venv/bin/python"
                }
            ]
        }

    def _get_tasks_config(self) -> Dict[str, Any]:
        """Generate VSCode tasks.json configuration for common development tasks."""
        return {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "Install All Dependencies",
                    "type": "shell",
                    "command": "make",
                    "args": ["install"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                        "showReuseMessage": True,
                        "clear": False
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Start Development Server",
                    "type": "shell",
                    "command": "make",
                    "args": ["dev"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                        "showReuseMessage": True,
                        "clear": False
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Start Backend Only",
                    "type": "shell",
                    "command": "make",
                    "args": ["dev-backend"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                        "showReuseMessage": True,
                        "clear": False
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Start Frontend Only",
                    "type": "shell",
                    "command": "make",
                    "args": ["dev-frontend"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                        "showReuseMessage": True,
                        "clear": False
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Run All Tests",
                    "type": "shell",
                    "command": "make",
                    "args": ["test"],
                    "group": "test",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                        "showReuseMessage": True,
                        "clear": False
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Run Backend Tests",
                    "type": "shell",
                    "command": "make",
                    "args": ["test-backend"],
                    "group": "test",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                        "showReuseMessage": True,
                        "clear": False
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Run Frontend Tests",
                    "type": "shell",
                    "command": "make",
                    "args": ["test-frontend"],
                    "group": "test",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                        "showReuseMessage": True,
                        "clear": False
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Lint All Code",
                    "type": "shell",
                    "command": "make",
                    "args": ["lint"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                        "showReuseMessage": True,
                        "clear": False
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Format All Code",
                    "type": "shell",
                    "command": "make",
                    "args": ["format"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                        "showReuseMessage": True,
                        "clear": False
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Generate TypeScript Types",
                    "type": "shell",
                    "command": "make",
                    "args": ["types"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                        "showReuseMessage": True,
                        "clear": False
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Clean Build Artifacts",
                    "type": "shell",
                    "command": "make",
                    "args": ["clean"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                        "showReuseMessage": True,
                        "clear": False
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Docker: Start Services",
                    "type": "shell",
                    "command": "make",
                    "args": ["docker-up"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                        "showReuseMessage": True,
                        "clear": False
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Docker: Stop Services",
                    "type": "shell",
                    "command": "make",
                    "args": ["docker-down"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                        "showReuseMessage": True,
                        "clear": False
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Database: Run Migrations",
                    "type": "shell",
                    "command": "make",
                    "args": ["migrate"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                        "showReuseMessage": True,
                        "clear": False
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Database: Reset Development DB",
                    "type": "shell",
                    "command": "make",
                    "args": ["db-reset"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                        "showReuseMessage": True,
                        "clear": False
                    },
                    "problemMatcher": []
                }
            ]
        }
