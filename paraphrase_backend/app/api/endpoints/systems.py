"""
Paraphrasing Systems Overview and Comparison endpoints
"""
from fastapi import APIRouter, Depends
from typing import Dict, Any, List

from app.core.config import get_settings, Settings
from app.api.models.common import SuccessResponse

router = APIRouter()

@router.get("/", response_model=SuccessResponse)
async def get_all_systems():
    """
    Get overview of all available paraphrasing systems
    
    Returns comprehensive information about all paraphrasing systems
    available in the API, their features, use cases, and characteristics.
    """
    systems = {
        "smart_efficient": {
            "name": "Smart Efficient Paraphraser",
            "version": "1.0",
            "status": "active",
            "description": "Cost-effective paraphrasing with DDGS search enhancement",
            "endpoints": [
                "/api/v1/paraphrase/smart-efficient/text",
                "/api/v1/paraphrase/smart-efficient/batch",
                "/api/v1/paraphrase/smart-efficient/stats"
            ],
            "features": {
                "ddgs_search": True,
                "local_processing": True,
                "ai_backup": True,
                "cost_optimization": True,
                "batch_processing": True,
                "document_processing": True
            },
            "characteristics": {
                "speed": "fast",
                "quality": "good",
                "cost": "low",
                "scalability": "high"
            },
            "best_for": [
                "Daily usage",
                "High-volume processing", 
                "Cost-sensitive applications",
                "Quick turnaround needs"
            ]
        },
        "full_gemini": {
            "name": "Full Gemini AI Paraphraser",
            "version": "1.0", 
            "status": "active",
            "description": "Premium quality paraphrasing using complete Gemini AI pipeline",
            "endpoints": [
                "/api/v1/paraphrase/full-gemini/text",
                "/api/v1/paraphrase/full-gemini/batch",
                "/api/v1/paraphrase/full-gemini/stats",
                "/api/v1/paraphrase/full-gemini/features"
            ],
            "features": {
                "full_ai_processing": True,
                "content_protection": True,
                "academic_optimization": True,
                "premium_quality": True,
                "advanced_models": True,
                "quality_focus": True
            },
            "characteristics": {
                "speed": "medium",
                "quality": "excellent",
                "cost": "medium",
                "scalability": "medium"
            },
            "best_for": [
                "Academic papers",
                "Professional documents",
                "High-quality content",
                "Premium applications"
            ]
        },
        "ultimate_hybrid": {
            "name": "Ultimate Hybrid Paraphraser",
            "version": "3.0",
            "status": "active",
            "description": "All-in-one solution with smart routing and Turnitin detection",
            "endpoints": [
                "/api/v1/paraphrase/ultimate-hybrid/text",
                "/api/v1/paraphrase/ultimate-hybrid/batch",
                "/api/v1/paraphrase/ultimate-hybrid/multi-options",
                "/api/v1/paraphrase/ultimate-hybrid/modes",
                "/api/v1/paraphrase/ultimate-hybrid/stats"
            ],
            "features": {
                "smart_routing": True,
                "turnitin_detection": True,
                "multiple_modes": True,
                "advanced_ai": True,
                "pattern_analysis": True,
                "risk_assessment": True
            },
            "characteristics": {
                "speed": "medium",
                "quality": "excellent", 
                "cost": "medium_high",
                "scalability": "medium"
            },
            "best_for": [
                "Professional documents",
                "Anti-plagiarism requirements",
                "Complex processing needs",
                "Multi-modal workflows"
            ]
        },
        "integrated_smart": {
            "name": "Integrated Smart Paraphrase System",
            "version": "1.0",
            "status": "active", 
            "description": "Complete workflow with online plagiarism detection",
            "endpoints": [
                "/api/v1/paraphrase/integrated-smart/analyze-and-paraphrase",
                "/api/v1/paraphrase/integrated-smart/plagiarism-check",
                "/api/v1/paraphrase/integrated-smart/batch",
                "/api/v1/paraphrase/integrated-smart/workflow-stats",
                "/api/v1/paraphrase/integrated-smart/features"
            ],
            "features": {
                "plagiarism_detection": True,
                "workflow_automation": True,
                "risk_analysis": True,
                "comprehensive_reporting": True,
                "online_checking": True,
                "automated_processing": True
            },
            "characteristics": {
                "speed": "slow",
                "quality": "high",
                "cost": "medium",
                "scalability": "low"
            },
            "best_for": [
                "Academic research",
                "Publication requirements",
                "Complete document analysis",
                "Workflow automation"
            ]
        },
        "batch_word": {
            "name": "Batch Word Paraphraser",
            "version": "1.0",
            "status": "active",
            "description": "Direct Word document modification for thesis chapters",
            "endpoints": [
                "/api/v1/paraphrase/batch-word/process-documents",
                "/api/v1/paraphrase/batch-word/bab-sections",
                "/api/v1/paraphrase/batch-word/analyze",
                "/api/v1/paraphrase/batch-word/stats",
                "/api/v1/paraphrase/batch-word/features"
            ],
            "features": {
                "word_direct_modification": True,
                "chapter_processing": True,
                "priority_sections": True,
                "bulk_processing": True,
                "file_modification": True,
                "academic_focus": True
            },
            "characteristics": {
                "speed": "fast",
                "quality": "good",
                "cost": "low",
                "scalability": "high"
            },
            "best_for": [
                "Academic thesis",
                "BAB 1-3 processing",
                "Bulk document modification", 
                "Direct file processing"
            ]
        }
    }
    
    return SuccessResponse(
        success=True,
        message="Available paraphrasing systems overview",
        data={
            "systems": systems,
            "total_systems": len(systems),
            "active_systems": len([s for s in systems.values() if s["status"] == "active"]),
            "development_systems": len([s for s in systems.values() if s["status"] == "development"])
        }
    )

@router.get("/comparison", response_model=SuccessResponse)
async def get_systems_comparison():
    """
    Get detailed comparison between all paraphrasing systems
    
    Returns a comprehensive comparison matrix showing differences
    in features, performance, costs, and use cases.
    """
    comparison = {
        "feature_matrix": {
            "ddgs_search": {
                "smart_efficient": True,
                "full_gemini": False,
                "ultimate_hybrid": True, 
                "integrated_smart": False,
                "batch_word": False
            },
            "full_ai_processing": {
                "smart_efficient": False,
                "full_gemini": True,
                "ultimate_hybrid": True,
                "integrated_smart": True,
                "batch_word": False
            },
            "content_protection": {
                "smart_efficient": True,
                "full_gemini": True,
                "ultimate_hybrid": True,
                "integrated_smart": True,
                "batch_word": True
            },
            "plagiarism_detection": {
                "smart_efficient": False,
                "full_gemini": False,
                "ultimate_hybrid": True,
                "integrated_smart": True,
                "batch_word": False
            },
            "batch_processing": {
                "smart_efficient": True,
                "full_gemini": True,
                "ultimate_hybrid": True,
                "integrated_smart": True,
                "batch_word": True
            },
            "document_upload": {
                "smart_efficient": True,
                "full_gemini": True,
                "ultimate_hybrid": True,
                "integrated_smart": True,
                "batch_word": True
            },
            "cost_optimization": {
                "smart_efficient": True,
                "full_gemini": False,
                "ultimate_hybrid": True,
                "integrated_smart": False,
                "batch_word": True
            }
        },
        "performance_comparison": {
            "processing_speed": {
                "smart_efficient": "1-2 seconds",
                "full_gemini": "3-5 seconds",
                "ultimate_hybrid": "2-4 seconds",
                "integrated_smart": "5-8 seconds",
                "batch_word": "0.5 seconds per document"
            },
            "quality_score": {
                "smart_efficient": "85-90%",
                "full_gemini": "95-98%",
                "ultimate_hybrid": "90-95%",
                "integrated_smart": "88-93%",
                "batch_word": "80-85%"
            },
            "cost_per_request": {
                "smart_efficient": "$0.00 (Free)",
                "full_gemini": "$0.002-$0.005",
                "ultimate_hybrid": "$0.001-$0.003",
                "integrated_smart": "$0.001-$0.003",
                "batch_word": "$0.00 (Free)"
            }
        },
        "use_case_recommendations": {
            "academic_research": {
                "recommended": ["full_gemini", "integrated_smart", "ultimate_hybrid"],
                "not_recommended": ["batch_word"]
            },
            "business_documents": {
                "recommended": ["full_gemini", "ultimate_hybrid", "smart_efficient"],
                "not_recommended": ["batch_word"]
            },
            "high_volume_processing": {
                "recommended": ["smart_efficient", "batch_word"],
                "not_recommended": ["integrated_smart"]
            },
            "cost_sensitive": {
                "recommended": ["smart_efficient", "batch_word"],
                "not_recommended": ["full_gemini"]
            },
            "premium_quality": {
                "recommended": ["full_gemini", "ultimate_hybrid"],
                "not_recommended": ["batch_word"]
            }
        }
    }
    
    return SuccessResponse(
        success=True,
        message="Comprehensive systems comparison",
        data=comparison
    )

@router.get("/recommend", response_model=SuccessResponse)
async def get_system_recommendation(
    text_length: int = 1000,
    quality_requirement: str = "medium",  # low, medium, high, premium
    cost_sensitivity: str = "medium",     # low, medium, high
    processing_volume: str = "medium",    # low, medium, high
    document_type: str = "general"        # general, academic, business, thesis
):
    """
    Get personalized system recommendation based on requirements
    
    Analyzes your specific needs and recommends the best paraphrasing
    system based on text characteristics, quality needs, and constraints.
    
    **Parameters:**
    - **text_length**: Approximate text length in characters
    - **quality_requirement**: Required quality level
    - **cost_sensitivity**: How important is cost optimization
    - **processing_volume**: Expected processing volume
    - **document_type**: Type of documents to process
    """
    
    def calculate_recommendation_score(system: str, requirements: dict) -> float:
        """Calculate recommendation score for a system"""
        scores = {
            "smart_efficient": {
                "cost_efficiency": 95,
                "speed": 90,
                "quality": 75,
                "volume_handling": 95,
                "academic": 70,
                "business": 80
            },
            "full_gemini": {
                "cost_efficiency": 30,
                "speed": 60,
                "quality": 95,
                "volume_handling": 60,
                "academic": 95,
                "business": 90
            },
            "ultimate_hybrid": {
                "cost_efficiency": 60,
                "speed": 70,
                "quality": 90,
                "volume_handling": 75,
                "academic": 85,
                "business": 95
            },
            "integrated_smart": {
                "cost_efficiency": 50,
                "speed": 40,
                "quality": 85,
                "volume_handling": 40,
                "academic": 90,
                "business": 70
            },
            "batch_word": {
                "cost_efficiency": 90,
                "speed": 95,
                "quality": 70,
                "volume_handling": 90,
                "academic": 80,
                "business": 60
            }
        }
        
        if system not in scores:
            return 0.0
        
        system_scores = scores[system]
        total_score = 0.0
        total_weight = 0.0
        
        for requirement, weight in requirements.items():
            if requirement in system_scores:
                total_score += system_scores[requirement] * weight
                total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    # Convert requirements to weights
    quality_weights = {
        "low": {"quality": 1, "cost_efficiency": 3, "speed": 2},
        "medium": {"quality": 2, "cost_efficiency": 2, "speed": 1},
        "high": {"quality": 3, "cost_efficiency": 1, "speed": 1},
        "premium": {"quality": 4, "cost_efficiency": 0, "speed": 1}
    }
    
    cost_weights = {
        "low": 0.5,    # Cost not important
        "medium": 1.0, # Cost somewhat important
        "high": 2.0    # Cost very important
    }
    
    volume_weights = {
        "low": {"volume_handling": 1, "speed": 1},
        "medium": {"volume_handling": 2, "speed": 1},
        "high": {"volume_handling": 3, "speed": 2}
    }
    
    document_weights = {
        "general": {"quality": 1},
        "academic": {"academic": 2, "quality": 1},
        "business": {"business": 2, "quality": 1},
        "thesis": {"academic": 3, "quality": 2}
    }
    
    # Build requirements dictionary
    requirements = {}
    
    # Add quality requirements
    for req, weight in quality_weights.get(quality_requirement, {}).items():
        requirements[req] = requirements.get(req, 0) + weight
    
    # Add cost sensitivity
    cost_weight = cost_weights.get(cost_sensitivity, 1.0)
    requirements["cost_efficiency"] = requirements.get("cost_efficiency", 0) * cost_weight
    
    # Add volume requirements
    for req, weight in volume_weights.get(processing_volume, {}).items():
        requirements[req] = requirements.get(req, 0) + weight
    
    # Add document type requirements
    for req, weight in document_weights.get(document_type, {}).items():
        requirements[req] = requirements.get(req, 0) + weight
    
    # Calculate scores for all systems
    system_scores = {}
    systems = ["smart_efficient", "full_gemini", "ultimate_hybrid", "integrated_smart", "batch_word"]
    
    for system in systems:
        system_scores[system] = calculate_recommendation_score(system, requirements)
    
    # Sort by score
    sorted_systems = sorted(system_scores.items(), key=lambda x: x[1], reverse=True)
    
    recommendations = []
    for i, (system, score) in enumerate(sorted_systems):
        recommendations.append({
            "rank": i + 1,
            "system": system,
            "score": round(score, 1),
            "confidence": "high" if score > 80 else "medium" if score > 60 else "low"
        })
    
    return SuccessResponse(
        success=True,
        message="Personalized system recommendation",
        data={
            "input_parameters": {
                "text_length": text_length,
                "quality_requirement": quality_requirement,
                "cost_sensitivity": cost_sensitivity,
                "processing_volume": processing_volume,
                "document_type": document_type
            },
            "recommendations": recommendations,
            "top_choice": recommendations[0] if recommendations else None,
            "explanation": f"Based on your {quality_requirement} quality requirement, {cost_sensitivity} cost sensitivity, and {document_type} document type, we recommend {recommendations[0]['system'] if recommendations else 'smart_efficient'} system."
        }
    )