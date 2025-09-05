# FastAPI Patterns Guide for LLMs

## Required Stack
- FastAPI 0.100+
- Pydantic V2 (2.0+)
- SQLModel 0.0.8+
- SQLAlchemy 2.0
- Uvicorn + Gunicorn

## CORRECT Patterns

### 1. Layered Architecture
```python
# DO: Router → Service → Repository
@router.post("/users/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.create_user(user_data)

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, user_data: UserCreate) -> User:
        if await self.user_repo.email_exists(user_data.email):
            raise HTTPException(status_code=400, detail="Email exists")
        return await self.user_repo.create(user_data)

class UserRepository:
    async def create(self, user_data: UserCreate) -> User:
        db_user = User(**user_data.dict())
        self.session.add(db_user)
        await self.session.commit()
        return db_user
```

### 2. Async Everything
```python
# DO: Full async chain
async def get_user_with_posts(user_id: int, db: AsyncSession):
    user = await db.get(User, user_id)
    posts = await db.execute(select(Post).where(Post.user_id == user_id))
    return user, posts.scalars().all()
```

### 3. Dependency Injection
```python
# DO: Use Depends() for all dependencies
@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await user_service.get_user(user_id)
```

### 4. Pydantic Models
```python
# DO: Strong validation
class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    age: conint(ge=18, le=120)

    @field_validator('password')
    def validate_password(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain digit')
        return v
```

### 5. Background Tasks
```python
# DO: Offload slow operations
@router.post("/notify/")
async def notify_user(
    email: EmailStr,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Queued"}
```

### 6. Error Handling
```python
# DO: Custom exceptions with proper status codes
class UserNotFoundError(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=404,
            detail=f"User {user_id} not found"
        )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc), "type": "value_error"}
    )
```

## INCORRECT Antipatterns

### 1. Blocking Operations
```python
# DON'T: Sync operations in async routes
@app.get("/users")
async def get_users():
    time.sleep(1)  # ❌ Blocks entire event loop
    users = sync_database.query("SELECT * FROM users")  # ❌ Blocking
    return users

# DO: Async operations only
@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    await asyncio.sleep(1)  # ✅ Non-blocking
    return await db.execute(select(User)).scalars().all()
```

### 2. No Dependency Injection
```python
# DON'T: Manual resource management
@app.get("/users")
async def get_users():
    db = create_database_connection()  # ❌ Manual connection
    try:
        users = db.query("SELECT * FROM users")
        return users
    finally:
        db.close()  # ❌ Manual cleanup

# DO: Use Depends()
@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

### 3. No Validation
```python
# DON'T: Accept raw dicts
@app.post("/users")
async def create_user(user_data: dict):  # ❌ No validation
    if "email" not in user_data:
        raise HTTPException(400, "Email required")
    return user_data

# DO: Use Pydantic models
class UserCreate(BaseModel):
    email: EmailStr
    age: conint(ge=18)

@app.post("/users")
async def create_user(user_data: UserCreate):  # ✅ Auto validation
    return user_data
```

### 4. Fat Controllers
```python
# DON'T: Business logic in routes
@app.post("/orders")
async def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    # ❌ 50+ lines of business logic in controller
    user = db.query(User).filter(User.id == order_data.user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    # ... many more lines

# DO: Use service layer
@app.post("/orders")
async def create_order(
    order_data: OrderCreate,
    order_service: OrderService = Depends(get_order_service)
):
    return await order_service.create_order(order_data)
```

### 5. Poor Error Handling
```python
# DON'T: Return None or let errors bubble
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return user  # ❌ Returns None if not found

# DO: Proper error responses
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, f"User {user_id} not found")
    return user
```

### 6. Sync Dependencies
```python
# DON'T: Sync dependencies with async routes
def get_db():  # ❌ Sync dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# DO: Async dependencies
async def get_db():  # ✅ Async dependency
    async with AsyncSessionLocal() as session:
        yield session
```



## Production Essentials
```python
# Rate limiting
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.get("/api/data")
@limiter.limit("10/minute")
async def get_data(request: Request):
    return {"data": "value"}

# Caching
@app.get("/expensive")
@cache(expire=60)
async def expensive_operation():
    return result

# Multiple workers
# gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Common Linting Violations (Ruff/Flake8)

### Import Organization
```python
# DON'T: Wrong import order
import os
from fastapi import FastAPI
import sys
from pydantic import BaseModel

# DO: Correct order (stdlib, third-party, local)
import os
import sys

from fastapi import FastAPI
from pydantic import BaseModel

from .models import User
```

### Unused Imports/Variables
```python
# DON'T: Unused imports/variables
import json  # ❌ Unused import
from typing import Dict, List  # ❌ Dict unused

async def get_users() -> List[User]:
    result = await db.execute(select(User))  # ❌ result unused
    users = result.scalars().all()
    temp_var = "hello"  # ❌ Unused variable
    return users

# DO: Only import what you use
from typing import List

async def get_users() -> List[User]:
    result = await db.execute(select(User))
    return result.scalars().all()
```

### Type Annotations
```python
# DON'T: Missing type hints
def process_user(user_data):  # ❌ No type hints
    return user_data

async def get_users():  # ❌ No return type
    return await db.execute(select(User))

# DO: Proper type annotations
def process_user(user_data: dict[str, Any]) -> dict[str, Any]:
    return user_data

async def get_users() -> list[User]:
    result = await db.execute(select(User))
    return result.scalars().all()
```

### Line Length & Formatting
```python
# DON'T: Lines too long (>88 chars)
async def create_user_with_profile(user_data: UserCreate, profile_data: ProfileCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)) -> UserResponse:  # ❌ Too long

# DO: Break long lines
async def create_user_with_profile(
    user_data: UserCreate,
    profile_data: ProfileCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    pass
```

### Exception Handling
```python
# DON'T: Bare except clauses
try:
    user = await get_user(user_id)
except:  # ❌ Bare except
    pass

try:
    user = await get_user(user_id)
except Exception as e:  # ❌ Too broad
    pass

# DO: Specific exception handling
try:
    user = await get_user(user_id)
except UserNotFoundError:
    raise HTTPException(404, "User not found")
except ValidationError as e:
    raise HTTPException(400, str(e))
```

### String Formatting
```python
# DON'T: Old-style formatting
name = "John"
message = "Hello %s" % name  # ❌ % formatting
message = "Hello {}".format(name)  # ❌ .format()

# DO: f-strings
message = f"Hello {name}"  # ✅ f-string
```

### Mutable Default Arguments
```python
# DON'T: Mutable defaults
async def process_items(items: list = []):  # ❌ Mutable default
    items.append("new")
    return items

# DO: Use None with conditional
async def process_items(items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append("new")
    return items
```

## Security Checklist
- ✅ OAuth2/JWT auth
- ✅ Rate limiting on all endpoints
- ✅ CORS properly configured (not `["*"]`)
- ✅ Input validation with Pydantic
- ✅ Password hashing with bcrypt
- ✅ HTTPS only in production
- ✅ Environment variables for secrets
