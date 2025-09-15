"""
Backend generator for monorepo bootstrap.
"""

from pathlib import Path


class BackendGenerator:
    def __init__(self, project_name: str, project_dir: Path, features):
        self.project_name = project_name
        self.project_dir = project_dir
        self.features = features

    def create_structure(self):
        """Create the backend structure (FastAPI with Poetry)."""
        print("  🔧 Creating backend structure...")

        # Backend pyproject.toml
        pyproject_content = self._get_pyproject_toml()
        (self.project_dir / "backend" / "pyproject.toml").write_text(pyproject_content)

        # Backend .env.example
        env_example = self._get_env_example()
        (self.project_dir / "backend" / ".env.example").write_text(env_example)

        # Create main.py with CORS configured for frontend
        main_content = self._get_main_py()
        (self.project_dir / "backend" / "src" / "app" / "main.py").write_text(main_content)

        # Create backend README.md (required by Poetry)
        backend_readme = self._get_readme()
        (self.project_dir / "backend" / "README.md").write_text(backend_readme)

        # Create core config.py
        config_content = self._get_config_py()
        (self.project_dir / "backend" / "src" / "app" / "core" / "config.py").write_text(config_content)

        # Create API router structure
        api_v1_content = self._get_api_router()
        (self.project_dir / "backend" / "src" / "app" / "api" / "v1" / "api.py").write_text(api_v1_content)

        # Create basic endpoint files
        self._create_endpoints()

        # Create type generation script
        if self.features.type_generation:
            self._create_type_generation_script()
        
        # Create basic test examples if testing is enabled
        if self.features.testing:
            self._create_basic_tests()

        # Create validation scripts
        self._create_validation_scripts()

        print("  ✓ Backend structure created with FastAPI and Poetry")

    def _get_pyproject_toml(self) -> str:
        # Get dependencies based on features
        deps = self.features.get_backend_dependencies()
        dev_deps = self.features.get_backend_dev_dependencies()
        
        # Format dependencies for TOML
        deps_str = '\n'.join([f'  "{dep}",' for dep in deps])
        
        # Format dev dependencies for TOML
        dev_deps_lines = []
        for name, version in dev_deps.items():
            if isinstance(version, dict):
                # Handle special cases like bandit
                extras = version.get("extras", [])
                extras_str = f'{{extras = {extras}, version = "{version["version"]}"}}' if extras else f'"{version["version"]}"'
                dev_deps_lines.append(f'{name} = {extras_str}')
            else:
                dev_deps_lines.append(f'{name} = "{version}"')
        
        dev_deps_str = '\n'.join(dev_deps_lines)
        
        return f'''[project]
name = "{self.project_name}"
version = "0.1.0"
description = "Backend Bootstrap"
authors = [
  {{ name = "Your Name", email = "your.email@example.com" }}
]
readme = "README.md"
requires-python = ">=3.12,<3.13"

dependencies = [
{deps_str}
]

[tool.poetry.group.dev.dependencies]
{dev_deps_str}

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

# Ruff configuration with architectural antipattern prevention
[tool.ruff]
target-version = "py312"
line-length = 100
fix = true

[tool.ruff.lint]
select = [
    "E", "W", "F",        # pycodestyle errors, warnings, pyflakes
    "UP",                 # pyupgrade  
    "B", "SIM",          # bugbear, simplify
    "I",                 # isort
    "N",                 # naming
    "TCH", "ANN",        # type checking, annotations
    "ASYNC",             # async
    "S",                 # bandit security
    "RUF",               # ruff-specific
    "PTH",               # use pathlib
    "ERA",               # remove commented code
    "C90",               # mccabe complexity
    "PL",                # pylint
    "PERF",              # performance
    "FLY"                # flynt f-string conversion
]
ignore = [
    "ANN101", "ANN102",  # type annotations for self/cls
    "ANN401",            # dynamically typed expressions (Any)
    "B008",              # function call in default argument
    "PLR0913",           # too many arguments (we'll set a custom limit)
    "PLR2004",           # magic value used in comparison
    "S101"               # use of assert (ok in tests)
]

[tool.ruff.lint.per-file-ignores]
# Test files
"tests/*" = ["S101", "ANN", "ARG", "PLR2004", "PLR0913"]
# Migration files  
"alembic/*" = ["ANN", "ARG", "ERA001"]
# API routes - enforce architectural patterns
"**/api/v1/endpoints/*" = ["PLR0913"]  # Routes should have few args (use services)
# Models can have many fields
"**/models/*" = ["PLR0913"]

[tool.ruff.lint.mccabe]
max-complexity = 8

[tool.ruff.lint.pylint]
max-args = 6          # Force dependency injection over parameter lists
max-locals = 15       # Reasonable limit for local vars
max-branches = 12     # Prevent deeply nested conditionals

[tool.ruff.lint.flake8-tidy-imports]
ban-relative-imports = "all"  # Force absolute imports

[tool.ruff.lint.isort]
known-first-party = ["src"]
force-single-line = true
lines-after-imports = 2

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true

[[tool.mypy.overrides]]
module = "tests.*"
ignore_errors = true

[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
asyncio_mode = "auto"
pythonpath = ["."]
'''

    def _get_env_example(self) -> str:
        return f'''# Backend Environment Variables
ENVIRONMENT=development
DEBUG=true

# API
API_PREFIX=/api/v1
PROJECT_NAME=FastAPI Backend
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/{self.project_name}_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Frontend URL (for emails, etc.)
FRONTEND_URL=http://localhost:3000
'''

    def _get_main_py(self) -> str:
        return '''"""
FastAPI application entry point configured for monorepo.
"""

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import structlog

from src.app.api.v1.api import api_router
from src.app.core.config import get_settings

logger = structlog.get_logger()
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    logger.info("Starting application", environment=settings.ENVIRONMENT)
    yield
    logger.info("Shutting down application")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Health check
@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy", "service": "backend"}

'''

    def _get_readme(self) -> str:
        return f'''# {self.project_name.replace("_", " ").title()} Backend

FastAPI backend service for the {self.project_name} monorepo.

## Development

1. Install dependencies:
   ```bash
   poetry install
   ```

2. Set up environment:
   ```bash
   cp .env.example .env
   ```

3. Run the server:
   ```bash
   poetry run uvicorn src.app.main:app --reload
   ```

## API Documentation

- Interactive API docs: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc

## Testing

```bash
poetry run pytest
```
'''

    def _get_config_py(self) -> str:
        return f'''"""
Application configuration using Pydantic settings.
"""
from functools import lru_cache
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Project info
    PROJECT_NAME: str = "FastAPI Backend"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Backend API"
    
    # API Configuration
    API_V1_PREFIX: str = Field(default="/api/v1", alias="API_PREFIX")
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 1 week
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/{self.project_name}_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Frontend URL
    FRONTEND_URL: str = "http://localhost:3000"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
'''

    def _get_api_router(self) -> str:
        return '''"""
API v1 router configuration.
"""
from fastapi import APIRouter

from src.app.api.v1.endpoints import health

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
'''

    def _create_endpoints(self):
        """Create basic endpoint files."""
        # Health endpoint
        health_endpoint = '''"""
Health check endpoints.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from src.app.core.config import get_settings

router = APIRouter()
settings = get_settings()

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str

@router.get("/", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=settings.ENVIRONMENT
    )
'''
        (self.project_dir / "backend" / "src" / "app" / "api" / "v1" / "endpoints" / "health.py").write_text(health_endpoint)


    def _create_type_generation_script(self):
        """Create a type generation script."""
        # Read the robust type generation script and modify it for embedding
        robust_script_path = Path(__file__).parent.parent / "scripts" / "generate_types_robust.py"
        robust_script_content = robust_script_path.read_text()
        
        # Remove the original main function and if __name__ == "__main__" block
        robust_script_lines = robust_script_content.split('\n')
        filtered_lines = []
        skip_lines = False
        
        for line in robust_script_lines:
            if line.strip().startswith('def main():'):
                skip_lines = True
                continue
            elif line.strip().startswith('if __name__ == "__main__":'):
                skip_lines = True
                continue
            elif skip_lines and line.strip() == '':
                continue
            elif skip_lines and not line.startswith('    ') and not line.startswith('\t') and line.strip():
                skip_lines = False
                filtered_lines.append(line)
            elif not skip_lines:
                filtered_lines.append(line)
        
        robust_script_clean = '\n'.join(filtered_lines).rstrip()
        
        # Create a wrapper script that calls our robust generator
        type_gen_script = f'''#!/usr/bin/env python3
"""
Generate TypeScript types from Pydantic schemas.
This script uses a robust custom solution that handles edge cases gracefully.
"""

import sys
from pathlib import Path

# Embedded robust type generator
{robust_script_clean}

def main():
    """Main wrapper that calls the robust generator with correct paths."""
    schemas_path = Path("src/app/schemas")
    output_path = Path("../frontend/src/types/api.generated.ts")
    
    print(f"🔄 Generating TypeScript types...")
    print(f"   Schemas: {{schemas_path}}")
    print(f"   Output:  {{output_path}}")
    
    success = generate_typescript_types(schemas_path, output_path)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
'''

        script_path = self.project_dir / "backend" / "scripts" / "generate_types.py"
        script_path.parent.mkdir(parents=True, exist_ok=True)
        script_path.write_text(type_gen_script)
        script_path.chmod(0o755)
    
    def _create_basic_tests(self):
        """Create basic test examples to get developers started."""
        # Test health endpoint
        health_test = '''"""
Test health check endpoint.
"""
import pytest
from httpx import AsyncClient
from src.app.main import app


@pytest.mark.asyncio
async def test_health_endpoint():
    """Test that health endpoint returns correct response."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "backend"
'''
        (self.project_dir / "backend" / "tests" / "unit" / "test_health.py").write_text(health_test)
        
        # Test API v1 health endpoint if testing is enabled
        if self.features.testing:
            api_health_test = '''"""
Test API v1 health endpoint.
"""
import pytest
from httpx import AsyncClient
from src.app.main import app


@pytest.mark.asyncio
async def test_api_health_endpoint():
    """Test that API health endpoint returns correct response."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/health/")
        
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data
    assert "environment" in data
'''
            (self.project_dir / "backend" / "tests" / "unit" / "test_api_health.py").write_text(api_health_test)
        
        # Basic conftest.py for pytest configuration
        conftest_content = '''"""
Pytest configuration and fixtures.
"""
import pytest
from httpx import AsyncClient
from src.app.main import app


@pytest.fixture
async def client():
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
'''
        (self.project_dir / "backend" / "tests" / "conftest.py").write_text(conftest_content)

    def _create_validation_scripts(self):
        """Create environment validation scripts."""
        # Read validation script template
        template_path = Path(__file__).parent.parent / "templates" / "validate_env.sh"
        if template_path.exists():
            validation_script = template_path.read_text()

            # Create scripts directory if it doesn't exist
            scripts_dir = self.project_dir / "backend" / "scripts"
            scripts_dir.mkdir(exist_ok=True)

            # Write validation script
            validate_script_path = scripts_dir / "validate_env.sh"
            validate_script_path.write_text(validation_script)
            validate_script_path.chmod(0o755)  # Make executable