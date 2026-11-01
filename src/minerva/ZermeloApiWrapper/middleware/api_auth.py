import secrets
from django.conf import settings
from django.http import JsonResponse
from .. import get_api_wrapper_key

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.valid_api_key = (
            get_api_wrapper_key()
            or getattr(settings, "API_WRAPPER_KEY", "")
        )

    def __call__(self, request):
        if request.path.startswith("/api/"):
            api_key = request.headers.get("X-Api-Key", "")

            if not self.valid_api_key:
                return JsonResponse(
                    {"detail": "API_WRAPPER_KEY is niet geconfigureerd."},
                    status=500,
                )

            if not api_key or not secrets.compare_digest(
                api_key, self.valid_api_key
            ):
                return JsonResponse(
                    {"detail": "Ongeldige of ontbrekende API-sleutel."},
                    status=401,
                )

        return self.get_response(request)