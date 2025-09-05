# Monorepo Bootstrap Tool

A powerful, feature-toggleable monorepo generator that creates production-ready full-stack projects with FastAPI backends and modern frontend frameworks (React, Vue, Svelte).

## 🚀 Quick Start

```bash
# Create a full-featured monorepo
python3 monorepo_bootstrap.py my_awesome_app

# Create a minimal API-only project
python3 monorepo_bootstrap.py simple_api --no-database --no-cache --no-docker --minimal-tooling

# Create a Vue.js project without CI/CD
python3 monorepo_bootstrap.py vue_app --frontend vue --no-ci --no-testing
```

## 📋 Features

### ✅ **Always Included**
- **FastAPI Backend** with modern Python patterns
- **Modern Frontend** (React/Vue/Svelte) with TypeScript
- **Shared Types & Utilities** for monorepo consistency
- **Development Scripts** via Makefile and npm scripts
- **Production Build** configurations

### 🔧 **Toggleable Features**

#### Core Infrastructure
- **Database** (`--no-database`) - PostgreSQL with SQLAlchemy & Alembic migrations
- **Cache** (`--no-cache`) - Redis for caching and session storage  
- **Background Jobs** (`--no-celery`) - Celery task queue system
- **Docker** (`--no-docker`) - Full containerization with Docker Compose

#### Development & CI/CD
- **Testing** (`--no-testing`) - Pytest (backend) + Vitest/Jest (frontend)
- **CI/CD** (`--no-ci`) - GitHub Actions workflows with automated testing
- **VSCode Config** (`--no-vscode`) - Multi-root workspace with recommended extensions

#### Advanced Features  
- **Authentication** (`--no-auth`) - JWT-based auth endpoints and middleware
- **Type Generation** (`--no-type-gen`) - Auto-generate TypeScript types from Pydantic
- **Minimal Tooling** (`--minimal-tooling`) - Reduce linting/formatting tools to essentials

## 🎯 Usage Examples

### Full-Stack Application (Default)
```bash
python3 monorepo_bootstrap.py my_saas_app
```
**Includes:** Database, Redis, Celery, Docker, CI/CD, Testing, Auth, TypeScript generation

### Simple REST API
```bash
python3 monorepo_bootstrap.py api_server --no-docker --no-ci --no-testing --minimal-tooling
```
**Perfect for:** Internal APIs, microservices, prototypes

### Frontend-Heavy Application
```bash
python3 monorepo_bootstrap.py web_app --frontend vue --no-celery --no-cache
```
**Perfect for:** Content sites, dashboards, SPAs with simple backends

### Minimal Proof of Concept
```bash
python3 monorepo_bootstrap.py poc --no-database --no-cache --no-celery --no-docker --no-ci --no-testing --no-vscode --no-type-gen --no-auth --minimal-tooling
```
**Perfect for:** Quick prototypes, learning projects, demos

## 📁 Generated Project Structure

```
my_project/
├── backend/                 # FastAPI application
│   ├── src/app/
│   │   ├── api/v1/         # API endpoints
│   │   ├── core/           # Configuration & settings
│   │   ├── models/         # Database models (if --database)
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── tests/              # Backend tests (if --testing)
│   ├── alembic/            # DB migrations (if --database)
│   └── pyproject.toml      # Dependencies & config
├── frontend/               # React/Vue/Svelte app
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Route components
│   │   ├── services/       # API clients
│   │   ├── stores/         # State management
│   │   └── types/          # TypeScript definitions
│   └── package.json
├── shared/                 # Shared utilities & types
├── infrastructure/         # Docker & K8s configs (if --docker)
├── .github/workflows/      # CI/CD pipelines (if --ci)
├── .vscode/               # VSCode settings (if --vscode)
└── Makefile               # Development commands
```

## 🛠️ Development Workflow

### Initial Setup
```bash
cd my_project
make install              # Install all dependencies
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### With Docker (Default)
```bash
make docker-up           # Start database & Redis
make migrate             # Run database migrations (if database enabled)
make dev                 # Start all services
```

### Without Docker
```bash
# Start services individually
make dev-backend         # FastAPI server on :8000
make dev-frontend        # Frontend dev server on :3000
```

### Common Commands
```bash
make test               # Run all tests
make lint               # Run all linters  
make format             # Format all code
make types              # Generate TypeScript types (if enabled)
make help               # Show all available commands
```

## 🎨 Frontend Framework Support

### React (Default)
- React 18 with TypeScript
- Vite for fast development
- TanStack Query for API state management
- React Router for client-side routing

### Vue.js
```bash
python3 monorepo_bootstrap.py my_app --frontend vue
```
- Vue 3 Composition API with TypeScript
- Pinia for state management
- Vue Router for navigation
- Comprehensive component examples

### Svelte (Coming Soon)
```bash
python3 monorepo_bootstrap.py my_app --frontend svelte
```
- SvelteKit with TypeScript
- Native Svelte stores
- Built-in routing

## 🏗️ Architecture Highlights

### Backend (FastAPI)
- **Clean Architecture** with separated layers
- **Async/Await** throughout for performance
- **Pydantic** for data validation and serialization
- **SQLAlchemy 2.0** with async support (if database enabled)
- **Structured Logging** with contextual information
- **Health Checks** and monitoring endpoints

### Frontend
- **TypeScript** for type safety
- **Modern Bundling** with Vite
- **API Integration** with auto-generated types
- **State Management** (Zustand/Pinia/Svelte stores)
- **Responsive Design** ready

### Development Experience
- **Hot Reload** for both backend and frontend
- **Type Safety** end-to-end with shared schemas
- **Linting & Formatting** with Ruff (Python) and ESLint/Prettier (JavaScript)
- **Pre-commit Hooks** to maintain code quality
- **Multi-root VSCode** workspace for optimal DX

## 🔧 Customization

### Environment Variables

**Backend (.env)**
```env
ENVIRONMENT=development
DATABASE_URL=postgresql://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
```

**Frontend (.env)**
```env
VITE_API_URL=http://localhost:8000/api/v1
```

### Adding Features Later

The architecture supports easy feature addition:

1. **Database**: Add SQLAlchemy models and Alembic migrations
2. **Authentication**: Extend the auth endpoints and add middleware
3. **Background Jobs**: Create Celery tasks in `backend/src/app/tasks/`
4. **New Endpoints**: Add routers in `backend/src/app/api/v1/endpoints/`

## 📦 Dependencies

### Python (Backend)
- **Core**: FastAPI, Uvicorn, Pydantic
- **Database**: SQLAlchemy, Alembic, AsyncPG (if enabled)
- **Auth**: python-jose, passlib (if enabled)  
- **Tasks**: Celery (if enabled)
- **Cache**: Redis (if enabled)
- **Dev**: Ruff, mypy, pytest

### Node.js (Frontend)
- **Core**: React/Vue/Svelte, TypeScript, Vite
- **State**: TanStack Query, Zustand/Pinia
- **Dev**: ESLint, Prettier, Vitest (if testing enabled)

## 🚀 Deployment

### Docker Production
```bash
make build              # Build production images
docker-compose -f infrastructure/docker/docker-compose.yml up
```

### Manual Deployment
```bash
# Backend
cd backend && poetry install --only=main
poetry run uvicorn src.app.main:app --host 0.0.0.0 --port 8000

# Frontend  
cd frontend && npm ci && npm run build
# Serve dist/ with your web server
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💡 Tips & Best Practices

### Feature Selection Guidelines

- **Start Minimal**: Use `--minimal-tooling` and disable unused features for faster development
- **Add Gradually**: Enable features as your project grows (database → cache → background jobs)
- **Consider Environment**: Disable Docker for simple deployment environments
- **Team Size**: Larger teams benefit from full CI/CD and testing setup

### Performance Optimizations

- **Database**: Use `--no-database` for API gateways or stateless services
- **Cache**: Essential for session-heavy or data-intensive applications  
- **Background Jobs**: Only needed for email, file processing, or long-running tasks

### Development Experience

- **VSCode**: Multi-root workspace provides excellent monorepo support
- **Type Generation**: Keeps frontend and backend in sync automatically
- **Hot Reload**: Both backend and frontend support live reloading

---

**Happy coding!** 🎉

For questions or issues, please open a GitHub issue or check the documentation in the generated project's README.