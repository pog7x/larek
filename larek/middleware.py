from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.exceptions import ImproperlyConfigured
from django.middleware.csrf import (
    CSRF_SESSION_KEY,
    CSRF_TOKEN_LENGTH,
    CsrfViewMiddleware,
    _check_token_format,
    _unmask_cipher_token,
)


class CustomSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        if not session_key:
            session_key = request.headers.get("X-Sessionid")
        request.session = self.SessionStore(session_key)


class CustomCsrfViewMiddleware(CsrfViewMiddleware):
    def _get_secret(self, request):
        if settings.CSRF_USE_SESSIONS:
            try:
                csrf_secret = request.session.get(CSRF_SESSION_KEY)
            except AttributeError:
                raise ImproperlyConfigured(
                    "CSRF_USE_SESSIONS is enabled, but request.session is not "
                    "set. SessionMiddleware must appear before CsrfViewMiddleware "
                    "in MIDDLEWARE."
                )
        else:
            try:
                csrf_secret = request.COOKIES.get(settings.CSRF_COOKIE_NAME)
                if not csrf_secret:
                    csrf_secret = request.headers["X-Csrftoken"]
            except KeyError:
                csrf_secret = None
            else:
                # This can raise InvalidTokenFormat.
                _check_token_format(csrf_secret)
        if csrf_secret is None:
            return None
        # Django versions before 4.0 masked the secret before storing.
        if len(csrf_secret) == CSRF_TOKEN_LENGTH:
            csrf_secret = _unmask_cipher_token(csrf_secret)
        return csrf_secret
