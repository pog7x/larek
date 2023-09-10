from rest_framework import exceptions
from rest_framework.authentication import SessionAuthentication

from larek.middleware import CustomCsrfViewMiddleware


class CSRFCheck(CustomCsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason


class CustomSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        """
        Enforce CSRF validation for session based authentication.
        """

        def dummy_get_response(request):  # pragma: no cover
            return None

        check = CSRFCheck(dummy_get_response)
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied("CSRF Failed: %s" % reason)
