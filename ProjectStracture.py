import os
from pathlib import Path

# Folder and file structure definition
PROJECT_STRUCTURE = {
    "alembic": {},  # migrations
    "app": {
        "api/v1/endpoints": {
            "auth.py": "# Authentication endpoints\nfrom fastapi import APIRouter\nrouter = APIRouter()\n\n@router.post('/login')\ndef login():\n    return {'msg': 'Login successful'}\n",
            "users.py": "# User endpoints\nfrom fastapi import APIRouter\nrouter = APIRouter()\n\n@router.get('/')\ndef list_users():\n    return [{'id': 1, 'name': 'John Doe'}]\n",
            "students.py": "# Student endpoints\nfrom fastapi import APIRouter\nrouter = APIRouter()\n\n@router.get('/')\ndef list_students():\n    return [{'id': 1, 'name': 'Jane Student'}]\n",
            "payments.py": "# Payment endpoints\nfrom fastapi import APIRouter\nrouter = APIRouter()\n\n@router.post('/')\ndef create_payment():\n    return {'msg': 'Payment created'}\n",
            "__init__.py": ""
        },
        "core": {
            "config.py": "# App settings\nfrom pydantic_settings import BaseSettings\n\nclass Settings(BaseSettings):\n    APP_NAME: str = 'FastAPI Project'\n    DATABASE_URL: str = 'sqlite:///./test.db'\n    SECRET_KEY: str = 'supersecret'\n\n    class Config:\n        env_file = '.env'\n\nsettings = Settings()\n",
            "security.py": "# JWT & password hashing\nfrom passlib.context import CryptContext\n\npwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')\n\ndef hash_password(password: str):\n    return pwd_context.hash(password)\n\ndef verify_password(password: str, hashed: str):\n    return pwd_context.verify(password, hashed)\n",
            "otp.py": "# One-time password generation\nimport random\n\ndef generate_otp():\n    return random.randint(100000, 999999)\n",
            "logging.py": "# Logging setup\nimport logging\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(__name__)\n",
            "rate_limit.py": "# Rate limiting placeholder\n# You can integrate slowapi or custom middleware\nMAX_REQUESTS_PER_MINUTE = 60\n",
            "__init__.py": ""
        },
        "middlewares": {
            "auth_middleware.py": "# Auth middleware\nfrom starlette.middleware.base import BaseHTTPMiddleware\n\nclass AuthMiddleware(BaseHTTPMiddleware):\n    async def dispatch(self, request, call_next):\n        response = await call_next(request)\n        return response\n",
            "firewall.py": "# Firewall middleware\nALLOWED_IPS = ['127.0.0.1']\n",
            "request_logger.py": "# Request logging middleware\nimport logging\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger('requests')\n",
            "__init__.py": ""
        },
        "models": {
            "user.py": "# SQLAlchemy User model\nfrom sqlalchemy import Column, Integer, String\nfrom app.db.base import Base\n\nclass User(Base):\n    __tablename__ = 'users'\n    id = Column(Integer, primary_key=True)\n    name = Column(String)\n",
            "student.py": "# SQLAlchemy Student model\nfrom sqlalchemy import Column, Integer, String\nfrom app.db.base import Base\n\nclass Student(Base):\n    __tablename__ = 'students'\n    id = Column(Integer, primary_key=True)\n    name = Column(String)\n",
            "payment.py": "# SQLAlchemy Payment model\nfrom sqlalchemy import Column, Integer, Float\nfrom app.db.base import Base\n\nclass Payment(Base):\n    __tablename__ = 'payments'\n    id = Column(Integer, primary_key=True)\n    amount = Column(Float)\n",
            "__init__.py": ""
        },
        "schemas": {
            "user.py": "# Pydantic User schema\nfrom pydantic import BaseModel\n\nclass User(BaseModel):\n    id: int\n    name: str\n    class Config:\n        orm_mode = True\n",
            "student.py": "# Pydantic Student schema\nfrom pydantic import BaseModel\n\nclass Student(BaseModel):\n    id: int\n    name: str\n    class Config:\n        orm_mode = True\n",
            "payment.py": "# Pydantic Payment schema\nfrom pydantic import BaseModel\n\nclass Payment(BaseModel):\n    id: int\n    amount: float\n    class Config:\n        orm_mode = True\n",
            "__init__.py": ""
        },
        "crud": {
            "user.py": "# User CRUD\nfrom sqlalchemy.orm import Session\nfrom app.models.user import User\n\n",
            "student.py": "# Student CRUD\nfrom sqlalchemy.orm import Session\nfrom app.models.student import Student\n\n",
            "payment.py": "# Payment CRUD\nfrom sqlalchemy.orm import Session\nfrom app.models.payment import Payment\n\n",
            "__init__.py": ""
        },
        "services": {
            "email_service.py": "# Email service placeholder\n",
            "sms_service.py": "# SMS service placeholder\n",
            "payment_service.py": "# Payment integration placeholder\n",
            "ai_service.py": "# AI service placeholder\n",
            "__init__.py": ""
        },
        "db": {
            "base.py": "# SQLAlchemy Base\nfrom sqlalchemy.orm import declarative_base\nBase = declarative_base()\n",
            "session.py": "# DB session\nfrom sqlalchemy import create_engine\nfrom sqlalchemy.orm import sessionmaker\nfrom app.core.config import settings\n\nengine = create_engine(settings.DATABASE_URL, echo=True)\nSessionLocal = sessionmaker(bind=engine)\n",
            "__init__.py": ""
        },
        "tasks": {
            "celery_worker.py": "# Celery worker setup\n",
            "tasks.py": "# Background tasks\n",
            "__init__.py": ""
        },
        "utils": {
            "hashing.py": "# Password hashing utils\n",
            "jwt_handler.py": "# JWT helper functions\n",
            "validators.py": "# Custom validators\n",
            "__init__.py": ""
        },
        "tests": {
            "test_auth.py": "# Test auth endpoints\n",
            "test_users.py": "# Test user endpoints\n",
            "test_payments.py": "# Test payments\n",
            "__init__.py": ""
        },
        "main.py": "# FastAPI app entrypoint\nfrom fastapi import FastAPI\nfrom app.api.v1.endpoints import users\n\napp = FastAPI(title='FastAPI Project')\n\napp.include_router(users.router, prefix='/users', tags=['users'])\n\n@app.get('/')\ndef root():\n    return {'msg': 'Hello FastAPI'}\n",
        "__init__.py": ""
    },
    ".env": "DATABASE_URL=sqlite:///./test.db\nSECRET_KEY=supersecret\n",
    "requirements.txt": "fastapi\nuvicorn\nsqlalchemy\nalembic\npython-jose\npasslib\npydantic-settings\n",
    "README.md": "# FastAPI Project Scaffold\nGenerated by fastapi_project_init.py\n",
    "pyproject.toml": "[tool.poetry]\nname = \"fastapi-project\"\nversion = \"0.1.0\"\ndescription = \"FastAPI project scaffold\"\n",
    "alembic.ini": "# Alembic configuration placeholder\n"
}

def create_structure(base_path: Path):
    for name, content in PROJECT_STRUCTURE.items():
        path = base_path / name
        if isinstance(content, dict):  # Folder
            path.mkdir(parents=True, exist_ok=True)
            for subname, subcontent in content.items():
                if isinstance(subcontent, dict):  # Nested folder
                    (path / subname).mkdir(parents=True, exist_ok=True)
                    for file, code in subcontent.items():
                        with open(path / subname / file, "w") as f:
                            f.write(code)
                else:  # File
                    with open(path / subname, "w") as f:
                        f.write(subcontent)
        else:  # File
            with open(path, "w") as f:
                f.write(content)

if __name__ == "__main__":
    project_name = input("Enter your project name: ").strip()
    base_path = Path(project_name)
    base_path.mkdir(parents=True, exist_ok=True)
    create_structure(base_path)
    print(f"✅ FastAPI project '{project_name}' created successfully!")
