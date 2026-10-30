import os
from django.http import JsonResponse

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.valid_api_key = os.getenv("API_WRAPPER_KEY")

    def __call__(self, request):
        # Controleer alleen specifieke endpoints (bijv. alles wat begint met /api/)
        if request.path.startswith('/api/'):
            # Headers worden in Django HttpRequest.headers uitgelezen (of via request.META['HTTP_X_API_KEY'])
            api_key = request.headers.get('X-Api-Key')

            if not api_key or api_key != self.valid_api_key:
                return JsonResponse(
                    {"detail": "Ongeldige of ontbrekende API-sleutel."}, 
                    status=401
                )

        return self.get_response(request)