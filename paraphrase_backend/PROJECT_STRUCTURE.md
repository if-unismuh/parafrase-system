# 📁 Project Structure - Paraphrase Backend

```
paraphrase_backend/
├── app/                          # Main application code
│   ├── __init__.py
│   ├── main.py                   # FastAPI app entry point
│   ├── api/                      # API layer
│   │   ├── __init__.py
│   │   ├── router.py            # Main API router
│   │   ├── dependencies.py      # API dependencies
│   │   ├── endpoints/           # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── paraphrase.py    # Paraphrasing endpoints
│   │   │   ├── search.py        # Search & context endpoints
│   │   │   ├── quality.py       # Quality assessment endpoints
│   │   │   ├── analysis.py      # Text analysis endpoints
│   │   │   ├── jobs.py          # Job management endpoints
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   ├── admin.py         # Admin endpoints
│   │   │   └── health.py        # Health check endpoints
│   │   └── models/              # Pydantic models
│   │       ├── __init__.py
│   │       ├── paraphrase.py    # Paraphrasing models
│   │       ├── search.py        # Search models
│   │       ├── analysis.py      # Analysis models
│   │       ├── jobs.py          # Job models
│   │       ├── auth.py          # Auth models
│   │       └── common.py        # Common response models
│   ├── core/                     # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py            # Configuration management
│   │   ├── security.py          # Security utilities
│   │   ├── database.py          # Database configuration
│   │   ├── cache.py             # Redis cache configuration
│   │   ├── logging.py           # Logging configuration
│   │   └── exceptions.py        # Custom exceptions
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   ├── paraphrase_service.py    # Main paraphrasing logic
│   │   ├── search_service.py        # Search functionality
│   │   ├── quality_service.py       # Quality assessment
│   │   ├── analysis_service.py      # Text analysis
│   │   ├── job_service.py          # Job management
│   │   ├── auth_service.py         # Authentication logic
│   │   └── file_service.py         # File handling
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       ├── text_processing.py   # Text processing utilities
│       ├── file_utils.py        # File handling utilities
│       ├── validators.py        # Input validators
│       ├── formatters.py        # Response formatters
│       └── helpers.py           # General helper functions
├── tests/                        # Test files
│   ├── __init__.py
│   ├── conftest.py              # Test configuration
│   ├── test_api/                # API tests
│   │   ├── __init__.py
│   │   ├── test_paraphrase.py
│   │   ├── test_search.py
│   │   └── test_auth.py
│   ├── test_services/           # Service tests
│   │   ├── __init__.py
│   │   ├── test_paraphrase_service.py
│   │   └── test_search_service.py
│   └── test_utils/              # Utility tests
│       ├── __init__.py
│       └── test_text_processing.py
├── config/                       # Configuration files
│   ├── __init__.py
│   ├── settings.yaml            # Application settings
│   ├── logging.yaml             # Logging configuration
│   └── docker/                  # Docker configurations
│       ├── Dockerfile
│       ├── docker-compose.yml
│       └── docker-compose.prod.yml
├── docs/                         # Documentation
│   ├── api/                     # API documentation
│   │   ├── openapi.json
│   │   └── README.md
│   ├── deployment/              # Deployment guides
│   │   ├── local.md
│   │   ├── docker.md
│   │   └── production.md
│   └── development/             # Development guides
│       ├── setup.md
│       ├── testing.md
│       └── contributing.md
├── scripts/                      # Utility scripts
│   ├── start.sh                 # Start application
│   ├── test.sh                  # Run tests
│   ├── build.sh                 # Build application
│   └── deploy.sh                # Deployment script
├── alembic/                      # Database migrations
│   ├── alembic.ini
│   ├── env.py
│   └── versions/
├── static/                       # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── templates/                    # Jinja2 templates
│   ├── base.html
│   └── docs.html
├── requirements/                 # Dependencies
│   ├── base.txt                 # Base requirements
│   ├── dev.txt                  # Development requirements
│   └── prod.txt                 # Production requirements
├── .env.example                  # Environment variables example
├── .gitignore                   # Git ignore file
├── pyproject.toml               # Python project configuration
├── README.md                    # Project README
└── LICENSE                      # License file
```

## 🎯 Architecture Principles

### 1. **Separation of Concerns**
- **API Layer**: Handle HTTP requests/responses
- **Service Layer**: Business logic
- **Utils Layer**: Reusable utilities

### 2. **Dependency Injection**
- Services injected through FastAPI dependencies
- Easy testing and mocking

### 3. **Configuration Management**
- Environment-based configuration
- YAML configuration files
- Environment variable override

### 4. **Error Handling**
- Centralized exception handling
- Structured error responses
- Proper HTTP status codes

### 5. **Testing**
- Unit tests for each layer
- Integration tests
- API endpoint tests

## 🔧 Key Components

### Core Configuration (`core/config.py`)
```python
class Settings(BaseSettings):
    app_name: str = "Paraphrase API"
    api_version: str = "v1"
    debug: bool = False
    database_url: str
    redis_url: str
    secret_key: str
    gemini_api_key: Optional[str] = None
```

### Service Layer Pattern
```python
class ParaphraseService:
    def __init__(self, config: Settings):
        self.paraphraser = SmartEfficientParaphraser()
    
    async def paraphrase_text(self, request: ParaphraseRequest) -> ParaphraseResponse:
        # Business logic here
        pass
```

### API Model Pattern
```python
class ParaphraseRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)
    use_search: bool = True
    quality_level: QualityLevel = QualityLevel.MEDIUM
```

## 📊 Benefits of This Structure

### 1. **Maintainability**
- Clear separation of responsibilities
- Easy to locate and modify code
- Consistent naming conventions

### 2. **Scalability**
- Easy to add new endpoints
- Service layer can be scaled independently
- Database and cache abstraction

### 3. **Testability**
- Each layer can be tested independently
- Mock dependencies easily
- Clear test structure

### 4. **Development Experience**
- Easy onboarding for new developers
- Clear project navigation
- Consistent patterns

### 5. **Deployment**
- Container-ready structure
- Environment-specific configurations
- Easy CI/CD integration

## 🚀 Next Steps

1. **Setup base FastAPI application**
2. **Implement core configuration**
3. **Create service layer**
4. **Implement API endpoints**
5. **Add error handling**
6. **Setup testing framework**
7. **Add documentation**
8. **Containerize application**