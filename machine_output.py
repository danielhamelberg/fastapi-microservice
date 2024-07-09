data = '''
{
"response_type": "file_structure_and_contents",
"file_structure": [
{
"path": "/",
"files": [
"README.md",
"requirements.txt",
"setup.py",
".gitignore",
"Dockerfile",
".dockerignore",
"docker-compose.yml",
".flake8",
"pyproject.toml"
]
},
{
"path": "/src",
"files": [
"main.py",
"database.py",
"models.py",
"schemas.py"
]
},
{
"path": "/src/auth",
"files": [
"utils.py",
"decorators.py"
]
},
{
"path": "/src/repositories",
"files": [
"base.py",
"user_repository.py",
"post_repository.py"
]
},
{
"path": "/src/services",
"files": [
"post_service.py"
]
},
{
"path": "/src/core",
"files": [
"logging.py"
]
},
{
"path": "/tests",
"files": [
"conftest.py",
"test_auth.py",
"test_posts.py"
]
},
{
"path": "/scripts",
"files": [
"run_migrations.py"
]
},
{
"path": "/.github/workflows",
"files": [
"ci-cd.yml"
]
}
],
"file_contents": {
"/README.md": "# FastAPI Microservice Project\\n\\nCI/CD\\n\\nThis project is a microservice built with FastAPI.\\n\\n## API Documentation\\n\\nThe API documentation is automatically generated and can be accessed at the following endpoints:\\n\\n- Swagger UI: /docs\\n- OpenAPI JSON: /openapi.json\\n\\nThese endpoints provide detailed information about the available API routes, request/response models, and authentication requirements.\\n\\n## Development\\n\\n...\\n\\n## Deployment\\n\\n...",
"/requirements.txt": "fastapi\\nuvicorn\\nsqlalchemy\\npydantic\\npython-jose[cryptography]\\npasslib[bcrypt]\\npytest\\nhttpx\\nloguru\\nprometheus-fastapi-instrumentator\\nflake8\\nblack",
"/setup.py": "from setuptools import setup, find_packages\\n\\nsetup(\\nname="fastapi-microservice",\\n version="0.1.0",\\n packages=find_packages(),\\n install_requires=[\\n "fastapi",\\n "uvicorn",\\n "sqlalchemy",\\n "pydantic",\\n ],\\n)"",
"/.gitignore": "pycache\\n*.pyc\\n.venv\\n.env",
"/Dockerfile": "# Use an official Python runtime as a parent image\\nFROM python:3.10-slim\\n\\n# Set the working directory in the container\\nWORKDIR /app\\n\\n# Copy the current directory contents into the container at /app\\nCOPY . /app\\n\\n# Install any needed packages specified in requirements.txt\\nRUN pip install --no-cache-dir -r requirements.txt\\n\\n# Make port 8000 available to the world outside this container\\nEXPOSE 8000\\n\\n# Define environment variable\\nENV NAME World\\n\\n# Run app.py when the container launches\\nCMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]",
"/.dockerignore": ".git\\n.gitignore\\n.vscode\\n__pycache__\\n*.pyc\\n*.pyo\\n*.pyd\\n.Python\\nenv\\npip-log.txt\\npip-delete-this-directory.txt\\n.tox\\n.coverage\\n.coverage.\\n.cache\\nnosetests.xml\\ncoverage.xml\\n.cover\\n*.log\\n.mypy_cache\\n.pytest_cache\\n.hypothesis",
"/docker-compose.yml": "version: '3.8'\\n\\nservices:\\n web:\\n build: .\\n command: uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload\\n volumes:\\n - .:/app\\n ports:\\n - "8000:8000"\\n environment:\\n - DATABASE_URL=sqlite:///./test.db",
"/.flake8": "[flake8]\\nmax-line-length = 100\\nexclude = .git,pycache,docs/source/conf.py,old,build,dist",
"/pyproject.toml": "[tool.black]\\nline-length = 100\\ntarget-version = ['py310']\\ninclude = '\.pyi?$'\\nextend-exclude = ---\\n/(\\n # directories\\n \.eggs\\n | \.git\\n | \.hg\\n | \.mypy_cache\\n | \.tox\\n | \.venv\\n | build\\n | dist\\n)/\\n---",
"/src/main.py": "from fastapi import FastAPI, Depends, HTTPException, status, Request\\nfrom fastapi.responses import JSONResponse\\nfrom fastapi.openapi.docs import get_swagger_ui_html\\nfrom fastapi.openapi.utils import get_openapi\\nfrom sqlalchemy.orm import Session\\nfrom typing import List\\n\\nfrom .database import engine, get_db\\nfrom . import models, schemas\\nfrom .auth.utils import get_current_active_user\\nfrom .auth.decorators import admin_required, moderator_required\\nfrom .services.post_service import PostService\\nfrom .core.logging import setup_logging\\nfrom scripts.run_migrations import run_migrations\\n\\nlogger = setup_logging()\\nmodels.Base.metadata.create_all(bind=engine)\\n\\napp = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)\\n\\n@app.middleware("http")\\nasync def log_requests(request: Request, call_next):\\n logger.info(f"Incoming request: {request.method} {request.url}")\\n response = await call_next(request)\\n logger.info(f"Outgoing response: {response.status_code}")\\n return response\\n\\n@app.get("/docs", include_in_schema=False)\\nasync def custom_swagger_ui_html():\\n return get_swagger_ui_html(\\n openapi_url="/openapi.json",\\n title="API Documentation",\\n oauth2_redirect_url="/docs/oauth2-redirect",\\n swagger_js_url="/static/swagger-ui-bundle.js",\\n swagger_css_url="/static/swagger-ui.css",\\n )\\n\\n@app.get("/openapi.json", include_in_schema=False)\\nasync def get_open_api_endpoint():\\n return get_openapi(\\n title="FastAPI Microservice",\\n version="1.0.0",\\n description="This is a microservice built with FastAPI",\\n routes=app.routes,\\n )\\n\\n@app.post("/posts", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)\\nasync def create_post(\\n post: schemas.PostCreate,\\n db: Session = Depends(get_db),\\n current_user: models.User = Depends(get_current_active_user)\\n):\\n 
"/src/database.py": "import os\\nfrom sqlalchemy import create_engine\\nfrom sqlalchemy.orm import sessionmaker\\nfrom sqlalchemy.ext.declarative import declarative_base\\n\\nSQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")\\n\\nengine = create_engine(\\n SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}\\n)\\nSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)\\n\\nBase = declarative_base()\\n\\ndef get_db():\\n db = SessionLocal()\\n try:\\n yield db\\n finally:\\n db.close()",
"/src/models.py": "from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum\\nfrom sqlalchemy.orm import relationship\\nfrom datetime import datetime\\nimport enum\\n\\nclass UserRole(enum.Enum):\\n ADMIN = "admin"\\n MODERATOR = "moderator"\\n USER = "user"\\n\\nclass User(Base):\\n tablename = 'users'\\n\\n id = Column(Integer, primary_key=True, index=True)\\n username = Column(String(50), unique=True, index=True)\\n email = Column(String(100), unique=True, index=True)\\n hashed_password = Column(String(100))\\n role = Column(Enum(UserRole), default=UserRole.USER)\\n created_at = Column(DateTime, default=datetime.utcnow)\\n posts = relationship("Post", back_populates="author")\\n\\nclass Post(Base):\\n tablename = 'posts'\\n\\n id = Column(Integer, primary_key=True, index=True)\\n title = Column(String(100), index=True)\\n content = Column(String(1000))\\n author_id = Column(Integer, ForeignKey('users.id'))\\n created_at = Column(DateTime, default=datetime.utcnow)\\n author = relationship("User", back_populates="posts")",
"/src/schemas.py": "from pydantic import BaseModel\\nfrom datetime import datetime\\nfrom typing import Optional\\n\\nclass PostBase(BaseModel):\\n title: str\\n content: str\\n\\nclass PostCreate(PostBase):\\n pass\\n\\nclass PostUpdate(PostBase):\\n pass\\n\\nclass PostResponse(PostBase):\\n id: int\\n author_id: int\\n created_at: datetime\\n\\n class Config:\\n orm_mode = True",
"/src/auth/utils.py": "from datetime import datetime, timedelta\\nfrom typing import Optional\\nfrom jose import JWTError, jwt\\nfrom passlib.context import CryptContext\\nfrom fastapi import Depends, HTTPException, status\\nfrom fastapi.security import OAuth2PasswordBearer\\nfrom sqlalchemy.orm import Session\\n\\nfrom src.database import get_db\\nfrom src.repositories.user_repository import UserRepository\\nfrom src.models import User\\n\\nSECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"\\nALGORITHM = "HS256"\\nACCESS_TOKEN_EXPIRE_MINUTES = 30\\n\\npwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")\\noauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")\\n\\ndef verify_password(plain_password, hashed_password):\\n return pwd_context.verify(plain_password, hashed_password)\\n\\ndef get_password_hash(password):\\n return pwd_context.hash(password)\\n\\ndef authenticate_user(db: Session, username: str, password: str):\\n user_repo = UserRepository(db)\\n user = user_repo.get_by_username(username)\\n if not user:\\n return False\\n if not verify_password(password, user.hashed_password):\\n return False\\n return user\\n\\ndef create_access_token(data: dict, expires_delta: Optional[timedelta] = None):\\n to_encode = data.copy()\\n if expires_delta:\\n expire = datetime.utcnow() + expires_delta\\n else:\\n expire = datetime.utcnow() + timedelta(minutes=15)\\n to_encode.update({"exp": expire})\\n encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)\\n return encoded_jwt\\n\\nasync def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):\\n credentials_exception = HTTPException(\\n status_code=status.HTTP_401_UNAUTHORIZED,\\n detail="Could not validate credentials",\\n headers={"WWW-Authenticate": "Bearer"},\\n )\\n try:\\n payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])\\n username: str = payload.get("sub")\\n if username is None:\\n raise credentials_exception\\n except JWTError:\\n raise credentials_exception\\n user_repo = UserRepository(db)\\n user = user_repo.get_by_username(username)\\n if user is None:\\n raise credentials_exception\\n return user\\n\\nasync def get_current_active_user(current_user: User = Depends(get_current_user)):\\n if not current_user.is_active:\\n raise HTTPException(status_code=400, detail="Inactive user")\\n return current_user",
"/src/auth/decorators.py": "from functools import wraps\\nfrom fastapi import Depends\\nfrom .utils import get_current_active_user, check_user_role\\nfrom src.models import User, UserRole\\n\\ndef role_required(allowed_roles):\\n def decorator(func):\\n @wraps(func)\\n async def wrapper(*args, current_user: User = Depends(get_current_active_user), **kwargs):\\n check_user_role(current_user, allowed_roles)\\n return await func(*args, current_user=current_user, **kwargs)\\n return wrapper\\n return decorator\\n\\nadmin_required = role_required([UserRole.ADMIN])\\nmoderator_required = role_required([UserRole.ADMIN, UserRole.MODERATOR])",
"/src/repositories/base.py": "from typing import Generic, TypeVar, Type, List\\nfrom sqlalchemy.orm import Session\\nfrom sqlalchemy.exc import SQLAlchemyError\\nfrom fastapi import HTTPException\\n\\nT = TypeVar('T')\\n\\nclass BaseRepository(Generic[T]):\\n def init(self, model: Type[T], db: Session):\\n self.model = model\\n self.db = db\\n\\n def get(self, id: int) -> T:\\n return self.db.query(self.model).filter(self.model.id == id).first()\\n\\n def get_all(self) -> List[T]:\\n return self.db.query(self.model).all()\\n\\n def create(self, obj: T) -> T:\\n try:\\n self.db.add(obj)\\n self.db.commit()\\n self.db.refresh(obj)\\n return obj\\n except SQLAlchemyError as e:\\n self.db.rollback()\\n raise HTTPException(status_code=500, detail=str(e))\\n\\n def update(self, obj: T) -> T:\\n try:\\n self.db.commit()\\n self.db.refresh(obj)\\n return obj\\n except SQLAlchemyError as e:\\n self.db.rollback()\\n raise HTTPException(status_code=500, detail=str(e))\\n\\n def delete(self, id: int) -> bool:\\n obj = self.get(id)\\n if obj:\\n self.db.delete(obj)\\n self.db.commit()\\n return True\\n return False",
"/src/repositories/user_repository.py": "from .base import BaseRepository\\nfrom src.models import User\\n\\nclass UserRepository(BaseRepository[User]):\\n def get_by_username(self, username: str) -> User:\\n return self.db.query(self.model).filter(self.model.username == username).first()",
"/src/services/post_service.py": "from src.repositories.post_repository import PostRepository\\nfrom src.models import Post, User\\nfrom sqlalchemy.orm import Session\\nfrom typing import List\\nfrom src.core.logging import setup_logging\\n\\nlogger = setup_logging()\\n\\nclass PostService:\\n def init(self, db: Session):\\n self.post_repo = PostRepository(Post, db)\\n\\n def create_post(self, title: str, content: str, author: User) -> Post:\\n logger.info(f"Creating new post: {title} by user {author.username}")\\n new_post = Post(title=title, content=content, author_id=author.id)\\n return self.post_repo.create(new_post)\\n\\n def get_post(self, post_id: int) -> Post:\\n logger.info(f"Fetching post with id: {post_id}")\\n return self.post_repo.get(post_id)\\n\\n def update_post(self, post_id: int, title: str, content: str) -> Post:\\n logger.info(f"Updating post with id: {post_id}")\\n post = self.get_post(post_id)\\n if post:\\n post.title = title\\n post.content = content\\n return self.post_repo.update(post)\\n return None\\n\\n def delete_post(self, post_id: int) -> bool:\\n logger.info(f"Deleting post with id: {post_id}")\\n return self.post_repo.delete(post_id)\\n\\n def get_user_posts(self, author_id: int) -> List[Post]:\\n logger.info(f"Fetching posts for user with id: {author_id}")\\n return self.post_repo.get_by_author(author_id)\\n\\n def get_recent_posts(self, limit: int = 10) -> List[Post]:\\n logger.info(f"Fetching {limit} recent posts")\\n return self.post_repo.get_recent(limit)",
"/src/core/logging.py": "import sys\\nfrom loguru import logger\\n\\ndef setup_logging():\\n logger.remove()\\n logger.add(\\n sys.stdout,\\n colorize=True,\\n format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",\\n level="INFO"\\n )\\n logger.add(\\n "logs/app.log",\\n rotation="500 MB",\\n retention="10 days",\\n compression="zip",\\n level="DEBUG"\\n )\\n\\n return logger",
"/tests/conftest.py": "import pytest\\nfrom fastapi.testclient import TestClient\\nfrom sqlalchemy import create_engine\\nfrom sqlalchemy.orm import sessionmaker\\n\\nfrom src.main import app\\nfrom src.database import Base, get_db\\nfrom src.models import User, UserRole\\nfrom src.auth.utils import get_password_hash\\n\\nSQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"\\n\\nengine = create_engine(\\n SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}\\n)\\nTestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)\\n\\n@pytest.fixture(scope="function")\\ndef db():\\n Base.metadata.create_all(bind=engine)\\n db = TestingSessionLocal()\\n try:\\n yield db\\n finally:\\n db.close()\\n Base.metadata.drop_all(bind=engine)\\n\\n@pytest.fixture(scope="function")\\ndef client(db):\\n def override_get_db():\\n try:\\n yield db\\n finally:\\n db.close()\\n \\n app.dependency_overrides[get_db] = override_get_db\\n yield TestClient(app)\\n del app.dependency_overrides[get_db]\\n\\n@pytest.fixture(scope="function")\\ndef test_user(db):\\n user = User(\\n username="testuser",\\n email="testuser@example.com",\\n hashed_password=get_password_hash("testpassword"),\\n role=UserRole.USER\\n )\\n db.add(user)\\n db.commit()\\n db.refresh(user)\\n return user",
"/tests/test_auth.py": "from fastapi.testclient import TestClient\\nfrom src.main import app\\n\\nclient = TestClient(app)\\n\\ndef test_login(test_user):\\n response = client.post(\\n "/token",\\n data={"username": "testuser", "password": "testpassword"}\\n )\\n assert response.status_code == 200\\n assert "access_token" in response.json()\\n assert response.json()["token_type"] == "bearer"\\n\\ndef test_login_incorrect_password(test_user):\\n response = client.post(\\n "/token",\\n data={"username": "testuser", "password": "wrongpassword"}\\n )\\n assert response.status_code == 401\\n assert response.json()["detail"] == "Incorrect username or password"\\n\\ndef test_read_users_me(test_user, client):\\n response = client.post(\\n "/token",\\n data={"username": "testuser", "password": "testpassword"}\\n )\\n access_token = response.json()["access_token"]\\n \\n response = client.get(\\n "/users/me",\\n headers={"Authorization": f"Bearer {access_token}"}\\n )\\n assert response.status_code == 200\\n assert response.json()["username"] == "testuser"\\n assert response.json()["email"] == "testuser@example.com"",
"/tests/test_posts.py": "import pytest\\nfrom fastapi.testclient import TestClient\\nfrom src.main import app\\n\\nclient = TestClient(app)\\n\\n@pytest.fixture(scope="function")\\ndef auth_headers(test_user):\\n response = client.post(\\n "/token",\\n data={"username": "testuser", "password": "testpassword"}\\n )\\n access_token = response.json()["access_token"]\\n return {"Authorization": f"Bearer {access_token}"}\\n\\ndef test_create_post(auth_headers):\\n response = client.post(\\n "/posts",\\n json={"title": "Test Post", "content": "This is a test post"},\\n headers=auth_headers\\n )\\n assert response.status_code == 200\\n assert response.json()["title"] == "Test Post"\\n assert response.json()["content"] == "This is a test post"\\n\\ndef test_read_post(auth_headers):\\n # First, create a post\\n response = client.post(\\n "/posts",\\n json={"title": "Test Post", "content": "This is a test post"},\\n headers=auth_headers\\n )\\n post_id = response.json()["id"]\\n\\n # Now, read the post\\n response = client.get(f"/posts/{post_id}")\\n assert response.status_code == 200\\n assert response.json()["title"] == "Test Post"\\n assert response.json()["content"] == "This is a test post"\\n\\ndef test_update_post(auth_headers):\\n # First, create a post\\n response = client.post(\\n "/posts",\\n json={"title": "Test Post", "content": "This is a test post"},\\n headers=auth_headers\\n )\\n post_id = response.json()["id"]\\n\\n # Now, update the post\\n response = client.put(\\n f"/posts/{post_id}",\\n json={"title": "Updated Test Post", "content": "This is an updated test post"},\\n headers=auth_headers\\n )\\n assert response.status_code == 200\\n assert response.json()["title"] == "Updated Test Post"\\n assert response.json()["content"] == "This is an updated test post"\\n\\ndef test_delete_post(auth_headers):\\n # First, create a post\\n response = client.post(\\n "/posts",\\n json={"title": "Test Post", "content": "This is a test post"},\\n headers=auth_headers\\n )\\n post_id = response.json()["id"]\\n\\n # Now, delete the post\\n response = client.delete(f"/posts/{post_id}", headers=auth_headers)\\n assert response.status_code == 204\\n\\n # Try to read the deleted post\\n response = client.get(f"/posts/{post_id}")\\n assert response.status_code == 404",
"/scripts/run_migrations.py": "from alembic import command\\nfrom alembic.config import Config\\n\\ndef run_migrations():\\n alembic_cfg = Config("alembic.ini")\\n command.upgrade(alembic_cfg, "head")\\n\\nif name == "main":\\n run_migrations()",
"/.github/workflows/ci-cd.yml": "name: CI/CD\\n\\non:\\n push:\\n branches: [ main ]\\n pull_request:\\n branches: [ main ]\\n\\njobs:\\n test:\\n runs-on: ubuntu-latest\\n steps:\\n - uses: actions/checkout@v2\\n - name: Set up Python\\n uses: actions/setup-python@v2\\n with:\\n python-version: '3.10'\\n - name: Install dependencies\\n run: |\\n python -m pip install --upgrade pip\\n pip install -r requirements.txt\\n - name: Run tests\\n run: |\\n pytest\\n\\n lint:\\n runs-on: ubuntu-latest\\n steps:\\n - uses: actions/checkout@v2\\n - name: Set up Python\\n uses: actions/setup-python@v2\\n with:\\n python-version: '3.10'\\n - name: Install dependencies\\n run: |\\n python -m pip install --upgrade pip\\n pip install flake8 black\\n - name: Run linters\\n run: |\\n flake8 .\\n black --check .\\n\\n build-and-push:\\n needs: [test, lint]\\n runs-on: ubuntu-latest\\n steps:\\n - uses: actions/checkout@v2\\n - name: Build Docker image\\n run: docker build -t fastapi-app .\\n - name: Log in to Docker Hub\\n uses: docker/login-action@v1\\n with:\\n username: ${{ secrets.DOCKER_HUB_USERNAME }}\\n password: ${{ secrets.DOCKER_HUB_ACCESS_TOKEN }}\\n - name: Push image to Docker Hub\\n run: |\\n docker tag fastapi-app ${{ secrets.DOCKER_HUB_USERNAME }}/fastapi-app:${{ github.sha }}\\n docker push ${{ secrets.DOCKER_HUB_USERNAME }}/fastapi-app:${{ github.sha }}\\n\\n deploy:\\n needs: build-and-push\\n runs-on: ubuntu-latest\\n steps:\\n - name: Deploy to production\\n run: |\\n echo "Deploying to production server"\\n # Add deployment steps here, e.g., SSH into server and pull/run new Docker image"
}
}
'''

import json

data = json.loads(data)

def create_folders():
    for folder in data["file_structure"]:
        path = folder["path"]
        files = folder["files"]
        print(f"Creating folder: {path}")
        for file in files:
            print(f"Creating file: {path}/{file}")

def create_files():
    for file, content in data["file_contents"].items():
        print(f"Creating file: {file}")
        print(f"Writing content to {file}:")
        print(content)

def setup():
    create_folders()
    create_files()

setup()