"""
Ultimate Hybrid Paraphrasing service
Business logic for Ultimate Hybrid paraphrasing operations
"""
import time
from typing import List, Optional, Dict, Any
from pathlib import Path
import sys

# Add the parent directory to sys.path to import UltimateHybridParaphraser
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from ultimate_hybrid_paraphraser import UltimateHybridParaphraser
from app.core.config import Settings
from app.core.exceptions import (
    ParaphrasingFailedError,
    TextTooLongError,
    TextTooShortError,
    ProcessingError,
    AIServiceError
)
from app.api.models.ultimate_hybrid import (
    UltimateHybridRequest,
    UltimateHybridResult,
    BatchUltimateHybridRequest,
    BatchUltimateHybridResult,
    UltimateHybridBatchSummary,
    UltimateHybridProcessingMetadata,
    TextCharacteristics,
    ProcessingMode,
    MultiOptionRequest,
    MultiOptionResult,
    ProcessingStatsResult
)
from app.api.models.common import ProcessingMethod

class UltimateHybridService:
    """Service for handling Ultimate Hybrid paraphrasing operations"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self._paraphraser: Optional[UltimateHybridParaphraser] = None
        self._initialize_paraphraser()
    
    def _initialize_paraphraser(self):
        """Initialize the Ultimate Hybrid paraphraser instance"""
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
            
            # Initialize with smart mode as default
            self._paraphraser = UltimateHybridParaphraser(
                synonym_file=synonym_file,
                gemini_api_key=self.settings.gemini_api_key,
                mode='smart'
            )
            
        except Exception as e:
            raise ProcessingError(f"Failed to initialize Ultimate Hybrid paraphraser: {e}")
    
    @property
    def paraphraser(self) -> UltimateHybridParaphraser:
        """Get paraphraser instance, initialize if needed"""
        if self._paraphraser is None:
            self._initialize_paraphraser()
        return self._paraphraser
    
    def _validate_text_length(self, text: str) -> None:
        """Validate text length against settings"""
        text_length = len(text)
        
        if text_length < self.settings.min_text_length:
            raise TextTooShortError(text_length, self.settings.min_text_length)
        
        if text_length > 15000:  # Ultimate Hybrid supports longer texts
            raise TextTooLongError(text_length, 15000)
    
    def _convert_mode(self, mode: ProcessingMode) -> str:
        """Convert ProcessingMode enum to string for the paraphraser"""
        mode_mapping = {
            ProcessingMode.SMART: "smart",
            ProcessingMode.BALANCED: "balanced",
            ProcessingMode.AGGRESSIVE: "aggressive",
            ProcessingMode.TURNITIN_SAFE: "turnitin_safe"
        }
        return mode_mapping.get(mode, "smart")
    
    def _extract_text_characteristics(self, text: str, characteristics_data: dict) -> TextCharacteristics:
        """Extract text characteristics from paraphraser analysis"""
        return TextCharacteristics(
            length=characteristics_data.get('length', 0),
            sentence_count=characteristics_data.get('sentence_count', 0),
            avg_sentence_length=characteristics_data.get('avg_sentence_length', 0.0),
            complexity_score=characteristics_data.get('complexity_score', 0.0),
            is_academic=characteristics_data.get('is_academic', False),
            academic_indicators=characteristics_data.get('academic_indicators', 0),
            citation_count=characteristics_data.get('citation_count', 0),
            technical_patterns=characteristics_data.get('technical_patterns', 0),
            turnitin_risk_patterns=characteristics_data.get('turnitin_risk_patterns', 0),
            recommended_mode=ProcessingMode(characteristics_data.get('recommended_mode', 'smart')),
            recommended_aggressiveness=characteristics_data.get('recommended_aggressiveness', 0.5)
        )
    
    def _create_processing_metadata(
        self, 
        result: dict, 
        processing_time_ms: int,
        request: UltimateHybridRequest,
        text_characteristics: dict
    ) -> UltimateHybridProcessingMetadata:
        """Create UltimateHybridProcessingMetadata from paraphraser result"""
        
        # Determine processing method based on result
        method = ProcessingMethod.LOCAL_ONLY
        if 'ai' in result.get('method', '').lower():
            if 'local' in result.get('method', '').lower():
                method = ProcessingMethod.LOCAL_PLUS_AI
            else:
                method = ProcessingMethod.AI_ONLY
        
        return UltimateHybridProcessingMetadata(
            method=method,
            similarity=result.get('similarity', 0.0),
            plagiarism_reduction=result.get('plagiarism_reduction', 0.0),
            quality_score=self._calculate_quality_score(result),
            changes_made=result.get('changes_made', 0),
            processing_time_ms=processing_time_ms,
            search_context=None,  # Ultimate Hybrid doesn't use search context directly
            api_calls_used=1 if 'ai' in result.get('method', '').lower() else 0,
            cost_estimate=self._estimate_cost(result),
            processing_mode=result.get('method', request.mode.value),
            routing_decision=result.get('routing_reason', 'Default processing'),
            ai_model_used=result.get('ai_model_used', 'gemini-1.5-flash' if 'ai' in result.get('method', '').lower() else None),
            cache_hit=result.get('method', '').endswith('_cached'),
            turnitin_risk_detected=text_characteristics.get('turnitin_risk_patterns', 0),
            complexity_score=text_characteristics.get('complexity_score', 0.0),
            academic_content=text_characteristics.get('is_academic', False),
            aggressiveness_used=request.aggressiveness,
            local_vs_ai_comparison=result.get('comparison_data')
        )
    
    def _calculate_quality_score(self, result: dict) -> float:
        """Calculate quality score based on result metrics"""
        plagiarism_reduction = result.get('plagiarism_reduction', 0)
        changes_made = result.get('changes_made', 0)
        
        # Base score from plagiarism reduction
        quality_score = min(plagiarism_reduction * 1.5, 100)
        
        # Bonus for meaningful changes
        if changes_made > 0:
            quality_score = min(quality_score + (changes_made * 2), 100)
        
        # Method bonus
        method = result.get('method', '')
        if 'ai' in method.lower():
            quality_score = min(quality_score + 10, 100)
        
        return round(quality_score, 1)
    
    def _estimate_cost(self, result: dict) -> Optional[float]:
        """Estimate cost based on processing method"""
        method = result.get('method', '')
        
        if 'ai' in method.lower() and not method.endswith('_cached'):
            # Rough Gemini pricing estimate
            text_length = result.get('original_length', 100)
            paraphrase_length = result.get('paraphrase_length', 100)
            
            # Estimate tokens (rough approximation)
            total_tokens = (text_length + paraphrase_length) * 2
            
            # Gemini Flash pricing
            input_cost_per_1k = 0.00015
            output_cost_per_1k = 0.0006
            
            estimated_cost = ((total_tokens / 1000) * input_cost_per_1k) + \
                           ((total_tokens / 1000) * output_cost_per_1k)
            
            return round(estimated_cost, 6)
        
        return 0.0  # Local processing is free
    
    async def paraphrase_text(self, request: UltimateHybridRequest) -> UltimateHybridResult:
        """Paraphrase a single text using Ultimate Hybrid system"""
        # Validate input
        self._validate_text_length(request.text)
        
        try:
            start_time = time.time()
            
            # Switch to requested mode
            mode_string = self._convert_mode(request.mode)
            if self.paraphraser.mode != mode_string:
                self.paraphraser.switch_mode(mode_string)
            
            # Analyze text characteristics
            characteristics = self.paraphraser.analyze_text_characteristics(request.text)
            
            # Process the text
            result = self.paraphraser.process_paragraph_ultimate(
                request.text,
                aggressiveness=request.aggressiveness
            )
            
            processing_time_ms = int((time.time() - start_time) * 1000)
            
            # Create metadata
            metadata = self._create_processing_metadata(result, processing_time_ms, request, characteristics)
            
            # Extract text characteristics
            text_chars = self._extract_text_characteristics(request.text, characteristics)
            
            return UltimateHybridResult(
                paraphrased_text=result.get('paraphrase', request.text),
                original_text=result.get('original', request.text),
                metadata=metadata,
                text_characteristics=text_chars,
                alternative_options=[]  # Can be populated later if needed
            )
            
        except Exception as e:
            if isinstance(e, (TextTooLongError, TextTooShortError)):
                raise
            raise ParaphrasingFailedError(f"Ultimate Hybrid processing failed: {str(e)}")
    
    async def paraphrase_batch(self, request: BatchUltimateHybridRequest) -> BatchUltimateHybridResult:
        """Paraphrase multiple texts using Ultimate Hybrid system"""
        # Validate batch size
        max_batch_size = min(self.settings.max_batch_size, 100)
        if len(request.texts) > max_batch_size:
            raise ProcessingError(
                f"Batch size ({len(request.texts)}) exceeds maximum allowed ({max_batch_size})"
            )
        
        results: List[UltimateHybridResult] = []
        total_processing_time = 0
        successful = 0
        failed = 0
        mode_distribution = {}
        ai_calls = 0
        total_cost = 0.0
        similarity_reductions = []
        quality_scores = []
        turnitin_detections = 0
        complexity_distribution = {"low": 0, "medium": 0, "high": 0}
        cache_hits = 0
        
        # Switch to requested mode
        mode_string = self._convert_mode(request.mode)
        if self.paraphraser.mode != mode_string:
            self.paraphraser.switch_mode(mode_string)
        
        for i, text in enumerate(request.texts):
            try:
                # Create individual request
                individual_request = UltimateHybridRequest(
                    text=text,
                    mode=request.mode,
                    aggressiveness=request.aggressiveness,
                    enable_turnitin_detection=request.enable_turnitin_detection,
                    cost_optimization=request.cost_optimization,
                    cache_enabled=request.cache_enabled
                )
                
                # Process text
                result = await self.paraphrase_text(individual_request)
                results.append(result)
                
                # Update statistics
                successful += 1
                total_processing_time += result.metadata.processing_time_ms
                ai_calls += result.metadata.api_calls_used
                if result.metadata.cost_estimate:
                    total_cost += result.metadata.cost_estimate
                similarity_reductions.append(result.metadata.plagiarism_reduction)
                quality_scores.append(result.metadata.quality_score)
                turnitin_detections += result.metadata.turnitin_risk_detected or 0
                
                # Mode distribution
                processing_mode = result.metadata.processing_mode
                mode_distribution[processing_mode] = mode_distribution.get(processing_mode, 0) + 1
                
                # Complexity distribution
                complexity = result.text_characteristics.complexity_score
                if complexity < 0.33:
                    complexity_distribution["low"] += 1
                elif complexity < 0.66:
                    complexity_distribution["medium"] += 1
                else:
                    complexity_distribution["high"] += 1
                
                # Cache hits
                if result.metadata.cache_hit:
                    cache_hits += 1
                
            except Exception as e:
                failed += 1
                # Create error result
                error_result = UltimateHybridResult(
                    paraphrased_text=f"[ERROR: {str(e)}]",
                    original_text=text,
                    metadata=UltimateHybridProcessingMetadata(
                        method=ProcessingMethod.LOCAL_ONLY,
                        similarity=100.0,  # No change due to error
                        plagiarism_reduction=0.0,
                        quality_score=0.0,
                        changes_made=0,
                        processing_time_ms=0,
                        api_calls_used=0,
                        processing_mode="error",
                        routing_decision="Processing failed",
                        complexity_score=0.0,
                        academic_content=False,
                        aggressiveness_used=request.aggressiveness
                    ),
                    text_characteristics=TextCharacteristics(
                        length=len(text.split()),
                        sentence_count=0,
                        avg_sentence_length=0.0,
                        complexity_score=0.0,
                        is_academic=False,
                        academic_indicators=0,
                        citation_count=0,
                        technical_patterns=0,
                        turnitin_risk_patterns=0,
                        recommended_mode=ProcessingMode.SMART,
                        recommended_aggressiveness=0.5
                    ),
                    alternative_options=[]
                )
                results.append(error_result)
        
        # Calculate summary
        avg_similarity_reduction = (
            sum(similarity_reductions) / len(similarity_reductions) 
            if similarity_reductions else 0.0
        )
        
        avg_quality_score = (
            sum(quality_scores) / len(quality_scores)
            if quality_scores else 0.0
        )
        
        ai_usage_ratio = ai_calls / len(request.texts) if request.texts else 0.0
        cache_hit_ratio = cache_hits / len(request.texts) if request.texts else 0.0
        
        summary = UltimateHybridBatchSummary(
            total_texts=len(request.texts),
            successful=successful,
            failed=failed,
            total_processing_time_ms=total_processing_time,
            average_similarity_reduction=avg_similarity_reduction,
            mode_distribution=mode_distribution,
            ai_usage_ratio=ai_usage_ratio,
            cache_hit_ratio=cache_hit_ratio,
            total_ai_calls=ai_calls,
            total_cost_estimate=total_cost if total_cost > 0 else None,
            turnitin_detections=turnitin_detections,
            complexity_distribution=complexity_distribution,
            quality_score_average=avg_quality_score
        )
        
        return BatchUltimateHybridResult(
            results=results,
            summary=summary
        )
    
    async def generate_multiple_options(self, request: MultiOptionRequest) -> MultiOptionResult:
        """Generate multiple paraphrase options using different approaches"""
        # Validate input
        self._validate_text_length(request.text)
        
        try:
            # Determine modes to use
            if request.modes:
                modes_to_use = [self._convert_mode(mode) for mode in request.modes]
            else:
                # Auto-select based on text characteristics
                characteristics = self.paraphraser.analyze_text_characteristics(request.text)
                recommended_mode = characteristics.get('recommended_mode', 'smart')
                
                # Select different modes for variety
                modes_to_use = ['smart', recommended_mode, 'balanced']
                if request.num_options >= 4:
                    modes_to_use.append('aggressive')
                if request.num_options >= 5:
                    modes_to_use.append('turnitin_safe')
            
            # Generate options
            options = self.paraphraser.generate_multiple_options(
                request.text, 
                num_options=request.num_options
            )
            
            # Convert to API models
            api_options = []
            for option in options:
                # Create metadata and characteristics for each option
                metadata = UltimateHybridProcessingMetadata(
                    method=ProcessingMethod.LOCAL_PLUS_AI if 'ai' in option.get('method', '') else ProcessingMethod.LOCAL_ONLY,
                    similarity=option.get('similarity', 0.0),
                    plagiarism_reduction=option.get('plagiarism_reduction', 0.0),
                    quality_score=self._calculate_quality_score(option),
                    changes_made=option.get('changes_made', 0),
                    processing_time_ms=0,  # Not tracked individually
                    api_calls_used=1 if 'ai' in option.get('method', '') else 0,
                    cost_estimate=self._estimate_cost(option),
                    processing_mode=option.get('method', 'unknown'),
                    routing_decision=option.get('routing_reason', 'Option generation'),
                    complexity_score=0.5,  # Default
                    academic_content=True,  # Assume academic for options
                    aggressiveness_used=0.5
                )
                
                characteristics = TextCharacteristics(
                    length=option.get('original_length', 0),
                    sentence_count=1,
                    avg_sentence_length=float(option.get('original_length', 0)),
                    complexity_score=0.5,
                    is_academic=True,
                    academic_indicators=0,
                    citation_count=0,
                    technical_patterns=0,
                    turnitin_risk_patterns=0,
                    recommended_mode=ProcessingMode.SMART,
                    recommended_aggressiveness=0.5
                )
                
                api_result = UltimateHybridResult(
                    paraphrased_text=option.get('paraphrase', ''),
                    original_text=request.text,
                    metadata=metadata,
                    text_characteristics=characteristics,
                    alternative_options=[]
                )
                api_options.append(api_result)
            
            # Create comparison matrix
            comparison_matrix = {
                "similarity_scores": [opt.metadata.similarity for opt in api_options],
                "plagiarism_reductions": [opt.metadata.plagiarism_reduction for opt in api_options],
                "quality_scores": [opt.metadata.quality_score for opt in api_options],
                "processing_methods": [opt.metadata.processing_mode for opt in api_options]
            }
            
            # Determine recommendation
            best_option = max(api_options, key=lambda x: x.metadata.plagiarism_reduction)
            recommendation = {
                "recommended_option": api_options.index(best_option) + 1,
                "reason": f"Highest plagiarism reduction ({best_option.metadata.plagiarism_reduction:.1f}%)",
                "quality_score": best_option.metadata.quality_score,
                "processing_method": best_option.metadata.processing_mode
            }
            
            return MultiOptionResult(
                options=api_options,
                comparison_matrix=comparison_matrix,
                recommendation=recommendation
            )
            
        except Exception as e:
            if isinstance(e, (TextTooLongError, TextTooShortError)):
                raise
            raise ParaphrasingFailedError(f"Multiple options generation failed: {str(e)}")
    
    async def get_processing_stats(self) -> ProcessingStatsResult:
        """Get Ultimate Hybrid service processing statistics"""
        stats = self.paraphraser.get_processing_statistics()
        
        return ProcessingStatsResult(
            current_mode=ProcessingMode(stats['current_mode']),
            total_processed=stats['total_processed'],
            ai_usage_ratio=stats['ai_usage_ratio'],
            cache_size=stats['cache_size'],
            cost_per_paragraph=stats['cost_per_paragraph'],
            average_improvement=stats['average_improvement'],
            mode_switches=stats['cost_tracker'].get('mode_switches', 0),
            turnitin_detections=stats['cost_tracker'].get('turnitin_detections', 0),
            cache_hits=stats['cost_tracker'].get('cache_hits', 0),
            cost_tracker=stats['cost_tracker']
        )
    
    async def get_service_info(self) -> dict:
        """Get Ultimate Hybrid service information"""
        return {
            "service_type": "ultimate_hybrid",
            "paraphraser_available": self._paraphraser is not None,
            "ai_service_configured": bool(self.settings.gemini_api_key),
            "synonym_database_loaded": (
                hasattr(self.paraphraser, 'synonyms') and 
                bool(getattr(self.paraphraser, 'synonyms', {}))
            ),
            "available_modes": ["smart", "balanced", "aggressive", "turnitin_safe"],
            "current_mode": self.paraphraser.mode if self._paraphraser else "smart",
            "features": [
                "smart_routing",
                "turnitin_detection",
                "multiple_modes",
                "cost_optimization",
                "ai_caching",
                "batch_processing",
                "complexity_analysis",
                "academic_optimization"
            ],
            "settings": {
                "max_text_length": 15000,
                "min_text_length": self.settings.min_text_length,
                "max_batch_size": min(self.settings.max_batch_size, 100),
                "supports_caching": True,
                "supports_mode_switching": True
            }
        }