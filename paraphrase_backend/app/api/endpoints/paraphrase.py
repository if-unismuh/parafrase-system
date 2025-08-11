"""
Paraphrase endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from app.core.config import get_settings, Settings
from app.services.paraphrase_service import ParaphraseService
from app.api.models.paraphrase import (
    ParaphraseRequest,
    ParaphraseResponse,
    BatchParaphraseRequest,
    BatchParaphraseResponse
)
from app.api.models.common import SuccessResponse
from app.core.exceptions import ParaphraseAPIException

router = APIRouter()

# Dependency to get paraphrase service
def get_paraphrase_service(settings: Settings = Depends(get_settings)) -> ParaphraseService:
    """Dependency to get paraphrase service instance"""
    return ParaphraseService(settings)

@router.post("/text", response_model=ParaphraseResponse)
async def paraphrase_text(
    request: ParaphraseRequest,
    service: ParaphraseService = Depends(get_paraphrase_service)
):
    """
    Paraphrase a single text
    
    This endpoint takes a text input and returns a paraphrased version using the
    Smart Efficient Paraphraser system. The system uses local paraphrasing with
    optional DuckDuckGo search context and AI refinement when needed.
    
    - **text**: The text to be paraphrased (10-10000 characters)
    - **use_search**: Enable DuckDuckGo search for context enhancement
    - **quality_level**: Quality level (low/medium/high)
    - **language**: Language code (default: 'id' for Indonesian)
    - **preserve_formatting**: Preserve original text formatting
    
    Returns the paraphrased text with detailed metadata including:
    - Processing method used
    - Similarity percentage
    - Quality scores
    - Performance metrics
    """
    try:
        result = await service.paraphrase_text(request)
        return ParaphraseResponse(
            success=True,
            message="Text paraphrased successfully",
            data=result
        )
    except ParaphraseAPIException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Paraphrasing failed: {str(e)}"
        )

@router.post("/batch", response_model=BatchParaphraseResponse)
async def paraphrase_batch(
    request: BatchParaphraseRequest,
    service: ParaphraseService = Depends(get_paraphrase_service)
):
    """
    Paraphrase multiple texts in a single request
    
    This endpoint allows you to paraphrase multiple texts efficiently in one
    API call. Each text is processed individually, and the results include
    both successful paraphrases and any errors that occurred.
    
    - **texts**: List of texts to paraphrase (1-100 texts)
    - **use_search**: Enable DuckDuckGo search for all texts
    - **quality_level**: Quality level for all texts
    - **language**: Language code for all texts
    - **preserve_formatting**: Preserve formatting for all texts
    
    Returns:
    - Individual results for each text
    - Batch processing summary with statistics
    - Error details for any failed texts
    """
    try:
        result = await service.paraphrase_batch(request)
        return BatchParaphraseResponse(
            success=True,
            message=f"Batch processed: {result.summary.successful} successful, {result.summary.failed} failed",
            data=result
        )
    except ParaphraseAPIException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch paraphrasing failed: {str(e)}"
        )

@router.get("/stats", response_model=SuccessResponse)
async def get_paraphrase_stats(
    service: ParaphraseService = Depends(get_paraphrase_service)
):
    """
    Get paraphrasing service statistics and configuration
    
    Returns information about:
    - Service availability and configuration
    - Synonym database status
    - AI service availability
    - Processing limits and settings
    """
    try:
        stats = await service.get_service_stats()
        return SuccessResponse(
            success=True,
            message="Service statistics retrieved",
            data=stats
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve stats: {str(e)}"
        )

# Placeholder for future endpoints

@router.post("/document")
async def paraphrase_document():
    """
    Paraphrase a document (TODO: Implement)
    
    This endpoint will handle document upload and paraphrasing.
    Supported formats: .docx, .txt, .pdf
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Document paraphrasing not yet implemented"
    )

@router.get("/methods", response_model=SuccessResponse)
async def get_paraphrase_methods():
    """
    Get available paraphrasing methods and their descriptions
    
    Returns information about different processing methods:
    - local_only: Local paraphrasing without search
    - local_with_search_context: Local paraphrasing with DuckDuckGo context
    - local_plus_ai_refinement: Local paraphrasing with AI refinement
    - local_plus_ai_refinement_with_search: Full pipeline with search and AI
    """
    methods = {
        "local_only": {
            "name": "Local Only",
            "description": "Fast local paraphrasing using synonym database",
            "features": ["Synonym replacement", "Phrase restructuring", "Fast processing"],
            "cost": "Free",
            "speed": "Very Fast"
        },
        "local_with_search_context": {
            "name": "Local with Search Context",
            "description": "Local paraphrasing enhanced with internet search context",
            "features": ["All local features", "Context-aware synonyms", "Search enhancement"],
            "cost": "Free (web search)",
            "speed": "Fast"
        },
        "local_plus_ai_refinement": {
            "name": "Local + AI Refinement",
            "description": "Local paraphrasing with AI quality improvement",
            "features": ["All local features", "AI quality assessment", "Smart refinement"],
            "cost": "Low (AI API usage)",
            "speed": "Medium"
        },
        "local_plus_ai_refinement_with_search": {
            "name": "Full Pipeline",
            "description": "Complete pipeline with search context and AI refinement",
            "features": ["All features combined", "Maximum quality", "Comprehensive processing"],
            "cost": "Low (AI API usage)",
            "speed": "Medium"
        }
    }
    
    return SuccessResponse(
        success=True,
        message="Available paraphrasing methods",
        data={
            "methods": methods,
            "default_method": "Automatically selected based on quality assessment",
            "recommendation": "Use default settings for optimal balance of speed, quality, and cost"
        }
    )