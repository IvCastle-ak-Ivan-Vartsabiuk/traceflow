
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .models import Requirements


class RequirementAPITests(TestCase):
    databases = {"default"}

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="api_test_user",
            password="TestPassword123!"
        )

    def setUp(self):
        self.client = APIClient()

    def test_get_requirements(self):
        response = self.client.get("/api/requirements/")
        self.assertEqual(response.status_code, 200)

    def test_invalid_priority(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            "/api/requirements/",
            {
                "title": "Тестова вимога",
                "priority": "banana",
                "status": "draft"
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("priority", response.data)

    def test_unauthorized_creation(self):
        response = self.client.post(
            "/api/requirements/",
            {
                "title": "Нова вимога",
                "priority": "high",
                "status": "draft"
            },
            format="json"
        )

        self.assertIn(response.status_code, [401, 403])

    def test_not_found(self):
        response = self.client.get(
            "/api/requirements/99999/"
        )
        self.assertEqual(response.status_code, 404)

    def test_coverage_analytics(self):
        response = self.client.get(
            "/api/analytics/coverage/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "coverage_percentage",
            response.data
        )
