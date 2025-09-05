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

[tool.ruff.per-file-ignores]
# Test files
"tests/*" = ["S101", "ANN", "ARG", "PLR2004", "PLR0913"]
# Migration files  
"alembic/*" = ["ANN", "ARG", "ERA001"]
# API routes - enforce architectural patterns
"**/api/v1/endpoints/*" = ["PLR0913"]  # Routes should have few args (use services)
# Models can have many fields
"**/models/*" = ["PLR0913"]

[tool.ruff.mccabe]
max-complexity = 8

[tool.ruff.pylint]
max-args = 6          # Force dependency injection over parameter lists
max-locals = 15       # Reasonable limit for local vars
max-branches = 12     # Prevent deeply nested conditionals

[tool.ruff.flake8-tidy-imports]
ban-relative-imports = "all"  # Force absolute imports

[tool.ruff.isort]
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
async def lifespan(app: FastAPI):
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
async def health_check():
    return {"status": "healthy", "service": "backend"}

# In production, you might serve the built frontend from here
# if (Path(__file__).parent / "static").exists():
#     app.mount("/", StaticFiles(directory="static", html=True), name="static")
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
from pydantic_settings import BaseSettings


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
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
'''

    def _get_api_router(self) -> str:
        # Build imports and router includes based on features
        imports = ['from src.app.api.v1.endpoints import health']
        router_includes = ['api_router.include_router(health.router, prefix="/health", tags=["health"])']
        
        if self.features.authentication:
            imports.append('from src.app.api.v1.endpoints import auth, users')
            router_includes.extend([
                'api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])',
                'api_router.include_router(users.router, prefix="/users", tags=["users"])'
            ])
        
        imports_str = '\n'.join(imports)
        includes_str = '\n'.join([f'{inc}' for inc in router_includes])
        
        return f'''"""
API v1 router configuration.
"""
from fastapi import APIRouter

{imports_str}

api_router = APIRouter()

# Include endpoint routers
{includes_str}
'''

    def _create_endpoints(self):
        """Create basic endpoint files."""
        # Health endpoint
        health_endpoint = '''"""
Health check endpoints.
"""
from fastapi import APIRouter
from src.app.core.config import get_settings

router = APIRouter()
settings = get_settings()

@router.get("/")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }
'''
        (self.project_dir / "backend" / "src" / "app" / "api" / "v1" / "endpoints" / "health.py").write_text(health_endpoint)

        # Create authentication endpoints only if enabled
        if self.features.authentication:
            # Auth endpoint (placeholder)
            auth_endpoint = '''"""
Authentication endpoints.
"""
from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
async def login():
    """Login endpoint (placeholder)."""
    return {"message": "Login endpoint - implement authentication logic here"}

@router.post("/logout")  
async def logout():
    """Logout endpoint (placeholder)."""
    return {"message": "Logout successful"}
'''
            (self.project_dir / "backend" / "src" / "app" / "api" / "v1" / "endpoints" / "auth.py").write_text(auth_endpoint)

            # Users endpoint (placeholder)
            users_endpoint = '''"""
User management endpoints.
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/me")
async def get_current_user():
    """Get current user (placeholder)."""
    return {"message": "Get current user - implement user logic here"}
'''
            (self.project_dir / "backend" / "src" / "app" / "api" / "v1" / "endpoints" / "users.py").write_text(users_endpoint)

    def _create_type_generation_script(self):
        """Create a type generation script."""
        type_gen_script = '''#!/usr/bin/env python3
"""
Generate TypeScript types from Pydantic schemas.
This script should be run from the backend directory.
"""

import subprocess
from pathlib import Path


def generate_types():
    """Generate TypeScript types from Pydantic schemas."""
    schemas_path = Path("src/app/schemas")
    output_path = Path("../frontend/src/types/api.generated.ts")

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Run pydantic2ts
    cmd = [
        "pydantic2ts",
        "--module", str(schemas_path).replace("/", "."),
        "--output", str(output_path),
        "--json2ts-cmd", "npx json2ts"
    ]

    print(f"Generating TypeScript types from {schemas_path} to {output_path}")

    try:
        subprocess.run(cmd, check=True)
        print("✅ Types generated successfully!")

        # Add a header to the generated file
        content = output_path.read_text()
        header = """/* eslint-disable */
/* tslint:disable */
/**
 * AUTO-GENERATED FILE - DO NOT EDIT
 * This file is automatically generated from Pydantic schemas.
 * Run 'make types' from the root to regenerate.
 */

"""
        output_path.write_text(header + content)

    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating types: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(generate_types())
'''

        script_path = self.project_dir / "backend" / "scripts" / "generate_types.py"
        script_path.parent.mkdir(parents=True, exist_ok=True)
        script_path.write_text(type_gen_script)
        script_path.chmod(0o755)