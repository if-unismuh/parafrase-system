"""
Batch Word Paraphrasing service
Business logic for batch Word document processing and direct file modification
"""
import time
import os
import tempfile
import shutil
from typing import List, Optional, Dict, Any, BinaryIO
from pathlib import Path
from datetime import datetime
import sys
import json

# Add the parent directory to sys.path to import BatchWordParaphraser
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

# Mock the batch word paraphraser imports for now - we'll implement the actual integration later
# from batch_word_paraphraser import BatchWordParaphraser

from app.core.config import Settings
from app.core.exceptions import (
    ParaphrasingFailedError,
    TextTooLongError,
    TextTooShortError,
    ProcessingError,
    AIServiceError
)
from app.api.models.batch_word import (
    ProcessDocumentsRequest,
    BabSectionsRequest,
    BatchProcessingResult,
    BabSectionsProcessingResult,
    DocumentProcessingResult,
    SectionProcessingResult,
    BatchWordSummary,
    BatchWordProcessingMetadata,
    BatchWordStatsResult,
    DocumentAnalysisResult,
    DocumentUploadInfo,
    SectionPriority
)
from app.api.models.common import ProcessingMethod

class BatchWordService:
    """Service for handling Batch Word document processing operations"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self._processor: Optional[Any] = None
        self._mock_mode = True  # Use mock mode until we integrate the actual system
        self._upload_dir = Path(tempfile.gettempdir()) / "batch_word_uploads"
        self._upload_dir.mkdir(exist_ok=True)
        self._stats = {
            'total_documents': 0,
            'total_paragraphs': 0,
            'total_changes': 0,
            'processing_times': [],
            'section_distribution': {'high': 0, 'medium': 0, 'low': 0},
            'success_rate': 0.0
        }
        self._initialize_processor()
    
    def _initialize_processor(self):
        """Initialize the Batch Word processor"""
        try:
            if self._mock_mode:
                # Use mock implementation for now
                print("⚠️  Using mock Batch Word processor - full implementation pending")
                self._processor = None
            else:
                # TODO: Initialize actual BatchWordParaphraser when ready
                pass
                
        except Exception as e:
            raise ProcessingError(f"Failed to initialize Batch Word processor: {e}")
    
    @property
    def processor(self):
        """Get processor instance"""
        return self._processor
    
    def _get_default_priority_sections(self) -> Dict[str, List[str]]:
        """Get default priority sections mapping"""
        return {
            'high': [
                'latar belakang', 'landasan teori', 'tinjauan pustaka', 
                'kajian teori', 'teori', 'konsep'
            ],
            'medium': [
                'metodologi', 'metode penelitian', 'penelitian terkait',
                'rumusan masalah', 'tujuan penelitian'
            ],
            'low': [
                'manfaat penelitian', 'sistematika penulisan',
                'batasan masalah', 'definisi operasional'
            ]
        }
    
    def _analyze_uploaded_document(self, file_path: str) -> DocumentAnalysisResult:
        """Analyze an uploaded document to determine processing characteristics"""
        try:
            filename = os.path.basename(file_path)
            
            # Mock analysis - in real implementation, this would use python-docx
            import random
            
            # Simulate document analysis
            total_paragraphs = random.randint(50, 200)
            
            # Mock section detection
            detected_sections = []
            bab_sections = ['BAB I', 'BAB II', 'BAB III']
            content_sections = [
                'latar belakang', 'landasan teori', 'metodologi penelitian',
                'tinjauan pustaka', 'rumusan masalah', 'tujuan penelitian'
            ]
            
            # Simulate finding sections
            for section in bab_sections:
                if random.random() > 0.3:  # 70% chance of finding each BAB
                    detected_sections.append(section)
            
            for section in content_sections:
                if random.random() > 0.5:  # 50% chance of finding each content section
                    detected_sections.append(section)
            
            # Paragraph distribution by section
            paragraph_lengths = {}
            for section in detected_sections:
                paragraph_lengths[section] = random.randint(5, 25)
            
            # Priority grouping
            priority_sections = self._get_default_priority_sections()
            
            # Calculate suitability score
            suitability_score = min(100, (len(detected_sections) * 10) + (total_paragraphs / 2))
            
            # Recommended aggressiveness based on document characteristics
            if 'BAB II' in detected_sections or 'landasan teori' in detected_sections:
                recommended_aggressiveness = 0.6  # Higher for theory sections
            elif 'metodologi' in detected_sections:
                recommended_aggressiveness = 0.4  # Lower for methodology
            else:
                recommended_aggressiveness = 0.5  # Default
            
            # Estimated processing time
            estimated_time = max(1, total_paragraphs // 20)  # ~20 paragraphs per minute
            
            return DocumentAnalysisResult(
                filename=filename,
                total_paragraphs=total_paragraphs,
                sections_detected=detected_sections,
                paragraph_lengths=paragraph_lengths,
                priority_sections=priority_sections,
                recommended_aggressiveness=recommended_aggressiveness,
                estimated_processing_time=estimated_time,
                suitability_score=round(suitability_score, 1)
            )
            
        except Exception as e:
            raise ProcessingError(f"Failed to analyze document {file_path}: {e}")
    
    def _mock_process_document(
        self, 
        file_path: str, 
        request: ProcessDocumentsRequest
    ) -> DocumentProcessingResult:
        """Mock document processing"""
        import random
        
        start_time = time.time()
        filename = os.path.basename(file_path)
        
        # Simulate document processing
        total_paragraphs = random.randint(50, 150)
        processed_paragraphs = int(total_paragraphs * random.uniform(0.6, 0.9))
        total_changes = random.randint(processed_paragraphs * 2, processed_paragraphs * 8)
        
        # Create backup path
        backup_path = None
        if request.create_backup:
            backup_dir = Path(file_path).parent / "backups"
            backup_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = str(backup_dir / f"{Path(filename).stem}_backup_{timestamp}.docx")
        
        # Simulate section processing
        sections_processed = []
        priority_sections = self._get_default_priority_sections()
        
        for priority, section_list in priority_sections.items():
            for section in section_list[:random.randint(1, len(section_list))]:
                section_paragraphs = random.randint(5, 20)
                section_processed = int(section_paragraphs * random.uniform(0.5, 0.9))
                section_changes = random.randint(section_processed, section_processed * 3)
                
                section_result = SectionProcessingResult(
                    section_name=section,
                    priority_level=SectionPriority(priority),
                    paragraphs_found=section_paragraphs,
                    paragraphs_processed=section_processed,
                    total_changes=section_changes,
                    average_improvement=round(random.uniform(25, 65), 1),
                    processing_time_ms=random.randint(5000, 20000)
                )
                sections_processed.append(section_result)
        
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        # Create metadata
        metadata = BatchWordProcessingMetadata(
            method=ProcessingMethod.LOCAL_ONLY,  # Batch Word is primarily local
            similarity=round(100 - random.uniform(30, 60), 2),  # Simulate improvement
            plagiarism_reduction=round(random.uniform(30, 60), 2),
            quality_score=round(random.uniform(80, 95), 1),
            changes_made=total_changes,
            processing_time_ms=processing_time_ms,
            api_calls_used=0,  # Local processing
            cost_estimate=0.0,  # Free local processing
            sections_analyzed=len(sections_processed),
            high_priority_sections=len([s for s in sections_processed if s.priority_level == SectionPriority.HIGH]),
            medium_priority_sections=len([s for s in sections_processed if s.priority_level == SectionPriority.MEDIUM]),
            low_priority_sections=len([s for s in sections_processed if s.priority_level == SectionPriority.LOW]),
            documents_backed_up=1 if request.create_backup else 0,
            average_aggressiveness_used=request.aggressiveness,
            formatting_preserved=True,  # Always preserve formatting
            highlight_applied=request.highlight_changes
        )
        
        # Processed file path (in real implementation, this would be the modified document)
        processed_path = file_path  # In-place modification
        
        return DocumentProcessingResult(
            filename=filename,
            original_file_path=file_path,
            processed_file_path=processed_path,
            backup_file_path=backup_path,
            total_paragraphs=total_paragraphs,
            processed_paragraphs=processed_paragraphs,
            total_changes=total_changes,
            sections_processed=sections_processed,
            processing_metadata=metadata,
            success=True,
            error_message=None
        )
    
    async def save_uploaded_files(self, files: List[BinaryIO]) -> List[DocumentUploadInfo]:
        """Save uploaded files and return upload information"""
        upload_infos = []
        
        for file in files:
            try:
                # Generate unique filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_filename = f"{timestamp}_{file.filename}"
                upload_path = self._upload_dir / safe_filename
                
                # Save file
                with open(upload_path, "wb") as f:
                    shutil.copyfileobj(file, f)
                
                # Get file size
                file_size = upload_path.stat().st_size
                
                # Analyze document
                analysis = self._analyze_uploaded_document(str(upload_path))
                
                upload_info = DocumentUploadInfo(
                    filename=file.filename,
                    size=file_size,
                    content_type=file.content_type or "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    upload_path=str(upload_path),
                    paragraphs_detected=analysis.total_paragraphs,
                    sections_detected=analysis.sections_detected,
                    estimated_processing_time=analysis.estimated_processing_time
                )
                
                upload_infos.append(upload_info)
                
            except Exception as e:
                raise ProcessingError(f"Failed to save uploaded file {file.filename}: {e}")
        
        return upload_infos
    
    async def process_documents(
        self, 
        request: ProcessDocumentsRequest,
        file_paths: List[str]
    ) -> BatchProcessingResult:
        """Process multiple Word documents"""
        if not file_paths:
            raise ProcessingError("No documents provided for processing")
        
        try:
            start_time = time.time()
            
            # Create backup folder if requested
            backup_folder = None
            if request.create_backup:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_folder = str(self._upload_dir / f"backup_{timestamp}")
                Path(backup_folder).mkdir(exist_ok=True)
            
            processed_documents = []
            successful = 0
            failed = 0
            total_paragraphs = 0
            paraphrased_paragraphs = 0
            total_changes = 0
            errors = []
            section_priority_distribution = {'high': 0, 'medium': 0, 'low': 0}
            
            for file_path in file_paths:
                try:
                    # Process document
                    result = self._mock_process_document(file_path, request)
                    processed_documents.append(result)
                    
                    # Update statistics
                    successful += 1
                    total_paragraphs += result.total_paragraphs
                    paraphrased_paragraphs += result.processed_paragraphs
                    total_changes += result.total_changes
                    
                    # Section priority distribution
                    for section in result.sections_processed:
                        section_priority_distribution[section.priority_level.value] += 1
                    
                except Exception as e:
                    failed += 1
                    error_msg = f"Error processing {os.path.basename(file_path)}: {str(e)}"
                    errors.append(error_msg)
                    
                    # Create error result
                    error_result = DocumentProcessingResult(
                        filename=os.path.basename(file_path),
                        original_file_path=file_path,
                        processed_file_path=file_path,
                        backup_file_path=None,
                        total_paragraphs=0,
                        processed_paragraphs=0,
                        total_changes=0,
                        sections_processed=[],
                        processing_metadata=BatchWordProcessingMetadata(
                            method=ProcessingMethod.LOCAL_ONLY,
                            similarity=100.0,
                            plagiarism_reduction=0.0,
                            quality_score=0.0,
                            changes_made=0,
                            processing_time_ms=0,
                            api_calls_used=0,
                            cost_estimate=0.0,
                            sections_analyzed=0,
                            high_priority_sections=0,
                            medium_priority_sections=0,
                            low_priority_sections=0,
                            documents_backed_up=0,
                            average_aggressiveness_used=0.0,
                            formatting_preserved=False,
                            highlight_applied=False
                        ),
                        success=False,
                        error_message=str(e)
                    )
                    processed_documents.append(error_result)
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Calculate success rate and average improvement
            success_rate = (successful / len(file_paths)) * 100 if file_paths else 0
            average_improvement = (
                sum(doc.processing_metadata.plagiarism_reduction for doc in processed_documents if doc.success) /
                successful if successful > 0 else 0
            )
            
            # Create summary
            summary = BatchWordSummary(
                total_documents=len(file_paths),
                successful_documents=successful,
                failed_documents=failed,
                total_paragraphs=total_paragraphs,
                paraphrased_paragraphs=paraphrased_paragraphs,
                total_changes_made=total_changes,
                processing_time_seconds=processing_time,
                success_rate_percentage=round(success_rate, 1),
                average_improvement=round(average_improvement, 1),
                section_priority_distribution=section_priority_distribution,
                errors=errors
            )
            
            # Generate report file
            report_file = None
            if processed_documents:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                report_file = str(self._upload_dir / f"batch_processing_report_{timestamp}.json")
                
                report_data = {
                    'timestamp': timestamp,
                    'summary': summary.dict(),
                    'documents': [doc.dict() for doc in processed_documents]
                }
                
                with open(report_file, 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
            
            # Update service statistics
            self._stats['total_documents'] += len(file_paths)
            self._stats['total_paragraphs'] += total_paragraphs
            self._stats['total_changes'] += total_changes
            self._stats['processing_times'].append(processing_time)
            self._stats['success_rate'] = success_rate
            
            return BatchProcessingResult(
                input_folder=str(self._upload_dir),
                backup_folder=backup_folder,
                processed_documents=processed_documents,
                summary=summary,
                report_file=report_file
            )
            
        except Exception as e:
            raise ParaphrasingFailedError(f"Batch document processing failed: {str(e)}")
    
    async def process_bab_sections(
        self, 
        request: BabSectionsRequest,
        file_paths: List[str]
    ) -> BabSectionsProcessingResult:
        """Process specific BAB (chapter) sections"""
        if not file_paths:
            raise ProcessingError("No documents provided for BAB sections processing")
        
        try:
            # Convert to document processing request
            base_aggressiveness = 0.5
            if request.aggressiveness_by_section:
                # Use average of specified aggressiveness levels
                base_aggressiveness = sum(request.aggressiveness_by_section.values()) / len(request.aggressiveness_by_section)
            
            doc_request = ProcessDocumentsRequest(
                aggressiveness=base_aggressiveness,
                create_backup=request.create_backup,
                min_paragraph_length=25,  # Slightly lower for BAB sections
                improvement_threshold=15.0,  # Lower threshold for academic content
                highlight_changes=True,
                priority_sections=None  # Use defaults for BAB processing
            )
            
            # Process documents
            batch_result = await self.process_documents(doc_request, file_paths)
            
            # Analyze BAB-specific results
            sections_found = set()
            sections_processed = set()
            bab_analysis = {
                'bab_distribution': {'bab_1': 0, 'bab_2': 0, 'bab_3': 0},
                'focus_area_coverage': {},
                'section_effectiveness': {}
            }
            
            for doc in batch_result.processed_documents:
                if doc.success:
                    for section in doc.sections_processed:
                        sections_found.add(section.section_name)
                        if section.paragraphs_processed > 0:
                            sections_processed.add(section.section_name)
                        
                        # Analyze BAB distribution
                        section_name_lower = section.section_name.lower()
                        if 'bab' in section_name_lower:
                            if 'i' in section_name_lower and 'ii' not in section_name_lower:
                                bab_analysis['bab_distribution']['bab_1'] += 1
                            elif 'ii' in section_name_lower and 'iii' not in section_name_lower:
                                bab_analysis['bab_distribution']['bab_2'] += 1
                            elif 'iii' in section_name_lower:
                                bab_analysis['bab_distribution']['bab_3'] += 1
                        
                        # Focus area coverage
                        for focus_area in request.focus_areas:
                            if focus_area.lower() in section_name_lower:
                                if focus_area not in bab_analysis['focus_area_coverage']:
                                    bab_analysis['focus_area_coverage'][focus_area] = 0
                                bab_analysis['focus_area_coverage'][focus_area] += 1
                        
                        # Section effectiveness
                        bab_analysis['section_effectiveness'][section.section_name] = section.average_improvement
            
            return BabSectionsProcessingResult(
                sections_requested=request.sections_to_process,
                sections_found=list(sections_found),
                sections_processed=list(sections_processed),
                documents_processed=batch_result.processed_documents,
                bab_analysis=bab_analysis,
                summary=batch_result.summary
            )
            
        except Exception as e:
            raise ParaphrasingFailedError(f"BAB sections processing failed: {str(e)}")
    
    async def analyze_documents(self, file_paths: List[str]) -> List[DocumentAnalysisResult]:
        """Analyze documents before processing"""
        if not file_paths:
            raise ProcessingError("No documents provided for analysis")
        
        try:
            analyses = []
            for file_path in file_paths:
                analysis = self._analyze_uploaded_document(file_path)
                analyses.append(analysis)
            
            return analyses
            
        except Exception as e:
            raise ProcessingError(f"Document analysis failed: {str(e)}")
    
    async def get_processing_stats(self) -> BatchWordStatsResult:
        """Get batch word processing statistics"""
        avg_processing_time = (
            sum(self._stats['processing_times']) / len(self._stats['processing_times'])
            if self._stats['processing_times'] else 0.0
        )
        
        return BatchWordStatsResult(
            total_documents_processed=self._stats['total_documents'],
            total_paragraphs_processed=self._stats['total_paragraphs'],
            total_changes_made=self._stats['total_changes'],
            average_processing_time_per_document=round(avg_processing_time, 2),
            success_rate=round(self._stats['success_rate'], 1),
            most_common_section_types=[
                'latar belakang', 'landasan teori', 'metodologi penelitian'
            ],  # Mock data
            aggressiveness_level_usage={
                '0.3-0.4': 20, '0.4-0.5': 35, '0.5-0.6': 30, '0.6-0.7': 15
            },  # Mock data
            priority_section_effectiveness={
                'high': 65.2, 'medium': 52.8, 'low': 38.5
            },  # Mock data
            backup_creation_rate=95.0,  # Mock data
            average_improvement_by_section={
                'latar belakang': 58.3,
                'landasan teori': 62.1,
                'metodologi penelitian': 45.7,
                'tinjauan pustaka': 59.8
            }  # Mock data
        )
    
    async def get_service_info(self) -> dict:
        """Get Batch Word service information"""
        return {
            "service_type": "batch_word",
            "processor_available": self._processor is not None,
            "mock_mode": self._mock_mode,
            "upload_directory": str(self._upload_dir),
            "supported_formats": ["docx"],
            "features": [
                "direct_file_modification",
                "backup_creation",
                "section_priority_processing",
                "batch_processing",
                "academic_focus",
                "bab_specific_processing",
                "formatting_preservation"
            ],
            "academic_sections": {
                "high_priority": [
                    "latar belakang", "landasan teori", "tinjauan pustaka", 
                    "kajian teori", "teori", "konsep"
                ],
                "medium_priority": [
                    "metodologi", "metode penelitian", "penelitian terkait",
                    "rumusan masalah", "tujuan penelitian"
                ],
                "low_priority": [
                    "manfaat penelitian", "sistematika penulisan",
                    "batasan masalah", "definisi operasional"
                ]
            },
            "processing_capabilities": {
                "min_paragraph_length": "10-100 words (configurable)",
                "improvement_threshold": "0-100% (configurable)",
                "aggressiveness_levels": "0.1-1.0 (configurable by section)",
                "backup_support": True,
                "highlight_changes": True,
                "preserve_formatting": True
            },
            "settings": {
                "max_file_size": "50MB per document",
                "max_batch_size": "20 documents per batch",
                "supported_sections": [
                    "bab_1", "bab_2", "bab_3", "bab_4", "bab_5",
                    "pendahuluan", "tinjauan_pustaka", "metodologi",
                    "hasil", "pembahasan", "kesimpulan"
                ]
            }
        }
    
    def cleanup_upload_directory(self, older_than_hours: int = 24):
        """Clean up old uploaded files"""
        try:
            current_time = time.time()
            cutoff_time = current_time - (older_than_hours * 3600)
            
            for file_path in self._upload_dir.iterdir():
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
            
        except Exception as e:
            print(f"Warning: Failed to cleanup upload directory: {e}")