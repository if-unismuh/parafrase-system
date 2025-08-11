"""
Ultimate Hybrid Paraphrasing endpoints
Advanced multi-mode paraphrasing with smart routing and Turnitin detection
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from app.core.config import get_settings, Settings
from app.services.ultimate_hybrid_service import UltimateHybridService
from app.api.models.ultimate_hybrid import (
    UltimateHybridRequest,
    UltimateHybridResponse,
    BatchUltimateHybridRequest,
    BatchUltimateHybridResponse,
    MultiOptionRequest,
    MultiOptionResponse,
    ProcessingStatsResponse,
    ProcessingMode
)
from app.api.models.common import SuccessResponse
from app.core.exceptions import ParaphraseAPIException

router = APIRouter()

# Dependency to get Ultimate Hybrid service
def get_ultimate_hybrid_service(settings: Settings = Depends(get_settings)) -> UltimateHybridService:
    """Dependency to get Ultimate Hybrid service instance"""
    return UltimateHybridService(settings)

@router.post("/text", response_model=UltimateHybridResponse)
async def ultimate_hybrid_paraphrase_text(
    request: UltimateHybridRequest,
    service: UltimateHybridService = Depends(get_ultimate_hybrid_service)
):
    """
    Paraphrase text using Ultimate Hybrid System - Multi-Mode Intelligence
    
    This endpoint uses the Ultimate Hybrid Paraphrasing system that combines
    smart routing, multiple processing modes, and Turnitin detection for
    optimal results across different use cases.
    
    **Features:**
    - 🎯 Smart Routing: Automatically chooses local vs AI processing
    - 🔄 Multiple Modes: Smart, Balanced, Aggressive, Turnitin-Safe
    - 🛡️ Turnitin Detection: Identifies and avoids plagiarism patterns
    - 💰 Cost Optimization: Minimizes AI usage while maximizing quality
    - 📊 Advanced Analytics: Detailed processing insights and comparisons
    - 🔄 Adaptive Processing: Adjusts strategy based on text characteristics
    
    **Processing Modes:**
    - **Smart**: Cost-efficient with high quality (30% AI usage target)
    - **Balanced**: Comparison mode with optimal balance (50% AI usage)
    - **Aggressive**: Maximum quality regardless of cost (80% AI usage)
    - **Turnitin-Safe**: Extra protection against detection (60% AI usage)
    
    **Parameters:**
    - **text**: The text to be paraphrased (10-15000 characters)
    - **mode**: Processing mode (smart/balanced/aggressive/turnitin_safe)
    - **aggressiveness**: How aggressive to be with changes (0.1-1.0)
    - **enable_turnitin_detection**: Enable Turnitin risk pattern detection
    - **cost_optimization**: Prefer local processing when possible
    - **cache_enabled**: Enable AI result caching for efficiency
    
    **Response includes:**
    - Intelligently paraphrased text
    - Comprehensive processing metadata
    - Text characteristics analysis
    - Routing decision explanation
    - Cost and performance metrics
    """
    try:
        result = await service.paraphrase_text(request)
        return UltimateHybridResponse(
            success=True,
            message=f"Text paraphrased successfully with Ultimate Hybrid ({request.mode.value} mode)",
            data=result
        )
    except ParaphraseAPIException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ultimate Hybrid paraphrasing failed: {str(e)}"
        )

@router.post("/batch", response_model=BatchUltimateHybridResponse)
async def ultimate_hybrid_paraphrase_batch(
    request: BatchUltimateHybridRequest,
    service: UltimateHybridService = Depends(get_ultimate_hybrid_service)
):
    """
    Batch paraphrase multiple texts using Ultimate Hybrid System
    
    Process up to 100 texts simultaneously with the Ultimate Hybrid system.
    Each text receives intelligent routing and processing optimized for the
    selected mode and text characteristics.
    
    **Features:**
    - 🔄 Batch Processing: Handle up to 100 texts per request
    - 📊 Comprehensive Analytics: Detailed batch statistics and insights
    - 🎯 Consistent Quality: Same intelligent routing for each text
    - 💰 Cost Tracking: Detailed cost analysis and optimization suggestions
    - 📈 Performance Metrics: Processing time, cache hits, AI usage ratios
    - 🛡️ Risk Analysis: Turnitin detection across all texts
    
    **Parameters:**
    - **texts**: List of texts to paraphrase (1-100 texts max)
    - **mode**: Processing mode applied to all texts
    - **aggressiveness**: Aggressiveness level for all texts
    - **enable_turnitin_detection**: Enable risk detection for all texts
    - **cost_optimization**: Cost optimization setting
    - **cache_enabled**: Enable caching for efficiency
    
    **Response includes:**
    - Individual results for each text
    - Comprehensive batch summary with distributions
    - Mode usage statistics
    - Cost analysis and recommendations
    - Performance and cache metrics
    """
    try:
        result = await service.paraphrase_batch(request)
        return BatchUltimateHybridResponse(
            success=True,
            message=f"Batch processed with Ultimate Hybrid ({request.mode.value} mode): {result.summary.successful} successful, {result.summary.failed} failed",
            data=result
        )
    except ParaphraseAPIException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ultimate Hybrid batch paraphrasing failed: {str(e)}"
        )

@router.post("/multi-options", response_model=MultiOptionResponse)
async def generate_multiple_options(
    request: MultiOptionRequest,
    service: UltimateHybridService = Depends(get_ultimate_hybrid_service)
):
    """
    Generate multiple paraphrase options using different approaches
    
    Creates 2-5 different paraphrase versions using various processing modes
    and strategies, allowing you to choose the best result for your needs.
    
    **Features:**
    - 🎯 Multiple Strategies: Different modes for variety
    - 📊 Quality Comparison: Side-by-side analysis of all options
    - 🏆 Smart Recommendation: AI-powered best option selection
    - 📈 Performance Matrix: Detailed comparison metrics
    - 🎨 Style Variety: Different approaches to the same text
    
    **Parameters:**
    - **text**: Text to generate multiple options for
    - **num_options**: Number of different options (2-5)
    - **modes**: Specific modes to use (auto-select if not provided)
    
    **Response includes:**
    - Multiple paraphrase options ranked by quality
    - Comparison matrix between all options
    - Recommended option with detailed reasoning
    - Performance and cost analysis for each option
    """
    try:
        result = await service.generate_multiple_options(request)
        return MultiOptionResponse(
            success=True,
            message=f"Generated {len(result.options)} paraphrase options with quality analysis",
            data=result
        )
    except ParaphraseAPIException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Multiple options generation failed: {str(e)}"
        )

@router.get("/stats", response_model=ProcessingStatsResponse)
async def get_ultimate_hybrid_stats(
    service: UltimateHybridService = Depends(get_ultimate_hybrid_service)
):
    """
    Get Ultimate Hybrid service statistics and performance metrics
    
    Returns comprehensive information about the Ultimate Hybrid system's
    performance including processing statistics, cost tracking, and usage patterns.
    
    **Information provided:**
    - Current processing mode and configuration
    - Processing volume and success rates
    - AI usage patterns and cost tracking
    - Cache performance and hit rates
    - Mode switching and routing decisions
    - Turnitin detection statistics
    """
    try:
        stats = await service.get_processing_stats()
        return ProcessingStatsResponse(
            success=True,
            message="Ultimate Hybrid processing statistics retrieved",
            data=stats
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve Ultimate Hybrid stats: {str(e)}"
        )

@router.get("/modes", response_model=SuccessResponse)
async def get_processing_modes():
    """
    Get detailed information about Ultimate Hybrid processing modes
    
    Returns comprehensive documentation about each processing mode,
    their characteristics, use cases, and when to use them.
    """
    modes = {
        "available_modes": {
            "smart": {
                "name": "Smart Mode",
                "description": "Cost-efficient processing with intelligent routing",
                "ai_usage_target": "30%",
                "cost": "Low",
                "speed": "Fast",
                "quality": "High",
                "characteristics": {
                    "local_confidence_threshold": 0.25,
                    "complexity_threshold": 0.7,
                    "cost_optimization": True,
                    "smart_caching": True
                },
                "best_for": [
                    "Daily document processing",
                    "Cost-sensitive applications", 
                    "High-volume workflows",
                    "General academic content"
                ]
            },
            "balanced": {
                "name": "Balanced Mode",
                "description": "Optimal balance between quality and cost with comparison analysis",
                "ai_usage_target": "50%",
                "cost": "Medium",
                "speed": "Medium",
                "quality": "Very High",
                "characteristics": {
                    "comparison_mode": True,
                    "local_confidence_threshold": 0.15,
                    "complexity_threshold": 0.4,
                    "result_comparison": True
                },
                "best_for": [
                    "Quality-focused applications",
                    "Research documents",
                    "Performance analysis",
                    "A/B testing scenarios"
                ]
            },
            "aggressive": {
                "name": "Aggressive Mode", 
                "description": "Maximum quality regardless of cost",
                "ai_usage_target": "80%",
                "cost": "High",
                "speed": "Medium",
                "quality": "Maximum",
                "characteristics": {
                    "local_confidence_threshold": 0.1,
                    "complexity_threshold": 0.3,
                    "cost_optimization": False,
                    "quality_priority": True
                },
                "best_for": [
                    "Critical documents",
                    "Publication-ready content",
                    "Premium quality requirements",
                    "Low-volume high-stakes processing"
                ]
            },
            "turnitin_safe": {
                "name": "Turnitin-Safe Mode",
                "description": "Extra protection against plagiarism detection systems",
                "ai_usage_target": "60%",
                "cost": "Medium-High", 
                "speed": "Medium",
                "quality": "Very High",
                "characteristics": {
                    "turnitin_detection": True,
                    "similarity_database_check": True,
                    "local_confidence_threshold": 0.35,
                    "plagiarism_risk_threshold": 0.9
                },
                "best_for": [
                    "Academic submissions",
                    "Institutional requirements",
                    "Anti-plagiarism compliance",
                    "Student assignments"
                ]
            }
        },
        "mode_selection_guide": {
            "cost_sensitive": "smart",
            "quality_focused": "balanced", 
            "maximum_quality": "aggressive",
            "plagiarism_protection": "turnitin_safe",
            "high_volume": "smart",
            "research_papers": "balanced",
            "student_work": "turnitin_safe",
            "business_documents": "smart"
        },
        "performance_comparison": {
            "processing_speed": {
                "smart": "1-3 seconds",
                "balanced": "2-4 seconds", 
                "aggressive": "3-6 seconds",
                "turnitin_safe": "2-5 seconds"
            },
            "quality_range": {
                "smart": "85-92%",
                "balanced": "88-95%",
                "aggressive": "92-98%", 
                "turnitin_safe": "88-94%"
            },
            "typical_cost": {
                "smart": "$0.000-$0.002",
                "balanced": "$0.001-$0.004",
                "aggressive": "$0.003-$0.008",
                "turnitin_safe": "$0.002-$0.006"
            }
        }
    }
    
    return SuccessResponse(
        success=True,
        message="Ultimate Hybrid processing modes information",
        data=modes
    )

@router.get("/features", response_model=SuccessResponse) 
async def get_ultimate_hybrid_features():
    """
    Get detailed information about Ultimate Hybrid features and capabilities
    
    Returns comprehensive documentation about what makes Ultimate Hybrid
    different from other paraphrasing systems and when to use it.
    """
    features = {
        "core_features": {
            "smart_routing": {
                "name": "Intelligent Processing Routing",
                "description": "Automatically decides between local and AI processing based on content analysis",
                "benefits": ["Cost optimization", "Quality assurance", "Efficiency"],
                "algorithms": ["Complexity analysis", "Academic pattern detection", "Risk assessment"]
            },
            "multi_mode_processing": {
                "name": "Multiple Processing Modes",
                "description": "Four distinct modes optimized for different use cases",
                "modes": ["Smart", "Balanced", "Aggressive", "Turnitin-Safe"],
                "dynamic_switching": True
            },
            "turnitin_detection": {
                "name": "Turnitin Risk Pattern Detection",
                "description": "Advanced detection of common plagiarism patterns flagged by Turnitin",
                "patterns": ["Academic phrases", "Research terminology", "Citation patterns"],
                "protection_level": "High"
            },
            "cost_optimization": {
                "name": "Advanced Cost Management",
                "description": "Intelligent cost optimization with quality preservation",
                "features": ["AI usage prediction", "Cost per paragraph tracking", "Budget optimization"]
            },
            "ai_caching": {
                "name": "Smart AI Result Caching", 
                "description": "Caches AI results to avoid duplicate processing costs",
                "cache_strategy": "Content-based hashing",
                "efficiency_gain": "Up to 70% cost reduction on repeated content"
            },
            "text_analysis": {
                "name": "Deep Text Characteristics Analysis",
                "description": "Comprehensive analysis of text properties for optimal processing",
                "analysis_points": ["Complexity", "Academic content", "Technical patterns", "Length distribution"]
            }
        },
        "comparison_vs_other_systems": {
            "vs_smart_efficient": {
                "routing": "Enhanced vs Basic",
                "modes": "4 modes vs 1 mode",
                "turnitin_detection": "Advanced vs None",
                "cost_optimization": "Multi-layer vs Basic"
            },
            "vs_full_gemini": {
                "processing": "Hybrid vs AI-only",
                "cost": "Optimized vs Premium",
                "flexibility": "Multi-mode vs Single approach",
                "speed": "Variable vs Consistent"
            }
        },
        "use_case_matrix": {
            "academic_research": {
                "recommended_mode": "balanced",
                "reasoning": "Quality comparison with cost awareness",
                "features": ["Academic pattern detection", "Citation protection", "Quality analysis"]
            },
            "student_assignments": {
                "recommended_mode": "turnitin_safe",
                "reasoning": "Maximum protection against detection",
                "features": ["Turnitin risk analysis", "Pattern avoidance", "Safety focus"]
            },
            "business_documents": {
                "recommended_mode": "smart",
                "reasoning": "Professional quality with cost efficiency",
                "features": ["Cost optimization", "Fast processing", "Reliable quality"]
            },
            "high_volume_processing": {
                "recommended_mode": "smart",
                "reasoning": "Scalable with consistent quality",
                "features": ["Batch optimization", "Cost control", "Cache utilization"]
            },
            "premium_content": {
                "recommended_mode": "aggressive",
                "reasoning": "Maximum quality regardless of cost",
                "features": ["AI-heavy processing", "Quality maximization", "Premium results"]
            }
        },
        "technical_specifications": {
            "text_length_support": "10-15,000 characters",
            "batch_size_limit": 100,
            "processing_languages": ["Indonesian (primary)", "Academic English"],
            "ai_models_supported": ["Gemini 1.5 Flash", "Gemini 1.5 Pro"],
            "caching_algorithm": "MD5-based content hashing",
            "routing_algorithms": ["Complexity scoring", "Pattern matching", "Risk assessment"]
        }
    }
    
    return SuccessResponse(
        success=True,
        message="Ultimate Hybrid features and capabilities",
        data=features
    )

@router.get("/info", response_model=SuccessResponse)
async def get_service_info(
    service: UltimateHybridService = Depends(get_ultimate_hybrid_service)
):
    """
    Get Ultimate Hybrid service configuration and availability information
    
    Returns current service status, configuration, and capability information.
    """
    try:
        info = await service.get_service_info()
        return SuccessResponse(
            success=True,
            message="Ultimate Hybrid service information retrieved",
            data=info
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve service info: {str(e)}"
        )

# Placeholder for document processing
@router.post("/document")
async def ultimate_hybrid_paraphrase_document():
    """
    Ultimate Hybrid document paraphrasing (TODO: Implement)
    
    This endpoint will handle document upload and paraphrasing using
    the Ultimate Hybrid system with intelligent mode selection and
    comprehensive document analysis.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Ultimate Hybrid document paraphrasing not yet implemented"
    )