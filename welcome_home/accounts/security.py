from .models import AuditLog


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def create_audit_log(request, action, details="", user=None):
    request_user = getattr(request, 'user', None)

    AuditLog.objects.create(
        user=user if user else request_user if request_user and request_user.is_authenticated else None,
        action=action,
        details=details,
        ip_address=get_client_ip(request),
    )