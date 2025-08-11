"""
Integrated Smart Paraphrase service
Business logic for comprehensive plagiarism detection and paraphrasing workflow
"""
import time
from typing import List, Optional, Dict, Any
from pathlib import Path
from datetime import datetime
import sys

# Add the parent directory to sys.path to import IntegratedSmartParaphraseSystem
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

# Mock the integrated system imports for now - we'll implement the actual integration later
# from integrated_smart_paraphrase_system import IntegratedSmartParaphraseSystem

from app.core.config import Settings
from app.core.exceptions import (
    ParaphrasingFailedError,
    TextTooLongError,
    TextTooShortError,
    ProcessingError,
    AIServiceError
)
from app.api.models.integrated_smart import (
    AnalyzeAndParaphraseRequest,
    IntegratedSmartResult,
    BatchAnalyzeAndParaphraseRequest,
    BatchIntegratedSmartResult,
    IntegratedSmartBatchSummary,
    PlagiarismCheckRequest,
    PlagiarismCheckResult,
    WorkflowStatsResult,
    AnalysisReport,
    ParagraphAnalysis,
    IntegratedSmartProcessingMetadata,
    CombinedRiskAnalysis,
    OnlineAnalysisResult,
    PatternAnalysisResult,
    WorkflowRecommendation,
    RiskLevel,
    ActionPriority,
    RecommendedAction
)
from app.api.models.common import ProcessingMethod

class IntegratedSmartService:
    """Service for handling Integrated Smart paraphrasing operations"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self._system: Optional[Any] = None
        self._mock_mode = True  # Use mock mode until we integrate the actual system
        self._stats = {
            'total_workflows': 0,
            'total_paragraphs_analyzed': 0,
            'total_paragraphs_paraphrased': 0,
            'processing_times': [],
            'risk_distribution': {'very_high': 0, 'high': 0, 'medium': 0, 'low': 0},
            'online_detection_success': 0,
            'pattern_analysis_success': 0,
            'paraphrasing_success': 0
        }
        self._initialize_system()
    
    def _initialize_system(self):
        """Initialize the Integrated Smart system"""
        try:
            if self._mock_mode:
                # Use mock implementation for now
                print("⚠️  Using mock Integrated Smart system - full implementation pending")
                self._system = None
            else:
                # TODO: Initialize actual IntegratedSmartParaphraseSystem when ready
                pass
                
        except Exception as e:
            raise ProcessingError(f"Failed to initialize Integrated Smart system: {e}")
    
    @property
    def system(self):
        """Get system instance"""
        return self._system
    
    def _validate_text_length(self, text: str) -> None:
        """Validate text length against settings"""
        text_length = len(text)
        
        if text_length < self.settings.min_text_length:
            raise TextTooShortError(text_length, self.settings.min_text_length)
        
        if text_length > 20000:  # Integrated Smart supports longer texts
            raise TextTooLongError(text_length, 20000)
    
    def _mock_online_detection(self, text: str) -> Dict[str, Any]:
        """Mock online plagiarism detection"""
        import random
        
        # Simulate online detection based on text characteristics
        word_count = len(text.split())
        
        # Simulate higher similarity for academic-looking text
        academic_indicators = sum(1 for word in ['penelitian', 'analisis', 'metode', 'sistem', 'teori'] if word in text.lower())
        base_similarity = min(20 + (academic_indicators * 15) + random.uniform(0, 30), 95)
        
        sources_found = random.randint(0, 8) if base_similarity > 30 else 0
        confidence = min(70 + random.uniform(0, 30), 100)
        
        return {
            'similarity': round(base_similarity, 2),
            'sources_found': sources_found,
            'confidence': round(confidence, 2),
            'risk_level': self._get_risk_level_from_similarity(base_similarity),
            'details': {
                'processing_time_ms': random.randint(2000, 8000),
                'sources_checked': random.randint(50, 200),
                'matched_phrases': random.randint(0, 5) if base_similarity > 50 else 0
            }
        }
    
    def _mock_pattern_analysis(self, text: str) -> Dict[str, Any]:
        """Mock pattern-based risk analysis"""
        import random
        
        # Analyze common academic patterns
        patterns = [
            'penelitian.*menunjukkan',
            'hasil.*penelitian',
            'berdasarkan.*analisis',
            'dapat.*disimpulkan',
            'menurut.*\\(\\d{4}\\)',
            'definisi.*adalah'
        ]
        
        patterns_detected = 0
        pattern_types = []
        
        for pattern in patterns:
            import re
            if re.search(pattern, text.lower()):
                patterns_detected += 1
                pattern_types.append(pattern.split('.*')[0])  # Simplified pattern name
        
        # Risk score based on pattern density and academic content
        words = text.split()
        pattern_density = patterns_detected / len(words) * 1000 if words else 0
        risk_score = min(pattern_density * 10 + random.uniform(0, 20), 95)
        
        return {
            'risk_score': round(risk_score, 2),
            'patterns_detected': patterns_detected,
            'pattern_types': pattern_types,
            'risk_level': self._get_risk_level_from_similarity(risk_score),
            'details': {
                'pattern_density': round(pattern_density, 3),
                'academic_indicators': sum(1 for word in ['penelitian', 'analisis', 'metode'] if word in text.lower()),
                'citation_patterns': len(re.findall(r'\\(\\d{4}\\)', text))
            }
        }
    
    def _get_risk_level_from_similarity(self, similarity: float) -> RiskLevel:
        """Convert similarity score to risk level"""
        if similarity >= 80:
            return RiskLevel.VERY_HIGH
        elif similarity >= 50:
            return RiskLevel.HIGH
        elif similarity >= 20:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _combine_risk_analysis(self, online_result: dict, pattern_result: dict) -> CombinedRiskAnalysis:
        """Combine online and pattern analysis results"""
        online_score = online_result['similarity']
        pattern_score = pattern_result['risk_score']
        
        # Weighted combination (70% online, 30% pattern)
        combined_score = (online_score * 0.7) + (pattern_score * 0.3)
        
        # Determine risk level and recommendation
        if combined_score >= 80:
            risk_level = RiskLevel.VERY_HIGH
            recommendation = RecommendedAction.IMMEDIATE_PARAPHRASE
            priority = ActionPriority.CRITICAL
        elif combined_score >= 50:
            risk_level = RiskLevel.HIGH
            recommendation = RecommendedAction.PARAPHRASE_REQUIRED
            priority = ActionPriority.HIGH
        elif combined_score >= 20:
            risk_level = RiskLevel.MEDIUM
            recommendation = RecommendedAction.PARAPHRASE_RECOMMENDED
            priority = ActionPriority.MEDIUM
        else:
            risk_level = RiskLevel.LOW
            recommendation = RecommendedAction.MONITOR_ONLY
            priority = ActionPriority.LOW
        
        confidence = min((online_result['confidence'] + 80) / 2, 100)  # Assume pattern analysis has ~80% confidence
        
        return CombinedRiskAnalysis(
            online_score=online_score,
            pattern_score=pattern_score,
            combined_score=round(combined_score, 2),
            risk_level=risk_level,
            recommendation=recommendation,
            priority=priority,
            confidence=round(confidence, 2)
        )
    
    def _mock_paraphrase_paragraph(self, text: str, mode: str) -> Dict[str, Any]:
        """Mock paragraph paraphrasing"""
        import random
        
        # Simulate paraphrasing effectiveness based on mode
        effectiveness_map = {
            'smart': 0.6,
            'balanced': 0.75,
            'aggressive': 0.85,
            'turnitin_safe': 0.8
        }
        
        effectiveness = effectiveness_map.get(mode, 0.6)
        
        # Simulate improvement
        similarity_reduction = random.uniform(20, 60) * effectiveness
        new_similarity = max(10, 80 - similarity_reduction)  # Assume original was ~80%
        
        # Create mock paraphrased text (in real implementation, this would be actual paraphrasing)
        paraphrased = f"[PARAPHRASED-{mode.upper()}] {text[:100]}..." if len(text) > 100 else f"[PARAPHRASED-{mode.upper()}] {text}"
        
        return {
            'paraphrased_text': paraphrased,
            'original_similarity': 80.0,  # Mock original similarity
            'new_similarity': round(new_similarity, 2),
            'improvement': round(80 - new_similarity, 2),
            'method_used': f'mock_{mode}',
            'processing_time_ms': random.randint(1000, 5000),
            'changes_made': random.randint(3, 12)
        }
    
    def _analyze_single_text(self, text: str, enable_online: bool, enable_pattern: bool) -> AnalysisReport:
        """Analyze a single text for plagiarism risk"""
        start_time = time.time()
        
        # Split text into paragraphs (simple split for now)
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        if not paragraphs:
            paragraphs = [text]  # Treat as single paragraph
        
        paragraphs_analyzed = []
        risk_summary = {'very_high': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        online_detection_time = 0
        pattern_analysis_time = 0
        
        for i, paragraph in enumerate(paragraphs):
            if len(paragraph.split()) < 5:  # Skip very short paragraphs
                continue
                
            # Online detection
            online_result = None
            if enable_online:
                online_start = time.time()
                online_data = self._mock_online_detection(paragraph)
                online_end = time.time()
                online_detection_time += (online_end - online_start) * 1000
                
                online_result = OnlineAnalysisResult(
                    similarity=online_data['similarity'],
                    sources_found=online_data['sources_found'],
                    confidence=online_data['confidence'],
                    risk_level=online_data['risk_level'],
                    details=online_data['details']
                )
            
            # Pattern analysis
            pattern_result = None
            if enable_pattern:
                pattern_start = time.time()
                pattern_data = self._mock_pattern_analysis(paragraph)
                pattern_end = time.time()
                pattern_analysis_time += (pattern_end - pattern_start) * 1000
                
                pattern_result = PatternAnalysisResult(
                    risk_score=pattern_data['risk_score'],
                    patterns_detected=pattern_data['patterns_detected'],
                    pattern_types=pattern_data['pattern_types'],
                    risk_level=pattern_data['risk_level'],
                    details=pattern_data['details']
                )
            
            # Combined analysis
            if online_result and pattern_result:
                combined_analysis = self._combine_risk_analysis(
                    {'similarity': online_result.similarity, 'confidence': online_result.confidence},
                    {'risk_score': pattern_result.risk_score}
                )
            elif online_result:
                combined_analysis = CombinedRiskAnalysis(
                    online_score=online_result.similarity,
                    pattern_score=0.0,
                    combined_score=online_result.similarity,
                    risk_level=online_result.risk_level,
                    recommendation=RecommendedAction.PARAPHRASE_REQUIRED if online_result.similarity > 50 else RecommendedAction.MONITOR_ONLY,
                    priority=ActionPriority.HIGH if online_result.similarity > 50 else ActionPriority.LOW,
                    confidence=online_result.confidence
                )
            elif pattern_result:
                combined_analysis = CombinedRiskAnalysis(
                    online_score=0.0,
                    pattern_score=pattern_result.risk_score,
                    combined_score=pattern_result.risk_score,
                    risk_level=pattern_result.risk_level,
                    recommendation=RecommendedAction.PARAPHRASE_RECOMMENDED if pattern_result.risk_score > 30 else RecommendedAction.MONITOR_ONLY,
                    priority=ActionPriority.MEDIUM if pattern_result.risk_score > 30 else ActionPriority.LOW,
                    confidence=75.0  # Default confidence for pattern-only analysis
                )
            else:
                # No analysis enabled - default to low risk
                combined_analysis = CombinedRiskAnalysis(
                    online_score=0.0,
                    pattern_score=0.0,
                    combined_score=0.0,
                    risk_level=RiskLevel.LOW,
                    recommendation=RecommendedAction.NO_ACTION,
                    priority=ActionPriority.LOW,
                    confidence=50.0
                )
            
            # Create paragraph analysis
            para_analysis = ParagraphAnalysis(
                paragraph_index=i + 1,
                text_preview=paragraph[:100] + ('...' if len(paragraph) > 100 else ''),
                online_analysis=online_result,
                pattern_analysis=pattern_result,
                combined_analysis=combined_analysis,
                paraphrased=False
            )
            
            paragraphs_analyzed.append(para_analysis)
            risk_summary[combined_analysis.risk_level.value] += 1
        
        # Generate recommendations
        recommendations = []
        if risk_summary['very_high'] > 0:
            recommendations.append(WorkflowRecommendation(
                priority=ActionPriority.CRITICAL,
                action=RecommendedAction.IMMEDIATE_PARAPHRASE,
                description=f"🚨 {risk_summary['very_high']} paragraphs require immediate paraphrasing",
                paragraphs_affected=risk_summary['very_high'],
                estimated_time="15-30 minutes"
            ))
        
        if risk_summary['high'] > 0:
            recommendations.append(WorkflowRecommendation(
                priority=ActionPriority.HIGH,
                action=RecommendedAction.PARAPHRASE_REQUIRED,
                description=f"⚠️ {risk_summary['high']} paragraphs need paraphrasing",
                paragraphs_affected=risk_summary['high'],
                estimated_time="10-20 minutes"
            ))
        
        if risk_summary['medium'] > 0:
            recommendations.append(WorkflowRecommendation(
                priority=ActionPriority.MEDIUM,
                action=RecommendedAction.PARAPHRASE_RECOMMENDED,
                description=f"💡 {risk_summary['medium']} paragraphs would benefit from paraphrasing",
                paragraphs_affected=risk_summary['medium'],
                estimated_time="5-10 minutes"
            ))
        
        end_time = time.time()
        total_time = int((end_time - start_time) * 1000)
        
        # Create metadata
        metadata = IntegratedSmartProcessingMetadata(
            method=ProcessingMethod.LOCAL_PLUS_AI,  # Assume hybrid approach
            similarity=sum(p.combined_analysis.combined_score for p in paragraphs_analyzed) / len(paragraphs_analyzed) if paragraphs_analyzed else 0,
            plagiarism_reduction=0.0,  # Not applicable for analysis-only
            quality_score=75.0,  # Default quality score for analysis
            changes_made=0,  # No changes in analysis phase
            processing_time_ms=total_time,
            api_calls_used=len(paragraphs_analyzed) if enable_online else 0,
            cost_estimate=len(paragraphs_analyzed) * 0.001 if enable_online else 0.0,
            online_detection_time_ms=int(online_detection_time),
            pattern_analysis_time_ms=int(pattern_analysis_time),
            paraphrasing_time_ms=0,
            total_analysis_time_ms=int(online_detection_time + pattern_analysis_time),
            paragraphs_analyzed=len(paragraphs_analyzed),
            paragraphs_paraphrased=0,
            online_sources_checked=sum(p.online_analysis.sources_found for p in paragraphs_analyzed if p.online_analysis) if enable_online else 0,
            patterns_analyzed=sum(p.pattern_analysis.patterns_detected for p in paragraphs_analyzed if p.pattern_analysis) if enable_pattern else 0,
            risk_distribution=risk_summary
        )
        
        return AnalysisReport(
            filename=None,
            analysis_timestamp=datetime.now(),
            total_paragraphs=len(paragraphs),
            paragraphs_analyzed=paragraphs_analyzed,
            risk_summary=risk_summary,
            recommendations=recommendations,
            metadata=metadata
        )
    
    async def analyze_and_paraphrase(self, request: AnalyzeAndParaphraseRequest) -> IntegratedSmartResult:
        """Analyze text and optionally paraphrase high-risk portions"""
        # Validate input
        self._validate_text_length(request.text)
        
        try:
            # Step 1: Analyze the text
            analysis_report = self._analyze_single_text(
                request.text,
                request.enable_online_detection,
                request.enable_pattern_analysis
            )
            
            paraphrased_text = None
            paraphrasing_summary = None
            
            # Step 2: Auto-paraphrase if enabled
            if request.auto_paraphrase:
                paraphrasing_start = time.time()
                paraphrased_paragraphs = []
                paraphrasing_stats = {
                    'paragraphs_processed': 0,
                    'paragraphs_paraphrased': 0,
                    'total_improvement': 0.0,
                    'paraphrasing_details': []
                }
                
                # Paraphrase paragraphs that meet the threshold
                text_paragraphs = [p.strip() for p in request.text.split('\n\n') if p.strip()]
                if not text_paragraphs:
                    text_paragraphs = [request.text]
                
                for i, (paragraph, analysis) in enumerate(zip(text_paragraphs, analysis_report.paragraphs_analyzed)):
                    paraphrasing_stats['paragraphs_processed'] += 1
                    
                    if analysis.combined_analysis.combined_score >= request.paraphrase_threshold:
                        # Paraphrase this paragraph
                        paraphrase_result = self._mock_paraphrase_paragraph(paragraph, request.processing_mode)
                        
                        paraphrased_paragraphs.append(paraphrase_result['paraphrased_text'])
                        paraphrasing_stats['paragraphs_paraphrased'] += 1
                        paraphrasing_stats['total_improvement'] += paraphrase_result['improvement']
                        
                        # Update analysis with paraphrasing result
                        analysis.paraphrased = True
                        analysis.paraphrase_result = paraphrase_result
                        
                        paraphrasing_stats['paraphrasing_details'].append({
                            'paragraph_index': i + 1,
                            'original_risk': analysis.combined_analysis.combined_score,
                            'improvement': paraphrase_result['improvement'],
                            'method': paraphrase_result['method_used']
                        })
                    else:
                        paraphrased_paragraphs.append(paragraph)  # Keep original
                
                paraphrasing_end = time.time()
                paraphrasing_time = int((paraphrasing_end - paraphrasing_start) * 1000)
                
                paraphrased_text = '\n\n'.join(paraphrased_paragraphs)
                
                paraphrasing_summary = {
                    'paragraphs_processed': paraphrasing_stats['paragraphs_processed'],
                    'paragraphs_paraphrased': paraphrasing_stats['paragraphs_paraphrased'],
                    'average_improvement': paraphrasing_stats['total_improvement'] / paraphrasing_stats['paragraphs_paraphrased'] if paraphrasing_stats['paragraphs_paraphrased'] > 0 else 0,
                    'processing_time_ms': paraphrasing_time,
                    'details': paraphrasing_stats['paraphrasing_details']
                }
                
                # Update metadata
                analysis_report.metadata.paraphrasing_time_ms = paraphrasing_time
                analysis_report.metadata.paragraphs_paraphrased = paraphrasing_stats['paragraphs_paraphrased']
            
            # Update stats
            self._stats['total_workflows'] += 1
            self._stats['total_paragraphs_analyzed'] += analysis_report.metadata.paragraphs_analyzed
            self._stats['total_paragraphs_paraphrased'] += analysis_report.metadata.paragraphs_paraphrased
            
            return IntegratedSmartResult(
                original_text=request.text,
                paraphrased_text=paraphrased_text,
                analysis_report=analysis_report,
                paraphrasing_summary=paraphrasing_summary,
                workflow_completed=True
            )
            
        except Exception as e:
            if isinstance(e, (TextTooLongError, TextTooShortError)):
                raise
            raise ParaphrasingFailedError(f"Integrated Smart processing failed: {str(e)}")
    
    async def plagiarism_check_only(self, request: PlagiarismCheckRequest) -> PlagiarismCheckResult:
        """Perform plagiarism check without paraphrasing"""
        # Validate input
        self._validate_text_length(request.text)
        
        try:
            analysis_report = self._analyze_single_text(
                request.text,
                request.enable_online_detection,
                request.enable_pattern_analysis
            )
            
            return PlagiarismCheckResult(
                original_text=request.text,
                analysis_report=analysis_report
            )
            
        except Exception as e:
            if isinstance(e, (TextTooLongError, TextTooShortError)):
                raise
            raise ParaphrasingFailedError(f"Plagiarism check failed: {str(e)}")
    
    async def analyze_and_paraphrase_batch(self, request: BatchAnalyzeAndParaphraseRequest) -> BatchIntegratedSmartResult:
        """Process multiple texts with integrated smart workflow"""
        # Validate batch size
        max_batch_size = min(self.settings.max_batch_size, 50)
        if len(request.texts) > max_batch_size:
            raise ProcessingError(
                f"Batch size ({len(request.texts)}) exceeds maximum allowed ({max_batch_size})"
            )
        
        results: List[IntegratedSmartResult] = []
        successful = 0
        failed = 0
        total_processing_time = 0
        total_paragraphs_analyzed = 0
        total_paragraphs_paraphrased = 0
        risk_distribution = {'very_high': 0, 'high': 0, 'medium': 0, 'low': 0}
        total_risk_scores = []
        total_improvements = []
        
        for text in request.texts:
            try:
                # Create individual request
                individual_request = AnalyzeAndParaphraseRequest(
                    text=text,
                    auto_paraphrase=request.auto_paraphrase,
                    paraphrase_threshold=request.paraphrase_threshold,
                    enable_online_detection=request.enable_online_detection,
                    enable_pattern_analysis=request.enable_pattern_analysis,
                    processing_mode=request.processing_mode
                )
                
                # Process text
                result = await self.analyze_and_paraphrase(individual_request)
                results.append(result)
                
                # Update statistics
                successful += 1
                total_processing_time += result.analysis_report.metadata.processing_time_ms
                total_paragraphs_analyzed += result.analysis_report.metadata.paragraphs_analyzed
                total_paragraphs_paraphrased += result.analysis_report.metadata.paragraphs_paraphrased
                
                # Risk distribution
                for risk_level, count in result.analysis_report.risk_summary.items():
                    risk_distribution[risk_level] += count
                
                # Average risk score
                if result.analysis_report.paragraphs_analyzed:
                    avg_risk = sum(p.combined_analysis.combined_score for p in result.analysis_report.paragraphs_analyzed) / len(result.analysis_report.paragraphs_analyzed)
                    total_risk_scores.append(avg_risk)
                
                # Paraphrasing effectiveness
                if result.paraphrasing_summary and result.paraphrasing_summary.get('average_improvement'):
                    total_improvements.append(result.paraphrasing_summary['average_improvement'])
                
            except Exception as e:
                failed += 1
                # Create error result
                error_result = IntegratedSmartResult(
                    original_text=text,
                    paraphrased_text=None,
                    analysis_report=AnalysisReport(
                        analysis_timestamp=datetime.now(),
                        total_paragraphs=0,
                        paragraphs_analyzed=[],
                        risk_summary={'very_high': 0, 'high': 0, 'medium': 0, 'low': 0},
                        recommendations=[],
                        metadata=IntegratedSmartProcessingMetadata(
                            method=ProcessingMethod.LOCAL_ONLY,
                            similarity=0.0,
                            plagiarism_reduction=0.0,
                            quality_score=0.0,
                            changes_made=0,
                            processing_time_ms=0,
                            api_calls_used=0,
                            online_detection_time_ms=0,
                            pattern_analysis_time_ms=0,
                            paraphrasing_time_ms=0,
                            total_analysis_time_ms=0,
                            paragraphs_analyzed=0,
                            paragraphs_paraphrased=0,
                            online_sources_checked=0,
                            patterns_analyzed=0,
                            risk_distribution={'very_high': 0, 'high': 0, 'medium': 0, 'low': 0}
                        )
                    ),
                    paraphrasing_summary=None,
                    workflow_completed=False
                )
                results.append(error_result)
        
        # Calculate summary statistics
        average_risk_score = sum(total_risk_scores) / len(total_risk_scores) if total_risk_scores else 0.0
        paraphrasing_effectiveness = sum(total_improvements) / len(total_improvements) if total_improvements else 0.0
        
        online_detection_coverage = (
            sum(1 for r in results if r.analysis_report.metadata.online_sources_checked > 0) / len(results) * 100
            if results else 0.0
        )
        
        pattern_analysis_coverage = (
            sum(1 for r in results if r.analysis_report.metadata.patterns_analyzed > 0) / len(results) * 100
            if results else 0.0
        )
        
        summary = IntegratedSmartBatchSummary(
            total_texts=len(request.texts),
            successful=successful,
            failed=failed,
            total_paragraphs_analyzed=total_paragraphs_analyzed,
            total_paragraphs_paraphrased=total_paragraphs_paraphrased,
            total_processing_time_ms=total_processing_time,
            average_risk_score=round(average_risk_score, 2),
            risk_distribution=risk_distribution,
            paraphrasing_effectiveness=round(paraphrasing_effectiveness, 2),
            online_detection_coverage=round(online_detection_coverage, 2),
            pattern_analysis_coverage=round(pattern_analysis_coverage, 2)
        )
        
        return BatchIntegratedSmartResult(
            results=results,
            summary=summary
        )
    
    async def get_workflow_stats(self) -> WorkflowStatsResult:
        """Get workflow processing statistics"""
        avg_processing_time = (
            sum(self._stats['processing_times']) / len(self._stats['processing_times'])
            if self._stats['processing_times'] else 0
        )
        
        return WorkflowStatsResult(
            total_workflows_processed=self._stats['total_workflows'],
            total_paragraphs_analyzed=self._stats['total_paragraphs_analyzed'],
            total_paragraphs_paraphrased=self._stats['total_paragraphs_paraphrased'],
            average_processing_time_ms=int(avg_processing_time),
            risk_level_distribution=self._stats['risk_distribution'],
            online_detection_success_rate=95.0,  # Mock value
            pattern_analysis_success_rate=98.0,  # Mock value
            paraphrasing_success_rate=92.0,  # Mock value
            average_improvement_score=45.0,  # Mock value
            most_common_patterns=['academic_citations', 'research_methodology', 'conclusion_patterns'],
            processing_mode_usage={'smart': 60, 'balanced': 25, 'aggressive': 10, 'turnitin_safe': 5}
        )
    
    async def get_service_info(self) -> dict:
        """Get Integrated Smart service information"""
        return {
            "service_type": "integrated_smart",
            "system_available": self._system is not None,
            "mock_mode": self._mock_mode,
            "features": [
                "online_plagiarism_detection",
                "pattern_based_analysis",
                "automated_workflow",
                "comprehensive_reporting",
                "risk_assessment",
                "intelligent_paraphrasing",
                "batch_processing"
            ],
            "supported_modes": ["smart", "balanced", "aggressive", "turnitin_safe"],
            "analysis_capabilities": {
                "online_detection": "Searches internet sources for similar content",
                "pattern_analysis": "Identifies common plagiarism patterns",
                "risk_scoring": "Combines multiple analysis methods",
                "workflow_automation": "Automated decision making"
            },
            "settings": {
                "max_text_length": 20000,
                "min_text_length": self.settings.min_text_length,
                "max_batch_size": min(self.settings.max_batch_size, 50),
                "default_paraphrase_threshold": 70.0,
                "supports_auto_paraphrasing": True
            }
        }