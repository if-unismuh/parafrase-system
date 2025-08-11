"""
Custom exceptions for the application
"""

class ParaphraseAPIException(Exception):
    """Base exception for all API errors"""
    def __init__(self, message: str, code: str = "API_ERROR", details: dict = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)

class ValidationError(ParaphraseAPIException):
    """Input validation error"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, "VALIDATION_ERROR", details)

class TextTooLongError(ValidationError):
    """Text exceeds maximum length"""
    def __init__(self, length: int, max_length: int):
        message = f"Text length ({length}) exceeds maximum allowed ({max_length})"
        details = {"length": length, "max_length": max_length}
        super().__init__(message, details)

class TextTooShortError(ValidationError):
    """Text is too short"""
    def __init__(self, length: int, min_length: int):
        message = f"Text length ({length}) is below minimum required ({min_length})"
        details = {"length": length, "min_length": min_length}
        super().__init__(message, details)

class UnsupportedFileTypeError(ValidationError):
    """File type not supported"""
    def __init__(self, file_type: str, supported_types: list):
        message = f"File type '{file_type}' not supported. Supported types: {supported_types}"
        details = {"file_type": file_type, "supported_types": supported_types}
        super().__init__(message, details)

class FileTooLargeError(ValidationError):
    """File exceeds maximum size"""
    def __init__(self, size: int, max_size: int):
        message = f"File size ({size} bytes) exceeds maximum allowed ({max_size} bytes)"
        details = {"size": size, "max_size": max_size}
        super().__init__(message, details)

class ProcessingError(ParaphraseAPIException):
    """Error during processing"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, "PROCESSING_ERROR", details)

class ParaphrasingFailedError(ProcessingError):
    """Paraphrasing process failed"""
    def __init__(self, reason: str):
        message = f"Paraphrasing failed: {reason}"
        super().__init__(message)

class SearchServiceError(ProcessingError):
    """Search service error"""
    def __init__(self, message: str, service: str = "DDGS"):
        details = {"service": service}
        super().__init__(f"Search service error: {message}", details)

class AIServiceError(ProcessingError):
    """AI service error"""
    def __init__(self, message: str, service: str = "Gemini"):
        details = {"service": service}
        super().__init__(f"AI service error: {message}", details)

class AuthenticationError(ParaphraseAPIException):
    """Authentication error"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, "AUTHENTICATION_ERROR")

class AuthorizationError(ParaphraseAPIException):
    """Authorization error"""
    def __init__(self, message: str = "Access denied"):
        super().__init__(message, "AUTHORIZATION_ERROR")

class RateLimitError(ParaphraseAPIException):
    """Rate limit exceeded"""
    def __init__(self, limit: int, window: str):
        message = f"Rate limit exceeded: {limit} requests per {window}"
        details = {"limit": limit, "window": window}
        super().__init__(message, "RATE_LIMIT_ERROR", details)

class JobNotFoundError(ParaphraseAPIException):
    """Job not found"""
    def __init__(self, job_id: str):
        message = f"Job not found: {job_id}"
        details = {"job_id": job_id}
        super().__init__(message, "JOB_NOT_FOUND", details)

class ConfigurationError(ParaphraseAPIException):
    """Configuration error"""
    def __init__(self, message: str):
        super().__init__(message, "CONFIGURATION_ERROR")

class ExternalServiceError(ParaphraseAPIException):
    """External service unavailable"""
    def __init__(self, service: str, message: str = None):
        msg = f"External service '{service}' is unavailable"
        if message:
            msg += f": {message}"
        details = {"service": service}
        super().__init__(msg, "EXTERNAL_SERVICE_ERROR", details)