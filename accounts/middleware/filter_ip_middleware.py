from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin
from accounts.models import BlockUserIP


class FilterIPMiddleware(MiddlewareMixin):
    # Check if client IP is allowed
    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR')
        is_blocked = BlockUserIP.objects.filter(blocked_ip=ip).exists()
        if is_blocked:
            raise PermissionDenied()
        return None
