"""
Full Gemini Paraphrasing endpoints
Premium AI paraphrasing with full Gemini processing
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from app.core.config import get_settings, Settings
from app.services.full_gemini_service import FullGeminiService
from app.api.models.full_gemini import (
    FullGeminiRequest,
    FullGeminiResponse,
    BatchFullGeminiRequest,
    BatchFullGeminiResponse
)
from app.api.models.common import SuccessResponse
from app.core.exceptions import ParaphraseAPIException

router = APIRouter()

# Dependency to get Full Gemini service
def get_full_gemini_service(settings: Settings = Depends(get_settings)) -> FullGeminiService:
    """Dependency to get Full Gemini service instance"""
    return FullGeminiService(settings)

@router.post("/text", response_model=FullGeminiResponse)
async def full_gemini_paraphrase_text(
    request: FullGeminiRequest,
    service: FullGeminiService = Depends(get_full_gemini_service)
):
    """
    Paraphrase text using Full Gemini AI - Premium Quality
    
    This endpoint uses the complete Gemini AI processing pipeline for maximum
    quality paraphrasing. It provides superior results with advanced content
    protection and academic optimization features.
    
    **Features:**
    - 🤖 Full AI Processing: Complete Gemini AI pipeline
    - 🛡️ Content Protection: Advanced protection for titles, names, citations  
    - 🎓 Academic Mode: Optimized for academic documents
    - 🎯 Quality Focus: Prioritizes quality over speed
    - 📊 Premium Results: Highest quality paraphrasing available
    
    **Parameters:**
    - **text**: The text to be paraphrased (10-10000 characters)
    - **protection_level**: Content protection level (low/medium/high/maximum)
    - **academic_mode**: Enable academic document optimization
    - **temperature**: AI creativity level (0.0 = conservative, 1.0 = creative)
    - **preserve_formatting**: Preserve original text formatting
    - **quality_focus**: Prioritize quality over processing speed
    
    **Response includes:**
    - High-quality paraphrased text
    - Detailed processing metadata
    - Protected elements information
    - Cost and token usage estimates
    - Quality improvement details
    """
    try:
        result = await service.paraphrase_text(request)
        return FullGeminiResponse(
            success=True,
            message="Text paraphrased successfully with Full Gemini AI",
            data=result
        )
    except ParaphraseAPIException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Full Gemini paraphrasing failed: {str(e)}"
        )

@router.post("/batch", response_model=BatchFullGeminiResponse)
async def full_gemini_paraphrase_batch(
    request: BatchFullGeminiRequest,
    service: FullGeminiService = Depends(get_full_gemini_service)
):
    """
    Batch paraphrase multiple texts using Full Gemini AI
    
    Process multiple texts with the premium Full Gemini AI system. Each text
    receives the same high-quality processing with advanced AI capabilities.
    
    **Features:**
    - 🔄 Batch Processing: Handle up to 50 texts per request
    - 🤖 Consistent Quality: Full AI processing for each text
    - 📊 Detailed Analytics: Comprehensive batch statistics
    - 💰 Cost Tracking: Detailed cost and token usage reporting
    - 🛡️ Uniform Protection: Same protection level for all texts
    
    **Parameters:**
    - **texts**: List of texts to paraphrase (1-50 texts max)
    - **protection_level**: Content protection level for all texts
    - **academic_mode**: Enable academic optimization for all texts
    - **temperature**: AI creativity level for all processing
    - **preserve_formatting**: Preserve formatting for all texts
    - **quality_focus**: Quality priority setting
    
    **Response includes:**
    - Individual results for each text
    - Comprehensive batch summary
    - Cost analysis and optimization suggestions
    - Quality metrics and improvements
    """
    try:
        result = await service.paraphrase_batch(request)
        return BatchFullGeminiResponse(
            success=True,
            message=f"Batch processed with Full Gemini AI: {result.summary.successful} successful, {result.summary.failed} failed",
            data=result
        )
    except ParaphraseAPIException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Full Gemini batch paraphrasing failed: {str(e)}"
        )

@router.get("/stats", response_model=SuccessResponse)
async def get_full_gemini_stats(
    service: FullGeminiService = Depends(get_full_gemini_service)
):
    """
    Get Full Gemini service statistics and configuration
    
    Returns comprehensive information about the Full Gemini AI paraphrasing
    service including capabilities, pricing, and configuration details.
    
    **Information provided:**
    - Service availability and status
    - AI model configuration
    - Feature capabilities
    - Processing limits and settings
    - Cost information and estimates
    - Quality benchmarks
    """
    try:
        stats = await service.get_service_stats()
        return SuccessResponse(
            success=True,
            message="Full Gemini service statistics retrieved",
            data=stats
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve Full Gemini stats: {str(e)}"
        )

@router.get("/features", response_model=SuccessResponse)
async def get_full_gemini_features():
    """
    Get detailed information about Full Gemini features and capabilities
    
    Returns comprehensive documentation about what makes Full Gemini different
    from other paraphrasing methods and when to use it.
    """
    features = {
        "core_features": {
            "full_ai_processing": {
                "name": "Complete AI Processing",
                "description": "Uses full Gemini AI pipeline for every sentence",
                "benefits": ["Maximum quality", "Contextual understanding", "Advanced grammar"],
                "use_cases": ["Academic papers", "Professional documents", "High-stakes content"]
            },
            "content_protection": {
                "name": "Advanced Content Protection",
                "description": "Intelligent protection of important content elements",
                "protection_types": ["Titles and headings", "Author names", "Citations", "Technical terms"],
                "levels": ["Low", "Medium", "High", "Maximum"]
            },
            "academic_optimization": {
                "name": "Academic Document Optimization", 
                "description": "Specialized processing for academic content",
                "features": ["Formal language", "Academic vocabulary", "Citation preservation", "Structure maintenance"]
            },
            "quality_focus": {
                "name": "Quality-First Processing",
                "description": "Prioritizes output quality over processing speed",
                "guarantees": ["95%+ quality score", "Natural language flow", "Context preservation"]
            }
        },
        "comparison": {
            "vs_smart_efficient": {
                "quality": "Higher (AI vs Local+AI)",
                "speed": "Slower (3-5s vs 1-2s)", 
                "cost": "Higher (AI tokens vs Free)",
                "use_case": "Premium quality vs Daily usage"
            },
            "vs_other_systems": {
                "ultimate_hybrid": "More AI-focused vs Multi-modal",
                "integrated_smart": "Quality vs Workflow automation", 
                "batch_word": "Individual processing vs Bulk modification"
            }
        },
        "pricing": {
            "model": "Per-token usage",
            "typical_costs": {
                "short_paragraph": "$0.002 - $0.005",
                "academic_page": "$0.01 - $0.03",
                "full_document": "$0.05 - $0.20"
            },
            "cost_factors": ["Text length", "Complexity", "Protection level", "Academic features"]
        },
        "recommendations": {
            "best_for": [
                "Academic research papers",
                "Professional business documents", 
                "High-quality content creation",
                "Premium publishing requirements"
            ],
            "not_recommended_for": [
                "High-volume batch processing",
                "Cost-sensitive applications",
                "Real-time processing needs",
                "Simple text modifications"
            ]
        }
    }
    
    return SuccessResponse(
        success=True,
        message="Full Gemini features and capabilities",
        data=features
    )

@router.get("/models", response_model=SuccessResponse)
async def get_gemini_models():
    """
    Get information about available Gemini models and their characteristics
    
    Returns details about different Gemini model variants and their
    specific use cases and performance characteristics.
    """
    models = {
        "available_models": {
            "gemini-1.5-flash": {
                "description": "Fast, efficient model for most use cases",
                "speed": "Fast",
                "quality": "High",
                "cost": "Low",
                "best_for": ["General paraphrasing", "Batch processing", "Cost-effective quality"],
                "token_limits": "1M tokens context"
            },
            "gemini-1.5-pro": {
                "description": "Premium model for highest quality results",
                "speed": "Medium", 
                "quality": "Highest",
                "cost": "Higher",
                "best_for": ["Academic papers", "Complex documents", "Maximum quality"],
                "token_limits": "2M tokens context"
            }
        },
        "model_selection": {
            "automatic": "System automatically selects best model based on content",
            "factors": ["Text complexity", "Quality requirements", "Cost preferences"],
            "override": "Users can specify model preferences in advanced settings"
        },
        "performance_benchmarks": {
            "quality_scores": {
                "gemini-1.5-flash": "92-95%",
                "gemini-1.5-pro": "95-98%"
            },
            "processing_times": {
                "gemini-1.5-flash": "1-3 seconds",
                "gemini-1.5-pro": "3-6 seconds"
            }
        }
    }
    
    return SuccessResponse(
        success=True,
        message="Available Gemini models and specifications",
        data=models
    )

# Placeholder for document processing
@router.post("/document")
async def full_gemini_paraphrase_document():
    """
    Full Gemini document paraphrasing (TODO: Implement)
    
    This endpoint will handle document upload and paraphrasing using
    the complete Full Gemini AI pipeline with advanced document analysis.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Full Gemini document paraphrasing not yet implemented"
    )