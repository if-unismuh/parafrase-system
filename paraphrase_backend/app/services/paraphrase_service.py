"""
Paraphrasing service
Business logic for text paraphrasing operations
"""
import time
from typing import List, Optional
from pathlib import Path
import sys
import os

# Add the parent directory to sys.path to import SmartEfficientParaphraser
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from smart_efficient_paraphraser import SmartEfficientParaphraser
from app.core.config import Settings
from app.core.exceptions import (
    ParaphrasingFailedError,
    TextTooLongError,
    TextTooShortError,
    ProcessingError
)
from app.api.models.paraphrase import (
    ParaphraseRequest,
    ParaphraseResult,
    BatchParaphraseRequest,
    BatchParaphraseResult,
    BatchSummary
)
from app.api.models.common import ProcessingMetadata, ProcessingMethod

class ParaphraseService:
    """Service for handling paraphrasing operations"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self._paraphraser: Optional[SmartEfficientParaphraser] = None
        self._initialize_paraphraser()
    
    def _initialize_paraphraser(self):
        """Initialize the paraphraser instance"""
        try:
            # Look for synonym file in the parent directory
            synonym_file_paths = [
                Path(__file__).parent.parent.parent.parent / "sinonim.json",
                Path("sinonim.json"),
                Path("components/sinonim.json")
            ]
            
            synonym_file = None
            for path in synonym_file_paths:
                if path.exists():
                    synonym_file = str(path)
                    break
            
            if not synonym_file:
                print("⚠️  Warning: sinonim.json not found, using empty synonym database")
                synonym_file = None
            
            self._paraphraser = SmartEfficientParaphraser(
                synonym_file=synonym_file,
                gemini_api_key=self.settings.gemini_api_key
            )
            
            # Update search configuration
            if hasattr(self._paraphraser, 'search_config'):
                self._paraphraser.search_config.update({
                    'max_results': self.settings.ddgs_max_results,
                    'region': self.settings.ddgs_region,
                    'language': self.settings.ddgs_language,
                    'safesearch': self.settings.ddgs_safe_search
                })
            
        except Exception as e:
            raise ProcessingError(f"Failed to initialize paraphraser: {e}")
    
    @property
    def paraphraser(self) -> SmartEfficientParaphraser:
        """Get paraphraser instance, initialize if needed"""
        if self._paraphraser is None:
            self._initialize_paraphraser()
        return self._paraphraser
    
    def _validate_text_length(self, text: str) -> None:
        """Validate text length against settings"""
        text_length = len(text)
        
        if text_length < self.settings.min_text_length:
            raise TextTooShortError(text_length, self.settings.min_text_length)
        
        if text_length > self.settings.max_text_length:
            raise TextTooLongError(text_length, self.settings.max_text_length)
    
    def _convert_processing_method(self, method_str: str) -> ProcessingMethod:
        """Convert string method to ProcessingMethod enum"""
        method_mapping = {
            'local_only': ProcessingMethod.LOCAL_ONLY,
            'local_with_search_context': ProcessingMethod.LOCAL_WITH_SEARCH,
            'local_plus_ai_refinement': ProcessingMethod.LOCAL_PLUS_AI,
            'local_plus_ai_refinement_with_search': ProcessingMethod.LOCAL_SEARCH_AI,
            'protected_content': ProcessingMethod.PROTECTED_CONTENT
        }
        return method_mapping.get(method_str, ProcessingMethod.LOCAL_ONLY)
    
    def _create_processing_metadata(self, result: dict, processing_time_ms: int) -> ProcessingMetadata:
        """Create ProcessingMetadata from paraphraser result"""
        return ProcessingMetadata(
            method=self._convert_processing_method(result.get('method', 'local_only')),
            similarity=result.get('similarity', 0.0),
            plagiarism_reduction=result.get('plagiarism_reduction', 0.0),
            quality_score=result.get('quality_score'),
            changes_made=result.get('changes_made', 0),
            processing_time_ms=processing_time_ms,
            search_context=result.get('search_context'),
            api_calls_used=result.get('api_calls_used', 0),
            cost_estimate=self._estimate_cost(result)
        )
    
    def _estimate_cost(self, result: dict) -> Optional[float]:
        """Estimate cost based on API usage"""
        # Simple cost estimation (you can make this more sophisticated)
        api_calls = result.get('api_calls_used', 0)
        if api_calls > 0:
            # Estimate based on Gemini pricing (very rough estimate)
            return api_calls * 0.001  # $0.001 per API call
        return None
    
    async def paraphrase_text(self, request: ParaphraseRequest) -> ParaphraseResult:
        """Paraphrase a single text"""
        # Validate input
        self._validate_text_length(request.text)
        
        try:
            start_time = time.time()
            
            # Perform paraphrasing
            result = self.paraphraser.paraphrase_text(
                text=request.text,
                use_search=request.use_search and self.settings.ddgs_enabled
            )
            
            processing_time_ms = int((time.time() - start_time) * 1000)
            
            # Create metadata
            metadata = self._create_processing_metadata(result, processing_time_ms)
            
            return ParaphraseResult(
                paraphrased_text=result['paraphrase'],
                original_text=result['original'],
                metadata=metadata
            )
            
        except Exception as e:
            if isinstance(e, (TextTooLongError, TextTooShortError)):
                raise
            raise ParaphrasingFailedError(str(e))
    
    async def paraphrase_batch(self, request: BatchParaphraseRequest) -> BatchParaphraseResult:
        """Paraphrase multiple texts"""
        # Validate batch size
        if len(request.texts) > self.settings.max_batch_size:
            raise ProcessingError(
                f"Batch size ({len(request.texts)}) exceeds maximum allowed ({self.settings.max_batch_size})"
            )
        
        results: List[ParaphraseResult] = []
        total_processing_time = 0
        successful = 0
        failed = 0
        total_api_calls = 0
        total_cost = 0.0
        similarity_reductions = []
        
        for i, text in enumerate(request.texts):
            try:
                # Create individual request
                individual_request = ParaphraseRequest(
                    text=text,
                    use_search=request.use_search,
                    quality_level=request.quality_level,
                    language=request.language,
                    preserve_formatting=request.preserve_formatting
                )
                
                # Process text
                result = await self.paraphrase_text(individual_request)
                results.append(result)
                
                # Update statistics
                successful += 1
                total_processing_time += result.metadata.processing_time_ms
                total_api_calls += result.metadata.api_calls_used
                if result.metadata.cost_estimate:
                    total_cost += result.metadata.cost_estimate
                similarity_reductions.append(result.metadata.plagiarism_reduction)
                
            except Exception as e:
                failed += 1
                # Create error result
                error_result = ParaphraseResult(
                    paraphrased_text=f"[ERROR: {str(e)}]",
                    original_text=text,
                    metadata=ProcessingMetadata(
                        method=ProcessingMethod.LOCAL_ONLY,
                        similarity=100.0,  # No change due to error
                        plagiarism_reduction=0.0,
                        changes_made=0,
                        processing_time_ms=0,
                        api_calls_used=0
                    )
                )
                results.append(error_result)
        
        # Calculate summary
        avg_similarity_reduction = (
            sum(similarity_reductions) / len(similarity_reductions) 
            if similarity_reductions else 0.0
        )
        
        summary = BatchSummary(
            total_texts=len(request.texts),
            successful=successful,
            failed=failed,
            total_processing_time_ms=total_processing_time,
            average_similarity_reduction=avg_similarity_reduction,
            total_api_calls=total_api_calls,
            estimated_total_cost=total_cost if total_cost > 0 else None
        )
        
        return BatchParaphraseResult(
            results=results,
            summary=summary
        )
    
    async def get_service_stats(self) -> dict:
        """Get service statistics"""
        return {
            "paraphraser_available": self._paraphraser is not None,
            "ddgs_enabled": self.settings.ddgs_enabled,
            "ai_service_configured": bool(self.settings.gemini_api_key),
            "synonym_database_loaded": (
                hasattr(self.paraphraser, 'synonyms') and 
                bool(self.paraphraser.synonyms)
            ),
            "settings": {
                "max_text_length": self.settings.max_text_length,
                "min_text_length": self.settings.min_text_length,
                "max_batch_size": self.settings.max_batch_size,
                "ddgs_region": self.settings.ddgs_region,
                "ddgs_language": self.settings.ddgs_language
            }
        }