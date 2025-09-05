"""
Feature configuration system for monorepo bootstrap.
Manages toggleable features and their dependencies.
"""

from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class FeatureConfig:
    """Configuration class for managing toggleable features in the monorepo bootstrap."""
    
    # Core infrastructure features
    database: bool = True
    cache: bool = True
    background_jobs: bool = True
    docker: bool = True
    
    # Development & CI features
    ci_cd: bool = True
    testing: bool = True
    vscode: bool = True
    
    # Code generation & tooling features
    type_generation: bool = True
    authentication: bool = True
    minimal_tooling: bool = False
    
    @classmethod
    def from_args(cls, args) -> 'FeatureConfig':
        """Create FeatureConfig from command line arguments."""
        return cls(
            # Core infrastructure
            database=not getattr(args, 'no_database', False),
            cache=not getattr(args, 'no_cache', False),
            background_jobs=not getattr(args, 'no_celery', False),
            docker=not getattr(args, 'no_docker', False),
            
            # Development & CI
            ci_cd=not getattr(args, 'no_ci', False),
            testing=not getattr(args, 'no_testing', False),
            vscode=not getattr(args, 'no_vscode', False),
            
            # Code generation & tooling
            type_generation=not getattr(args, 'no_type_gen', False),
            authentication=not getattr(args, 'no_auth', False),
            minimal_tooling=getattr(args, 'minimal_tooling', False),
        )
    
    def get_backend_dependencies(self) -> List[str]:
        """Return backend dependencies based on enabled features."""
        deps = [
            "fastapi>=0.115.0,<0.116.0",
            "uvicorn[standard]>=0.32.0,<0.33.0",
            "pydantic>=2.9.0,<3.0.0",
            "pydantic-settings>=2.5.0,<3.0.0",
            "httpx>=0.27.0,<0.28.0",
            "structlog>=24.4.0,<25.0.0",
        ]
        
        if self.database:
            deps.extend([
                "sqlalchemy>=2.0.35,<3.0.0",
                "alembic>=1.13.0,<2.0.0",
                "asyncpg>=0.29.0,<0.30.0",
            ])
        
        if self.cache:
            deps.extend([
                "redis>=5.1.0,<6.0.0",
            ])
        
        if self.background_jobs:
            deps.extend([
                "celery>=5.4.0,<6.0.0",
            ])
        
        if self.authentication:
            deps.extend([
                "python-jose[cryptography]>=3.3.0,<4.0.0",
                "passlib[bcrypt]>=1.7.4,<2.0.0",
                "python-multipart>=0.0.12,<0.1.0",
                "email-validator>=2.2.0,<3.0.0",
            ])
        
        # Always include Sentry for error tracking (can be disabled via env)
        deps.append("sentry-sdk>=2.14.0,<3.0.0")
        
        return deps
    
    def get_backend_dev_dependencies(self) -> Dict[str, str]:
        """Return backend dev dependencies based on enabled features."""
        deps = {
            "ipython": "^8.27.0",
            "rich": "^13.8.0",
        }
        
        if self.testing:
            deps.update({
                "pytest": "^8.3.0",
                "pytest-asyncio": "^0.24.0",
                "pytest-cov": "^5.0.0",
                "factory-boy": "^3.3.0",
                "faker": "^28.0.0",
            })
        
        if not self.minimal_tooling:
            deps.update({
                "ruff": "^0.7.0",
                "mypy": "^1.11.0",
                "bandit": {"extras": ["toml"], "version": "^1.7.10"},
            })
        else:
            deps.update({
                "ruff": "^0.7.0",  # Keep ruff as it's fast and essential
            })
        
        if self.type_generation:
            deps.update({
                "pydantic-to-typescript2": "^1.0.0",
            })
        
        return deps
    
    def get_frontend_dev_dependencies(self) -> Dict[str, str]:
        """Return frontend dev dependencies based on enabled features."""
        deps = {}
        
        if self.testing:
            deps.update({
                "@testing-library/jest-dom": "^6.0.0",
                "@testing-library/react": "^16.0.0",
                "@testing-library/user-event": "^14.0.0",
                "jsdom": "^25.0.0",
                "vitest": "^2.0.0",
            })
        
        if not self.minimal_tooling:
            deps.update({
                "eslint": "^8.57.0",
                "@typescript-eslint/eslint-plugin": "^8.0.0",
                "@typescript-eslint/parser": "^8.0.0",
                "prettier": "^3.0.0",
                "eslint-config-prettier": "^9.0.0",
                "eslint-plugin-react-hooks": "^4.6.0",
                "eslint-plugin-react-refresh": "^0.4.0",
            })
        
        return deps
    
    def get_root_dev_dependencies(self) -> Dict[str, str]:
        """Return root-level dev dependencies based on enabled features."""
        deps = {
            "@types/node": "^20.0.0",
            "concurrently": "^8.0.0",
        }
        
        if not self.minimal_tooling:
            deps.update({
                "husky": "^9.0.0",
                "lint-staged": "^15.0.0",
            })
        
        return deps
    
    def should_create_directory(self, directory: str) -> bool:
        """Check if a directory should be created based on enabled features."""
        feature_dirs = {
            # Database-related directories
            "backend/alembic": self.database,
            "backend/alembic/versions": self.database,
            "backend/src/app/models": self.database,
            
            # Testing directories
            "backend/tests": self.testing,
            "backend/tests/unit": self.testing,
            "backend/tests/integration": self.testing,
            "backend/tests/fixtures": self.testing,
            
            # Infrastructure directories
            "infrastructure": self.docker or self.ci_cd,
            "infrastructure/docker": self.docker,
            "infrastructure/kubernetes": self.docker,
            "infrastructure/terraform": self.docker,
            
            # CI/CD directories
            ".github": self.ci_cd,
            ".github/workflows": self.ci_cd,
            
            # VSCode directories
            ".vscode": self.vscode,
        }
        
        # Check if any parent directory should be excluded
        for pattern, should_create in feature_dirs.items():
            if directory.startswith(pattern) and not should_create:
                return False
        
        return True
    
    def get_makefile_commands(self) -> Dict[str, str]:
        """Get Makefile commands based on enabled features."""
        commands = {
            "install": "Install all dependencies",
            "dev-backend": "Start backend in development mode",
            "dev-frontend": "Start frontend in development mode",
            "clean": "Remove all cache and build files",
            "help": "Show this help message",
        }
        
        if self.docker:
            commands.update({
                "dev": "Start all services with Docker",
                "docker-up": "Start all services with Docker",
                "docker-down": "Stop all Docker services",
                "docker-logs": "View Docker service logs",
                "build": "Build all services",
            })
        else:
            commands.update({
                "dev": "Start all services in development mode",
            })
        
        if self.testing:
            commands.update({
                "test": "Run all tests",
                "test-backend": "Run backend tests only",
                "test-frontend": "Run frontend tests only",
            })
        
        if not self.minimal_tooling:
            commands.update({
                "lint": "Run all linters",
                "format": "Format all code",
            })
        
        if self.type_generation:
            commands["types"] = "Generate TypeScript types from Pydantic schemas"
        
        if self.database:
            commands.update({
                "migrate": "Run database migrations",
                "db-create": "Create new migration",
                "db-reset": "Reset development database",
            })
        
        return commands
    
    def get_excluded_files(self) -> List[str]:
        """Get list of files/patterns that should be excluded based on disabled features."""
        excluded = []
        
        if not self.docker:
            excluded.extend([
                "*/Dockerfile*",
                "*/docker-compose*",
                "infrastructure/docker/",
            ])
        
        if not self.testing:
            excluded.extend([
                "*/tests/",
                "*test*",
                "*.test.*",
                "*.spec.*",
            ])
        
        if not self.ci_cd:
            excluded.extend([
                ".github/",
            ])
        
        if not self.vscode:
            excluded.extend([
                ".vscode/",
                "*.code-workspace",
            ])
        
        return excluded
    
    def print_summary(self, project_name: str, frontend_type: str):
        """Print a summary of enabled features."""
        print(f"\n🚀 Bootstrapping Monorepo: {project_name}")
        print(f"   Frontend Framework: {frontend_type}")
        
        print("\n📋 Enabled Features:")
        features = [
            ("Database (PostgreSQL)", self.database),
            ("Cache (Redis)", self.cache), 
            ("Background Jobs (Celery)", self.background_jobs),
            ("Docker", self.docker),
            ("CI/CD", self.ci_cd),
            ("Testing", self.testing),
            ("VSCode Config", self.vscode),
            ("Type Generation", self.type_generation),
            ("Authentication", self.authentication),
        ]
        
        enabled = [name for name, enabled in features if enabled]
        disabled = [name for name, enabled in features if not enabled]
        
        for feature in enabled:
            print(f"   ✅ {feature}")
        
        if disabled:
            print("\n❌ Disabled Features:")
            for feature in disabled:
                print(f"   ❌ {feature}")
        
        if self.minimal_tooling:
            print("   ⚡ Using minimal tooling setup")
        
        print("=" * 50)