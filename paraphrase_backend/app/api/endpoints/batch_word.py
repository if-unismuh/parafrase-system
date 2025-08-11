"""
Batch Word Paraphrasing endpoints
Direct Word document modification for academic thesis chapters
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import List, Optional, Dict, Any
import json

from app.core.config import get_settings, Settings
from app.services.batch_word_service import BatchWordService
from app.api.models.batch_word import (
    ProcessDocumentsRequest,
    BatchWordResponse,
    BabSectionsRequest,
    BabSectionsResponse,
    BatchWordStatsResponse,
    DocumentAnalysisResponse
)
from app.api.models.common import SuccessResponse
from app.core.exceptions import ParaphraseAPIException

router = APIRouter()

# Dependency to get Batch Word service
def get_batch_word_service(settings: Settings = Depends(get_settings)) -> BatchWordService:
    """Dependency to get Batch Word service instance"""
    return BatchWordService(settings)

@router.post("/process-documents", response_model=BatchWordResponse)
async def process_word_documents(
    files: List[UploadFile] = File(..., description="Word documents to process (.docx files)"),
    aggressiveness: float = Form(0.5, description="Aggressiveness level (0.1-1.0)"),
    create_backup: bool = Form(True, description="Create backup copies"),
    min_paragraph_length: int = Form(30, description="Minimum paragraph length (words)"),
    improvement_threshold: float = Form(20.0, description="Minimum improvement threshold (%)"),
    highlight_changes: bool = Form(True, description="Highlight paraphrased sections"),
    service: BatchWordService = Depends(get_batch_word_service)
):
    """
    Process Multiple Word Documents - Direct File Modification
    
    This endpoint processes multiple Word documents (primarily academic thesis chapters)
    by directly modifying the original files with intelligent paraphrasing. Designed
    specifically for BAB 1-3 academic content with priority-based section processing.
    
    **Key Features:**
    - 📄 **Direct Modification**: Modifies original Word files in-place
    - 🎓 **Academic Focus**: Optimized for thesis chapters (BAB 1-3)
    - 📊 **Priority Sections**: Different processing levels for different content types
    - 💾 **Automatic Backup**: Creates backup copies before modification
    - 🎨 **Formatting Preservation**: Maintains original document formatting
    - ✨ **Change Highlighting**: Highlights modified sections for review
    
    **Academic Section Priorities:**
    - **High Priority**: Latar belakang, Landasan teori, Tinjauan pustaka
    - **Medium Priority**: Metodologi, Metode penelitian, Rumusan masalah
    - **Low Priority**: Manfaat penelitian, Sistematika penulisan
    
    **Processing Intelligence:**
    - Automatically detects document sections and chapters
    - Applies different aggressiveness levels based on content type
    - Skips references, tables, and figures automatically
    - Preserves academic formatting and structure
    
    **Parameters:**
    - **files**: Word document files (.docx format only)
    - **aggressiveness**: Base aggressiveness level (0.1 = conservative, 1.0 = maximum)
    - **create_backup**: Create backup copies before processing
    - **min_paragraph_length**: Minimum words in paragraph to consider for paraphrasing
    - **improvement_threshold**: Minimum similarity reduction required to apply changes
    - **highlight_changes**: Highlight paraphrased sections in yellow
    
    **Response includes:**
    - Individual processing results for each document
    - Section-by-section analysis and improvements
    - Backup file locations and processing statistics
    - Detailed processing report with effectiveness metrics
    """
    try:
        # Validate file types
        for file in files:
            if not file.filename.endswith('.docx'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Only .docx files are supported. Invalid file: {file.filename}"
                )
        
        # Save uploaded files
        upload_infos = await service.save_uploaded_files(files)
        file_paths = [info.upload_path for info in upload_infos]
        
        # Create processing request
        request = ProcessDocumentsRequest(
            aggressiveness=aggressiveness,
            create_backup=create_backup,
            min_paragraph_length=min_paragraph_length,
            improvement_threshold=improvement_threshold,
            highlight_changes=highlight_changes
        )
        
        # Process documents
        result = await service.process_documents(request, file_paths)
        
        return BatchWordResponse(
            success=True,
            message=f"Batch processing completed: {result.summary.successful_documents}/{result.summary.total_documents} documents processed successfully",
            data=result
        )
        
    except ParaphraseAPIException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch Word document processing failed: {str(e)}"
        )

@router.post("/bab-sections", response_model=BabSectionsResponse)
async def process_bab_sections(
    files: List[UploadFile] = File(..., description="Word documents containing BAB sections"),
    sections_to_process: str = Form(
        '["bab_1", "bab_2", "bab_3"]',
        description="JSON array of BAB sections to process"
    ),
    focus_areas: str = Form(
        '["latar belakang", "landasan teori", "metodologi penelitian"]',
        description="JSON array of focus areas"
    ),
    aggressiveness_by_section: Optional[str] = Form(
        None,
        description="JSON object mapping sections to aggressiveness levels"
    ),
    create_backup: bool = Form(True, description="Create backup copies"),
    preserve_formatting: bool = Form(True, description="Preserve document formatting"),
    service: BatchWordService = Depends(get_batch_word_service)
):
    """
    Process Specific BAB (Chapter) Sections - Academic Thesis Focus
    
    This endpoint is specifically designed for processing Indonesian academic thesis
    chapters (BAB 1, BAB 2, BAB 3) with targeted focus on the most important sections
    for plagiarism reduction while preserving academic integrity.
    
    **BAB-Specific Processing:**
    - 📚 **BAB I (Pendahuluan)**: Focus on latar belakang, rumusan masalah
    - 🔬 **BAB II (Tinjauan Pustaka)**: Emphasis on landasan teori, konsep
    - 🛠️ **BAB III (Metodologi)**: Careful processing of metode penelitian
    
    **Smart Section Recognition:**
    - Automatically detects BAB headers and section divisions
    - Identifies key academic sections within each BAB
    - Applies appropriate processing intensity per section type
    - Preserves citation formats and academic references
    
    **Customizable Processing:**
    - Different aggressiveness levels per BAB or section
    - Configurable focus areas for targeted improvement
    - Flexible section selection for partial processing
    - Academic formatting and structure preservation
    
    **Parameters:**
    - **files**: Word documents containing BAB sections
    - **sections_to_process**: List of BAB sections to focus on
    - **focus_areas**: Specific content areas to prioritize
    - **aggressiveness_by_section**: Custom aggressiveness per section (JSON object)
    - **create_backup**: Create backup copies before processing
    - **preserve_formatting**: Maintain original academic formatting
    
    **Supported Sections:**
    - `bab_1`, `bab_2`, `bab_3`, `bab_4`, `bab_5`
    - `pendahuluan`, `tinjauan_pustaka`, `metodologi`
    - `hasil`, `pembahasan`, `kesimpulan`
    
    **Response includes:**
    - BAB-specific processing analysis
    - Section coverage and effectiveness metrics
    - Focus area achievement statistics
    - Detailed academic content improvements
    """
    try:
        # Validate and parse JSON parameters
        try:
            sections_list = json.loads(sections_to_process)
            focus_areas_list = json.loads(focus_areas)
            aggressiveness_dict = json.loads(aggressiveness_by_section) if aggressiveness_by_section else None
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid JSON in parameters: {str(e)}"
            )
        
        # Validate file types
        for file in files:
            if not file.filename.endswith('.docx'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Only .docx files are supported. Invalid file: {file.filename}"
                )
        
        # Save uploaded files
        upload_infos = await service.save_uploaded_files(files)
        file_paths = [info.upload_path for info in upload_infos]
        
        # Create BAB processing request
        request = BabSectionsRequest(
            sections_to_process=sections_list,
            aggressiveness_by_section=aggressiveness_dict,
            focus_areas=focus_areas_list,
            create_backup=create_backup,
            preserve_formatting=preserve_formatting
        )
        
        # Process BAB sections
        result = await service.process_bab_sections(request, file_paths)
        
        return BabSectionsResponse(
            success=True,
            message=f"BAB sections processing completed: {len(result.sections_processed)} sections processed in {result.summary.successful_documents} documents",
            data=result
        )
        
    except ParaphraseAPIException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"BAB sections processing failed: {str(e)}"
        )

@router.post("/analyze", response_model=DocumentAnalysisResponse)
async def analyze_documents(
    files: List[UploadFile] = File(..., description="Word documents to analyze"),
    service: BatchWordService = Depends(get_batch_word_service)
):
    """
    Analyze Word Documents Before Processing
    
    Performs comprehensive analysis of Word documents to provide insights about
    their structure, content, and suitability for batch processing. This analysis
    helps determine optimal processing parameters and expected outcomes.
    
    **Analysis Capabilities:**
    - 📊 **Document Structure**: Paragraphs, sections, and chapters detection
    - 🎓 **Academic Content**: Identification of thesis sections and priorities  
    - 📈 **Processing Suitability**: Score indicating how well suited for batch processing
    - ⚙️ **Parameter Recommendations**: Suggested aggressiveness and settings
    - ⏱️ **Time Estimation**: Expected processing time and resource requirements
    
    **Detailed Analysis:**
    - Total paragraph count and distribution
    - Academic section detection (BAB, methodology, theory, etc.)
    - Content complexity assessment
    - Recommended processing parameters
    - Suitability score for different processing modes
    
    **Use Cases:**
    - Pre-processing assessment for optimal parameter selection
    - Batch processing planning and resource estimation
    - Document quality and structure evaluation
    - Academic content categorization and prioritization
    
    **Response includes:**
    - Per-document analysis with structure breakdown
    - Section detection and priority classification
    - Processing recommendations and parameter suggestions
    - Time and resource estimation for batch processing
    """
    try:
        # Validate file types
        for file in files:
            if not file.filename.endswith('.docx'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Only .docx files are supported. Invalid file: {file.filename}"
                )
        
        # Save uploaded files
        upload_infos = await service.save_uploaded_files(files)
        file_paths = [info.upload_path for info in upload_infos]
        
        # Analyze documents
        analyses = await service.analyze_documents(file_paths)
        
        return DocumentAnalysisResponse(
            success=True,
            message=f"Document analysis completed for {len(analyses)} documents",
            data=analyses
        )
        
    except ParaphraseAPIException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document analysis failed: {str(e)}"
        )

@router.get("/stats", response_model=BatchWordStatsResponse)
async def get_batch_word_statistics(
    service: BatchWordService = Depends(get_batch_word_service)
):
    """
    Get Batch Word Processing Statistics and Performance Metrics
    
    Returns comprehensive statistics about batch Word processing performance
    including processing volumes, success rates, and effectiveness metrics.
    
    **Statistics Provided:**
    - Processing volume and document success rates
    - Average processing times and performance metrics
    - Section priority effectiveness and improvement rates
    - Most common document types and processing patterns
    - Aggressiveness level usage and optimization insights
    """
    try:
        stats = await service.get_processing_stats()
        return BatchWordStatsResponse(
            success=True,
            message="Batch Word processing statistics retrieved",
            data=stats
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve batch word stats: {str(e)}"
        )

@router.get("/features", response_model=SuccessResponse)
async def get_batch_word_features():
    """
    Get detailed information about Batch Word features and capabilities
    
    Returns comprehensive documentation about the Batch Word system's
    unique features, academic focus, and specialized capabilities.
    """
    features = {
        "core_capabilities": {
            "direct_file_modification": {
                "name": "Direct Word Document Modification",
                "description": "Directly modifies original .docx files with intelligent paraphrasing",
                "benefits": ["No format conversion", "Preserves all formatting", "In-place processing"],
                "safety_features": ["Automatic backup creation", "Change highlighting", "Rollback support"]
            },
            "academic_optimization": {
                "name": "Academic Thesis Optimization",
                "description": "Specialized processing for Indonesian academic thesis chapters",
                "focus_areas": ["BAB 1-3 processing", "Thesis chapter structure", "Academic vocabulary"],
                "section_priorities": {
                    "high_priority": ["Latar belakang", "Landasan teori", "Tinjauan pustaka"],
                    "medium_priority": ["Metodologi", "Metode penelitian", "Rumusan masalah"],
                    "low_priority": ["Manfaat penelitian", "Sistematika penulisan"]
                }
            },
            "intelligent_section_detection": {
                "name": "Smart Academic Section Recognition",
                "description": "Automatically detects and categorizes academic document sections",
                "detection_patterns": ["BAB headers", "Section numbering", "Academic keywords"],
                "processing_adaptation": "Adjusts processing strategy based on detected content type"
            },
            "batch_processing_engine": {
                "name": "Efficient Batch Processing",
                "description": "Processes multiple documents with consistent quality and performance",
                "capabilities": ["Parallel processing", "Progress tracking", "Error handling"],
                "scalability": "Up to 20 documents per batch with 50MB size limit"
            }
        },
        "academic_specialization": {
            "thesis_chapter_focus": {
                "bab_1_pendahuluan": {
                    "sections": ["Latar belakang", "Rumusan masalah", "Tujuan penelitian"],
                    "processing_strategy": "High priority with conservative approach",
                    "special_handling": "Preserves problem statement clarity"
                },
                "bab_2_tinjauan_pustaka": {
                    "sections": ["Landasan teori", "Kajian teori", "Penelitian terkait"],
                    "processing_strategy": "Maximum priority with aggressive paraphrasing",
                    "special_handling": "Citation-aware processing"
                },
                "bab_3_metodologi": {
                    "sections": ["Metode penelitian", "Teknik analisis", "Populasi sampel"],
                    "processing_strategy": "Medium priority with careful approach",
                    "special_handling": "Preserves methodological precision"
                }
            },
            "content_preservation": {
                "protected_elements": ["Citations and references", "Tables and figures", "Mathematical formulas"],
                "formatting_preservation": ["Headers and styles", "Numbering systems", "Academic formatting"],
                "structure_maintenance": ["Chapter organization", "Section hierarchy", "Page layouts"]
            }
        },
        "processing_intelligence": {
            "adaptive_aggressiveness": {
                "description": "Adjusts processing intensity based on content type",
                "factors": ["Section priority", "Content complexity", "Academic importance"],
                "customization": "User-configurable per section or document type"
            },
            "quality_assurance": {
                "improvement_threshold": "Configurable minimum improvement requirement",
                "change_validation": "Validates improvements before applying",
                "rollback_capability": "Can revert changes if quality decreases"
            },
            "progress_tracking": {
                "real_time_updates": "Live processing progress and status",
                "error_handling": "Graceful error recovery and reporting",
                "detailed_logging": "Comprehensive processing logs and reports"
            }
        },
        "comparison_vs_other_systems": {
            "vs_smart_efficient": {
                "focus": "Academic documents vs General text",
                "processing": "Direct file modification vs Text-based",
                "specialization": "Thesis-specific vs General purpose",
                "output": "Modified documents vs Paraphrased text"
            },
            "vs_full_gemini": {
                "approach": "Local + structure-aware vs AI-heavy",
                "cost": "Free local processing vs Premium AI",
                "speed": "Fast batch processing vs Quality-focused",
                "specialization": "Academic structure vs General quality"
            },
            "vs_ultimate_hybrid": {
                "target": "Document modification vs Text paraphrasing", 
                "workflow": "File-centric vs Text-centric",
                "academic_focus": "Thesis-specific vs General academic",
                "output_format": "Original documents vs Processed text"
            }
        },
        "ideal_use_cases": {
            "thesis_preparation": {
                "description": "Complete thesis chapter processing for academic submission",
                "workflow": "Upload thesis → Section detection → Priority processing → Download improved thesis",
                "benefits": ["Maintains academic structure", "Reduces plagiarism risk", "Preserves formatting"]
            },
            "academic_batch_processing": {
                "description": "Process multiple academic documents simultaneously",
                "workflow": "Bulk upload → Batch analysis → Automated processing → Consolidated reporting",
                "benefits": ["Consistent quality", "Time efficiency", "Comprehensive reporting"]
            },
            "institutional_processing": {
                "description": "Academic institution bulk document improvement",
                "workflow": "Department-wide processing → Quality standardization → Compliance reporting",
                "benefits": ["Institutional consistency", "Quality assurance", "Audit trails"]
            }
        },
        "technical_specifications": {
            "supported_formats": [".docx (Microsoft Word 2007+)"],
            "file_size_limits": "50MB per document, 20 documents per batch",
            "processing_performance": "~20 paragraphs per minute average",
            "backup_systems": "Automatic timestamped backups with rollback capability",
            "change_tracking": "Visual highlighting and detailed change reports",
            "output_preservation": "100% formatting and structure preservation"
        }
    }
    
    return SuccessResponse(
        success=True,
        message="Batch Word features and capabilities",
        data=features
    )

@router.get("/supported-sections", response_model=SuccessResponse)
async def get_supported_sections():
    """
    Get information about supported academic sections and processing priorities
    
    Returns detailed information about which document sections are supported
    and how they are prioritized during processing.
    """
    sections = {
        "bab_chapters": {
            "name": "BAB (Chapter) Sections",
            "description": "Indonesian academic thesis chapter structure",
            "supported_sections": {
                "bab_1": {
                    "name": "BAB I - Pendahuluan",
                    "common_subsections": ["Latar belakang", "Rumusan masalah", "Tujuan penelitian", "Manfaat penelitian"],
                    "priority": "High",
                    "processing_notes": "Conservative approach to preserve problem clarity"
                },
                "bab_2": {
                    "name": "BAB II - Tinjauan Pustaka",
                    "common_subsections": ["Landasan teori", "Kajian teori", "Penelitian terkait", "Kerangka berpikir"],
                    "priority": "Maximum",
                    "processing_notes": "Aggressive paraphrasing with citation protection"
                },
                "bab_3": {
                    "name": "BAB III - Metodologi Penelitian",
                    "common_subsections": ["Metode penelitian", "Populasi dan sampel", "Teknik pengumpulan data"],
                    "priority": "Medium",
                    "processing_notes": "Careful approach to preserve methodological precision"
                },
                "bab_4": {
                    "name": "BAB IV - Hasil dan Pembahasan",
                    "common_subsections": ["Hasil penelitian", "Pembahasan", "Analisis data"],
                    "priority": "Medium",
                    "processing_notes": "Balanced processing with data integrity protection"
                },
                "bab_5": {
                    "name": "BAB V - Kesimpulan dan Saran",
                    "common_subsections": ["Kesimpulan", "Saran", "Keterbatasan penelitian"],
                    "priority": "Low",
                    "processing_notes": "Light processing to maintain conclusion clarity"
                }
            }
        },
        "content_sections": {
            "name": "Content-Based Sections",
            "description": "Academic content types regardless of chapter structure",
            "supported_sections": {
                "pendahuluan": {"priority": "High", "typical_location": "BAB I"},
                "tinjauan_pustaka": {"priority": "Maximum", "typical_location": "BAB II"},
                "metodologi": {"priority": "Medium", "typical_location": "BAB III"},
                "hasil": {"priority": "Medium", "typical_location": "BAB IV"},
                "pembahasan": {"priority": "Medium", "typical_location": "BAB IV"},
                "kesimpulan": {"priority": "Low", "typical_location": "BAB V"}
            }
        },
        "priority_system": {
            "high_priority": {
                "description": "Sections requiring aggressive paraphrasing",
                "sections": ["latar belakang", "landasan teori", "tinjauan pustaka", "kajian teori"],
                "aggressiveness_bonus": "+0.2 (up to 0.8 max)",
                "rationale": "These sections often contain literature that needs significant paraphrasing"
            },
            "medium_priority": {
                "description": "Sections requiring balanced processing",
                "sections": ["metodologi", "metode penelitian", "rumusan masalah", "tujuan penelitian"],
                "aggressiveness_bonus": "Base level (no adjustment)",
                "rationale": "Important sections that need careful but moderate processing"
            },
            "low_priority": {
                "description": "Sections requiring conservative processing",
                "sections": ["manfaat penelitian", "sistematika penulisan", "batasan masalah"],
                "aggressiveness_bonus": "-0.2 (down to 0.3 min)",
                "rationale": "Structural sections that should maintain clarity and simplicity"
            }
        },
        "section_detection": {
            "detection_methods": [
                "BAB header patterns (BAB I, BAB II, etc.)",
                "Numbered section patterns (1.1, 2.3, etc.)",
                "Keyword-based content classification",
                "Document structure analysis"
            ],
            "customization": {
                "custom_sections": "Users can define custom section priorities",
                "keyword_mapping": "Flexible keyword-to-priority mapping",
                "pattern_override": "Override automatic detection with manual settings"
            }
        }
    }
    
    return SuccessResponse(
        success=True,
        message="Supported academic sections and priority information",
        data=sections
    )

@router.get("/info", response_model=SuccessResponse)
async def get_service_info(
    service: BatchWordService = Depends(get_batch_word_service)
):
    """
    Get Batch Word service configuration and availability information
    
    Returns current service status, configuration, and capability information.
    """
    try:
        info = await service.get_service_info()
        return SuccessResponse(
            success=True,
            message="Batch Word service information retrieved",
            data=info
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve service info: {str(e)}"
        )