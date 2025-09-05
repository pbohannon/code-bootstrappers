#!/usr/bin/env python3
"""
Monorepo Bootstrap Script for FastAPI + Frontend Projects
Creates a production-ready monorepo with backend, frontend, and shared components.

Usage: python bootstrap_monorepo.py <project_name> [--frontend react|vue|svelte]
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, Any, Literal
import textwrap

# Import our specialized generators and feature configuration
from generators import (
    BackendGenerator,
    InfrastructureGenerator,
    ReactFrontendGenerator,
    VueFrontendGenerator,
)
from feature_config import FeatureConfig


class MonorepoBootstrapper:
    def __init__(self, project_name: str, frontend_type: str = "react", features: FeatureConfig = None):
        self.project_name = project_name.lower().replace(" ", "_").replace("-", "_")
        self.project_dir = Path(self.project_name)
        self.frontend_type = frontend_type
        self.features = features or FeatureConfig()
        
        # Initialize generators with feature configuration
        self.backend_generator = BackendGenerator(self.project_name, self.project_dir, self.features)
        self.infrastructure_generator = InfrastructureGenerator(self.project_name, self.project_dir, self.features)
        
        if self.frontend_type == "react":
            self.frontend_generator = ReactFrontendGenerator(self.project_name, self.project_dir, self.features)
        elif self.frontend_type == "vue":
            self.frontend_generator = VueFrontendGenerator(self.project_name, self.project_dir, self.features)
        else:
            self.frontend_generator = ReactFrontendGenerator(self.project_name, self.project_dir, self.features)  # Default
    
    def _use_template(self, template_name: str, output_name: str = None) -> str:
        """Load and use a template file."""
        template_path = Path(__file__).parent / "templates" / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template {template_name} not found")
        
        content = template_path.read_text()
        
        if output_name:
            (self.project_dir / output_name).write_text(content)
        
        return content

    def create_directory_structure(self):
        """Create the monorepo directory structure based on enabled features."""
        print("📁 Creating monorepo directory structure...")

        # Core directories always created
        core_directories = [
            # Backend core directories
            "backend/src/app/api/v1/endpoints",
            "backend/src/app/core",
            "backend/src/app/schemas",
            "backend/src/app/services",
            "backend/src/app/utils",

            # Frontend core directories
            "frontend/src/components",
            "frontend/src/pages", 
            "frontend/src/services",
            "frontend/src/hooks",
            "frontend/src/utils",
            "frontend/src/types",
            "frontend/src/router",
            "frontend/src/stores",
            "frontend/src/views",
            "frontend/src/assets",
            "frontend/public",

            # Shared directories
            "shared/types",
            "shared/constants", 
            "shared/utils",

            # Scripts and tools
            "scripts/development",
            "tools",
        ]

        # Feature-specific directories
        feature_directories = []
        
        if self.features.database:
            feature_directories.extend([
                "backend/src/app/models",
                "backend/alembic/versions",
            ])
        
        if self.features.testing:
            feature_directories.extend([
                "backend/tests/unit",
                "backend/tests/integration", 
                "backend/tests/fixtures",
            ])
        
        if self.features.docker:
            feature_directories.extend([
                "infrastructure/docker",
                "infrastructure/kubernetes",
                "infrastructure/terraform",
                "scripts/deployment",
            ])
        
        if self.features.ci_cd:
            feature_directories.extend([
                ".github/workflows",
            ])
        
        if self.features.vscode:
            feature_directories.extend([
                ".vscode",
            ])

        # Create all applicable directories
        all_directories = core_directories + feature_directories
        
        for directory in all_directories:
            if self.features.should_create_directory(directory):
                (self.project_dir / directory).mkdir(parents=True, exist_ok=True)

                # Add __init__.py files for Python packages
                if "backend/" in directory and ("src/" in directory or "tests/" in directory):
                    init_file = self.project_dir / directory / "__init__.py"
                    init_file.touch()

    def create_root_config_files(self):
        """Create root-level configuration files using templates."""
        print("📝 Creating root configuration files...")

        # Root package.json for workspace management with feature-based scripts
        scripts = {
            "install:all": "npm install && cd backend && poetry install",
            "dev:backend": "cd backend && poetry run uvicorn src.app.main:app --reload",
            "dev:frontend": "cd frontend && npm run dev",
            "build:frontend": "cd frontend && npm run build",
            "clean": "find . -type d -name '__pycache__' -exec rm -rf {} + && find . -type d -name 'node_modules' -exec rm -rf {} +",
        }
        
        # Conditional scripts based on features
        if self.features.docker:
            scripts["dev"] = "docker-compose -f infrastructure/docker/docker-compose.dev.yml up"
            scripts["build:backend"] = "cd backend && docker build -t backend ."
            scripts["build"] = "npm run build:backend && npm run build:frontend"
        else:
            scripts["dev"] = "concurrently \"npm run dev:backend\" \"npm run dev:frontend\""
            scripts["build"] = "npm run build:frontend"
        
        if self.features.testing:
            scripts.update({
                "test": "npm run test:backend && npm run test:frontend",
                "test:backend": "cd backend && poetry run pytest", 
                "test:frontend": "cd frontend && npm test",
            })
        
        if not self.features.minimal_tooling:
            scripts.update({
                "lint": "npm run lint:backend && npm run lint:frontend",
                "lint:backend": "cd backend && poetry run ruff check src tests",
                "lint:frontend": "cd frontend && npm run lint",
                "format": "npm run format:backend && npm run format:frontend",
                "format:backend": "cd backend && poetry run ruff format src tests", 
                "format:frontend": "cd frontend && npm run format",
            })
        
        if self.features.type_generation:
            scripts["generate:types"] = "cd backend && python scripts/generate_types.py"
        
        # Get dev dependencies based on features
        dev_deps = self.features.get_root_dev_dependencies()
        
        root_package_json = {
            "name": f"{self.project_name}-monorepo",
            "version": "0.1.0",
            "private": True,
            "workspaces": [
                "frontend",
                "shared"
            ],
            "scripts": scripts,
            "devDependencies": dev_deps,
        }
        
        # Add git hooks configuration only if not minimal tooling
        if not self.features.minimal_tooling:
            root_package_json.update({
                "husky": {
                    "hooks": {
                        "pre-commit": "lint-staged"
                    }
                },
                "lint-staged": {
                    "*.py": [
                        "cd backend && poetry run ruff format",
                        "cd backend && poetry run ruff check --fix"
                    ],
                    "*.{js,jsx,ts,tsx}": [
                        "cd frontend && npm run lint:fix",
                        "cd frontend && npm run format"
                    ]
                }
            })

        (self.project_dir / "package.json").write_text(
            json.dumps(root_package_json, indent=2)
        )

        # Use template files for larger configurations
        self._use_template("makefile.template", "Makefile")
        self._use_template("gitignore.template", ".gitignore")
        
        # Use template for README with substitutions
        readme_content = self._use_template("readme.template", None)
        readme_content = readme_content.replace("{project_name}", self.project_name)
        readme_content = readme_content.replace("{project_title}", self.project_name.replace("_", " ").title())
        readme_content = readme_content.replace("{frontend_type}", self.frontend_type.title())
        (self.project_dir / "README.md").write_text(readme_content)

    def create_backend_structure(self):
        """Create the backend structure using BackendGenerator."""
        self.backend_generator.create_structure()

    def create_frontend_structure(self):
        """Create frontend structure using the appropriate generator."""
        self.frontend_generator.create_structure()

    def create_infrastructure_files(self):
        """Create infrastructure configuration files using InfrastructureGenerator."""
        self.infrastructure_generator.create_docker_files()

    def create_vscode_settings(self):
        """Create VSCode workspace settings using InfrastructureGenerator."""
        self.infrastructure_generator.create_vscode_settings()

    def create_github_workflows(self):
        """Create GitHub Actions workflows using InfrastructureGenerator."""
        self.infrastructure_generator.create_github_workflows()

    def create_shared_utilities(self):
        """Create shared utilities and types."""
        print("🔗 Creating shared utilities...")

        # Shared constants
        constants_content = '''"""
Shared constants used across the monorepo.
"""

# API endpoints
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# Status codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_500_INTERNAL_SERVER_ERROR = 500

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Cache TTL (in seconds)
CACHE_TTL_SHORT = 60  # 1 minute
CACHE_TTL_MEDIUM = 300  # 5 minutes
CACHE_TTL_LONG = 3600  # 1 hour
'''

        (self.project_dir / "shared" / "constants" / "__init__.py").write_text(constants_content)

        # Shared TypeScript types
        shared_types = '''/**
 * Shared TypeScript types and interfaces.
 * These are manually defined types that complement the auto-generated ones.
 */

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface ApiError {
  detail: string;
  status: number;
  timestamp: string;
  path: string;
}

export type SortDirection = 'asc' | 'desc';

export interface QueryParams {
  page?: number;
  size?: number;
  sort?: string;
  direction?: SortDirection;
  search?: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token?: string;
  token_type: string;
  expires_in: number;
}

export interface User {
  id: string;
  email: string;
  username: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}
'''

        (self.project_dir / "shared" / "types" / "index.ts").write_text(shared_types)

    def run(self):
        """Execute the monorepo bootstrap process."""
        self.features.print_summary(self.project_name, self.frontend_type)

        self.create_directory_structure()
        self.create_root_config_files()
        self.create_backend_structure()
        self.create_frontend_structure()
        
        if self.features.docker:
            self.create_infrastructure_files()
        
        if self.features.vscode:
            self.create_vscode_settings()
        
        if self.features.ci_cd:
            self.create_github_workflows()
        
        self.create_shared_utilities()

        print("\n✅ Monorepo structure created successfully!")
        self._print_next_steps()

    def _print_next_steps(self):
        """Print contextual next steps based on enabled features."""
        print("\n📚 Next steps:")
        print(f"  1. cd {self.project_name}")
        print("  2. make install  # Install all dependencies")
        print("  3. cp backend/.env.example backend/.env")
        print("  4. cp frontend/.env.example frontend/.env")
        
        step = 5
        if self.features.docker and self.features.database:
            print(f"  {step}. make docker-up  # Start database and Redis")
            step += 1
            print(f"  {step}. make migrate  # Run database migrations")
            step += 1
        elif self.features.database:
            print(f"  {step}. # Set up your database (PostgreSQL recommended)")
            step += 1
            print(f"  {step}. make migrate  # Run database migrations")
            step += 1
        
        print(f"  {step}. make dev  # Start all services")
        
        print("\n🌐 Services will be available at:")
        print("  - Backend API: http://localhost:8000")
        print("  - API Docs: http://localhost:8000/docs")
        print("  - Frontend: http://localhost:3000")
        
        if self.features.docker and self.features.database:
            print("  - Database Admin: http://localhost:8080")
        
        print("\n💡 Pro tips:")
        if self.features.vscode:
            print("  - Open the workspace file in VSCode for multi-root setup")
        if self.features.type_generation:
            print("  - Run 'make types' to generate TypeScript types from Pydantic")
        print("  - Use 'make help' to see all available commands")
        
        if self.features.testing:
            print("\n🧪 Testing:")
            print("  - make test  # Run all tests")
            print("  - make test-backend  # Backend only")
            print("  - make test-frontend  # Frontend only")
        
        print("\nHappy coding! 🎉")


def main():
    parser = argparse.ArgumentParser(
        description="Bootstrap a monorepo with toggleable features",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 monorepo_bootstrap.py my_app
  python3 monorepo_bootstrap.py my_api --no-database --no-cache --frontend vue
  python3 monorepo_bootstrap.py minimal_app --no-docker --no-ci --no-testing
  python3 monorepo_bootstrap.py full_stack --frontend react
        """
    )
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument(
        "--frontend",
        choices=["react", "vue", "svelte"],
        default="react",
        help="Frontend framework to use (default: react)"
    )
    
    # Core feature toggles
    core_group = parser.add_argument_group('Core Infrastructure')
    core_group.add_argument("--no-database", action="store_true", 
                           help="Skip database setup (PostgreSQL, SQLAlchemy, Alembic)")
    core_group.add_argument("--no-cache", action="store_true", 
                           help="Skip Redis cache setup")
    core_group.add_argument("--no-celery", action="store_true", 
                           help="Skip Celery background job setup")
    core_group.add_argument("--no-docker", action="store_true", 
                           help="Skip Docker configuration files")
    
    # Development & CI toggles
    dev_group = parser.add_argument_group('Development & CI/CD')
    dev_group.add_argument("--no-ci", action="store_true", 
                          help="Skip GitHub Actions CI/CD workflows")
    dev_group.add_argument("--no-testing", action="store_true", 
                          help="Skip testing framework setup")
    dev_group.add_argument("--no-vscode", action="store_true", 
                          help="Skip VSCode workspace configuration")
    
    # Advanced feature toggles
    advanced_group = parser.add_argument_group('Advanced Features')
    advanced_group.add_argument("--no-type-gen", action="store_true", 
                               help="Skip TypeScript type generation from Pydantic")
    advanced_group.add_argument("--no-auth", action="store_true", 
                               help="Skip authentication endpoints and JWT setup")
    advanced_group.add_argument("--minimal-tooling", action="store_true", 
                               help="Use minimal linting/formatting tools")

    args = parser.parse_args()
    
    # Create feature configuration
    features = FeatureConfig.from_args(args)
    bootstrapper = MonorepoBootstrapper(args.project_name, args.frontend, features)

    # Check if directory already exists
    if bootstrapper.project_dir.exists():
        response = input(f"Directory '{args.project_name}' already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Aborting.")
            sys.exit(0)

    bootstrapper.run()


if __name__ == "__main__":
    main()
