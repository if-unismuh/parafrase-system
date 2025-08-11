"""
Main API router
"""
from fastapi import APIRouter

from app.api.endpoints import health, paraphrase, full_gemini, systems, ultimate_hybrid, integrated_smart, batch_word

# Create main API router
api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["Health Check"]
)

api_router.include_router(
    systems.router,
    prefix="/paraphrase/systems",
    tags=["Paraphrasing Systems Overview"]
)

api_router.include_router(
    paraphrase.router,
    prefix="/paraphrase/smart-efficient",
    tags=["Smart Efficient Paraphrasing"]
)

api_router.include_router(
    full_gemini.router,
    prefix="/paraphrase/full-gemini",
    tags=["Full Gemini AI Paraphrasing"]
)

api_router.include_router(
    ultimate_hybrid.router,
    prefix="/paraphrase/ultimate-hybrid",
    tags=["Ultimate Hybrid Paraphrasing"]
)

api_router.include_router(
    integrated_smart.router,
    prefix="/paraphrase/integrated-smart",
    tags=["Integrated Smart Paraphrasing"]
)

api_router.include_router(
    batch_word.router,
    prefix="/paraphrase/batch-word",
    tags=["Batch Word Document Processing"]
)

# Additional routers will be added here as we implement them
# api_router.include_router(search.router, prefix="/search", tags=["Search"])
# api_router.include_router(quality.router, prefix="/quality", tags=["Quality"])
# api_router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
# api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
# api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])