# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains development tools for bootstrapping modern web application projects. The main tool is:

1. **Monorepo Bootstrap Script** (`monorepo_bootstrap.py`) - Creates complete full-stack monorepos with FastAPI backends and modern frontend frameworks (React, Vue, Svelte)

## Key Commands

### Running the Bootstrap Scripts

```bash
# Create a new monorepo with React frontend (default)
python3 monorepo_bootstrap.py my_project

# Create a monorepo with Vue frontend  
python3 monorepo_bootstrap.py my_project --frontend vue

# Create a monorepo with Svelte frontend
python3 monorepo_bootstrap.py my_project --frontend svelte

# Get help for available options
python3 monorepo_bootstrap.py --help
```

### Python Environment

```bash
# Use venv from the project root when working with these scripts
source venv/bin/activate  # if venv exists
# Or create one if needed:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # if requirements file exists
```

## Architecture and Patterns

### Monorepo Bootstrap (`monorepo_bootstrap.py`)

This script creates production-ready monorepos with the following structure:
- **Backend**: FastAPI with Poetry, structured using clean architecture patterns
- **Frontend**: React/Vue/Svelte with TypeScript, modern tooling (Vite, ESLint, Prettier)
- **Shared**: Common types and utilities
- **Infrastructure**: Docker, Kubernetes, and CI/CD configurations
- **Development**: VSCode workspace, Makefile, and development scripts

Key architectural decisions:
- Uses Poetry for Python dependency management
- Implements monorepo workspace pattern with npm/yarn workspaces
- Follows clean architecture with separate layers (API, services, models, schemas)
- TypeScript types auto-generated from Pydantic schemas
- Comprehensive testing setup (pytest for backend, Vitest/Jest for frontend)
- Docker containerization for all services
- GitHub Actions CI/CD pipeline

### Generated Project Commands

The bootstrap script generates projects with these standard commands:
```bash
# In generated monorepo root:
make install     # Install all dependencies
make dev         # Start all services in development
make test        # Run all tests
make lint        # Run all linters  
make format      # Format all code
make build       # Build for production
make types       # Generate TypeScript types from Pydantic schemas
```

### Frontend Framework Support

The bootstrap script supports multiple frontend frameworks with full feature parity:

**Vue.js Frontend (`--frontend vue`)**:
- Vue 3 Composition API with TypeScript
- Pinia for state management
- Vue Router for client-side routing
- Vite for build tooling
- Authentication store patterns
- API service integration
- Component examples (LoginView, HomeView, DashboardView)

**React Frontend (`--frontend react`)**:
- React 18 with TypeScript
- Zustand for state management
- React Router for client-side routing
- Tanstack Query for API state management
- Vite for build tooling
- Authentication patterns
- API service integration

**Svelte Frontend (`--frontend svelte`)**:
- SvelteKit with TypeScript (planned)
- Native Svelte stores for state management
- Built-in routing
- Vite for build tooling

## Development Workflow

When modifying these bootstrap scripts:

1. Test script execution with different frontend options
2. Verify generated project structure follows expected patterns
3. Ensure all generated files have proper syntax and imports
4. Test the generated projects can be built and run successfully
5. Update version numbers and dependencies as needed

## Common Issues

- Ensure Python 3.12+ is available when running scripts
- Generated projects require Node.js 18+ and Poetry for full functionality
- Docker and Docker Compose needed for infrastructure components
- VSCode extensions recommended for optimal development experience in generated projects