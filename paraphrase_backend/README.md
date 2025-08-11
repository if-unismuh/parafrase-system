# 🚀 Paraphrase Backend API

High-performance text paraphrasing API with DuckDuckGo Search (DDGS) enhancement, built with FastAPI.

## ✨ Features

- **🔍 DDGS Integration**: Search-then-paraphrase workflow for better context
- **⚡ Smart Efficiency**: Local-first with AI backup for cost optimization  
- **🎯 Multiple Quality Levels**: Low, medium, high quality processing
- **📊 Batch Processing**: Handle multiple texts efficiently
- **🛡️ Content Protection**: Preserve titles, headings, citations
- **📈 Quality Assessment**: Automatic quality scoring and improvement
- **🔒 Production Ready**: Authentication, rate limiting, monitoring
- **📚 Auto Documentation**: Interactive API docs with OpenAPI/Swagger

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │  Service Layer   │    │  Core Engine    │
│                 │    │                  │    │                 │
│ • API Endpoints │────▶ • Business Logic │────▶ • Smart         │
│ • Validation    │    │ • Error Handling │    │   Paraphraser   │
│ • Docs          │    │ • Data Transform │    │ • DDGS Search   │
└─────────────────┘    └──────────────────┘    │ • AI Refinement │
                                               └─────────────────┘
```

## 🎯 API Endpoints

### Core Paraphrasing
- `POST /api/v1/paraphrase/text` - Paraphrase single text
- `POST /api/v1/paraphrase/batch` - Paraphrase multiple texts
- `POST /api/v1/paraphrase/document` - Upload and paraphrase documents
- `GET /api/v1/paraphrase/methods` - Available processing methods

### Health & Monitoring  
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed system status
- `GET /api/v1/health/ready` - Kubernetes readiness probe
- `GET /api/v1/health/live` - Kubernetes liveness probe

### Coming Soon
- `GET /api/v1/search/context` - Preview search context
- `POST /api/v1/quality/assess` - Quality assessment
- `POST /api/v1/analysis/similarity` - Similarity analysis
- `POST /api/v1/jobs/*` - Async job management
- `POST /api/v1/auth/*` - Authentication endpoints

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
cd paraphrase_backend

# Install dependencies
pip install -r requirements/dev.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your configuration
```

### 2. Configuration

Key environment variables:

```bash
# AI Service (Optional - for quality refinement)
GEMINI_API_KEY=your_gemini_api_key

# Database (SQLite works for development)
DATABASE_URL=sqlite:///./paraphrase.db

# DuckDuckGo Search (Enabled by default)
DDGS_ENABLED=true
DDGS_REGION=id-id
DDGS_LANGUAGE=id
```

### 3. Run the Application

```bash
# Using the start script (recommended)
./scripts/start.sh

# Or directly with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access the API

- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

## 📖 Usage Examples

### Single Text Paraphrasing

```bash
curl -X POST "http://localhost:8000/api/v1/paraphrase/text" \\
  -H "Content-Type: application/json" \\
  -d '{
    "text": "Penelitian ini bertujuan untuk menganalisis dampak teknologi AI terhadap pendidikan modern.",
    "use_search": true,
    "quality_level": "medium"
  }'
```

### Batch Processing

```bash
curl -X POST "http://localhost:8000/api/v1/paraphrase/batch" \\
  -H "Content-Type: application/json" \\
  -d '{
    "texts": [
      "Text pertama yang akan diparafrase.",
      "Text kedua untuk diproses bersama."
    ],
    "use_search": true,
    "quality_level": "high"
  }'
```

### Python Client Example

```python
import requests

# Single text paraphrasing
response = requests.post(
    "http://localhost:8000/api/v1/paraphrase/text",
    json={
        "text": "Your text here",
        "use_search": True,
        "quality_level": "medium"
    }
)

result = response.json()
print(f"Original: {result['data']['original_text']}")
print(f"Paraphrased: {result['data']['paraphrased_text']}")
print(f"Method: {result['data']['metadata']['method']}")
print(f"Similarity: {result['data']['metadata']['similarity']}%")
```

## 📊 Response Format

### Success Response
```json
{
  "success": true,
  "message": "Text paraphrased successfully",
  "data": {
    "paraphrased_text": "Riset ini dimaksudkan akan mengkaji dampak teknologi AI tentang edukasi kontemporer.",
    "original_text": "Penelitian ini bertujuan untuk menganalisis dampak teknologi AI terhadap pendidikan modern.",
    "metadata": {
      "method": "local_with_search_context",
      "similarity": 45.67,
      "plagiarism_reduction": 54.33,
      "quality_score": 85,
      "changes_made": 6,
      "processing_time_ms": 1250,
      "search_context": "AI in Education Research",
      "api_calls_used": 0,
      "cost_estimate": null
    }
  },
  "timestamp": "2025-01-01T12:00:00Z",
  "request_id": "abc-123-def"
}
```

### Error Response
```json
{
  "success": false,
  "message": "Request failed",
  "error": {
    "code": "TEXT_TOO_LONG",
    "message": "Text length (15000) exceeds maximum allowed (10000)",
    "details": {
      "length": 15000,
      "max_length": 10000
    }
  },
  "timestamp": "2025-01-01T12:00:00Z",
  "request_id": "abc-123-def"
}
```

## 🎯 Processing Methods

The API automatically selects the best method based on quality assessment:

1. **local_only**: Fast synonym-based paraphrasing
2. **local_with_search_context**: Enhanced with internet search
3. **local_plus_ai_refinement**: AI quality improvement
4. **local_plus_ai_refinement_with_search**: Full pipeline

## 🔧 Configuration

### Text Processing Limits
```bash
MAX_TEXT_LENGTH=10000        # Maximum characters per text
MIN_TEXT_LENGTH=10           # Minimum characters per text
MAX_BATCH_SIZE=100           # Maximum texts per batch request
```

### DuckDuckGo Search
```bash
DDGS_ENABLED=true            # Enable/disable search
DDGS_REGION=id-id           # Search region
DDGS_LANGUAGE=id            # Search language
DDGS_MAX_RESULTS=5          # Maximum search results
```

### Rate Limiting
```bash
RATE_LIMIT_PER_MINUTE=60    # Requests per minute
RATE_LIMIT_PER_HOUR=1000    # Requests per hour
RATE_LIMIT_PER_DAY=10000    # Requests per day
```

## 🔒 Security Features

- **Input Validation**: Comprehensive request validation
- **Rate Limiting**: Prevent abuse and DoS attacks
- **Error Handling**: Secure error messages
- **CORS Configuration**: Configurable cross-origin policies
- **Content Protection**: Automatic detection of sensitive content

## 📈 Monitoring & Health

### Health Endpoints
- `/api/v1/health` - Basic health status
- `/api/v1/health/detailed` - Comprehensive system info
- `/api/v1/health/ready` - Kubernetes readiness
- `/api/v1/health/live` - Kubernetes liveness

### Metrics (Coming Soon)
- Processing time distributions
- Success/failure rates
- API usage statistics
- Cost tracking

## 🧪 Testing

```bash
# Install dev dependencies
pip install -r requirements/dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific tests
pytest tests/test_api/test_paraphrase.py -v
```

## 🐳 Docker Deployment

```bash
# Build image
docker build -t paraphrase-api .

# Run container
docker run -p 8000:8000 \\
  -e DATABASE_URL=sqlite:///./app.db \\
  -e GEMINI_API_KEY=your_key \\
  paraphrase-api
```

## 📚 Development

### Project Structure
```
paraphrase_backend/
├── app/                    # Application code
│   ├── api/               # API layer
│   │   ├── endpoints/     # Route handlers
│   │   └── models/        # Pydantic models
│   ├── core/              # Core functionality
│   ├── services/          # Business logic
│   └── utils/             # Utilities
├── tests/                 # Test files
├── config/                # Configuration files
└── scripts/               # Utility scripts
```

### Adding New Endpoints
1. Create endpoint in `app/api/endpoints/`
2. Add Pydantic models in `app/api/models/`
3. Implement business logic in `app/services/`
4. Add tests in `tests/`
5. Update router in `app/api/router.py`

### Code Quality
```bash
# Format code
black app/
isort app/

# Lint
flake8 app/
mypy app/

# Pre-commit hooks
pre-commit install
pre-commit run --all-files
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- DuckDuckGo for privacy-focused search API
- Google Generative AI for text refinement capabilities
- The open-source community for inspiration and tools

---

**Version**: 1.0.0  
**Author**: DevNoLife  
**Last Updated**: 2025-01-01

For more information, visit the [API Documentation](http://localhost:8000/docs) when the server is running.