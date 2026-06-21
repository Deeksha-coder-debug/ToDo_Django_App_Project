import logging
import time
from django.conf import settings

logger = logging.getLogger(__name__)


class TaskMateAuditMiddleware:
    """
    Production middleware for security headers and audit logging.
    Extends Django's built-in auth, does NOT replace it.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        # Audit log for all mutating requests
        if request.method in ['POST', 'PUT', 'DELETE']:
            user = request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
            logger.info(
                f"ACTION | User:{user} | Method:{request.method} | Path:{request.path} | IP:{self.get_client_ip(request)}"
            )
        
        response = self.get_response(request)
        
        # Security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Performance header
        duration = time.time() - start_time
        response['X-Response-Time'] = f"{duration:.3f}s"
        
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')


class TaskMateSecurityHeadersMiddleware:
    """
    Additional security for production deployments.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # HSTS - only if you have HTTPS enabled
        if not settings.DEBUG:
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
