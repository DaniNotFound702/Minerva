import os
import unittest
import json

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "minerva.ZermeloApiWrapper.settings",
)

import django

django.setup()

from django.http import JsonResponse
from django.test import RequestFactory

from minerva import configure_api_wrapper
from minerva.ZermeloApiWrapper.middleware.api_auth import APIKeyMiddleware


class APIKeyMiddlewareTests(unittest.TestCase):
    def setUp(self):
        configure_api_wrapper("test-wrapper-key")
        self.factory = RequestFactory()
        self.middleware = APIKeyMiddleware(
            lambda request: JsonResponse({"ok": True})
        )

    def test_accepts_configured_key(self):
        request = self.factory.get(
            "/api/students/",
            HTTP_X_API_KEY="test-wrapper-key",
        )

        response = self.middleware(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"ok": True})

    def test_rejects_wrong_key(self):
        request = self.factory.get(
            "/api/students/",
            HTTP_X_API_KEY="wrong-key",
        )

        response = self.middleware(request)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            json.loads(response.content)["detail"],
            "Ongeldige of ontbrekende API-sleutel.",
        )

    def test_rejects_missing_key(self):
        request = self.factory.get("/api/students/")

        response = self.middleware(request)

        self.assertEqual(response.status_code, 401)

    def test_does_not_require_key_for_non_api_paths(self):
        request = self.factory.get("/health/")

        response = self.middleware(request)

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
