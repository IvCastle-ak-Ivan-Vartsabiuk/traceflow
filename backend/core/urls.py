
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import coverage_analytics
from .views import uncovered_requirements

from .views import (
    RequirementViewSet,
    TestCaseViewSet,
    TraceLinkViewSet,
    TestExecutionViewSet,
    RequirementHistoryViewSet,
)

router = DefaultRouter()

router.register(
    "requirements",
    RequirementViewSet,
    basename="requirements"
)
router.register(
    "test-cases",
    TestCaseViewSet,
    basename="test-cases"
)
router.register(
    "trace-links",
    TraceLinkViewSet,
    basename="trace-links"
)
router.register(
    "test-executions",
    TestExecutionViewSet,
    basename="test-executions"
)
router.register(
    "requirement-history",
    RequirementHistoryViewSet,
    basename="requirement-history"
)


urlpatterns = [
    path("analytics/coverage/", coverage_analytics),
    path("analytics/uncovered/", uncovered_requirements),
    path("", include(router.urls)),
]

