
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from .permissions import IsAuthenticatedEditorOrAdmin

from .models import (
    Requirements,
    TestCases,
    TraceLinks,
    TestExecutions,
    RequirementHistory,
)

from .serializers import (
    RequirementSerializer,
    TestCaseSerializer,
    TraceLinkSerializer,
    TestExecutionSerializer,
    RequirementHistorySerializer,
)



class RequirementViewSet(viewsets.ModelViewSet):
    queryset = Requirements.objects.all().order_by("id")
    serializer_class = RequirementSerializer
    permission_classes = [IsAuthenticatedEditorOrAdmin]

    @transaction.atomic
    def perform_update(self, serializer):
        requirement = serializer.instance

        old_data = {
            "title": requirement.title,
            "description": requirement.description,
            "priority": requirement.priority,
            "status": requirement.status,
            "parent_id": requirement.parent_id,
        }

        serializer.save(updated_at=timezone.now())

        requirement.refresh_from_db()

        new_data = {
            "title": requirement.title,
            "description": requirement.description,
            "priority": requirement.priority,
            "status": requirement.status,
            "parent_id": requirement.parent_id,
        }

       
        if old_data != new_data:
            RequirementHistory.objects.create(
                requirement=requirement,
                changed_by=None,
                old_data=old_data,
                new_data=new_data,
                changed_at=timezone.now(),
            )

            linked_test_ids = TraceLinks.objects.filter(
                requirement=requirement
            ).values_list("test_case_id", flat=True)

            TestCases.objects.filter(
                id__in=linked_test_ids
            ).update(needs_review=True)



class TestCaseViewSet(viewsets.ModelViewSet):
    queryset = TestCases.objects.all().order_by("id")
    serializer_class = TestCaseSerializer
    permission_classes = [IsAuthenticatedEditorOrAdmin]


class TraceLinkViewSet(viewsets.ModelViewSet):
    queryset = TraceLinks.objects.all().order_by("id")
    serializer_class = TraceLinkSerializer
    permission_classes = [IsAuthenticatedEditorOrAdmin]


class TestExecutionViewSet(viewsets.ModelViewSet):
    queryset = TestExecutions.objects.all().order_by("id")
    serializer_class = TestExecutionSerializer
    permission_classes = [IsAuthenticatedEditorOrAdmin]


class RequirementHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RequirementHistory.objects.all().order_by("-id")
    serializer_class = RequirementHistorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@api_view(["GET"])
@permission_classes([AllowAny])
def coverage_analytics(request):
    requirements = Requirements.objects.annotate(
        test_count=Count("tracelinks")
    )

    total = requirements.count()
    covered = requirements.filter(test_count__gt=0).count()
    uncovered = total - covered

    percentage = round(
        (covered / total * 100) if total else 0,
        2
    )

    return Response({
        "total_requirements": total,
        "covered_requirements": covered,
        "uncovered_requirements": uncovered,
        "coverage_percentage": percentage
    })


@api_view(["GET"])
@permission_classes([AllowAny])
def uncovered_requirements(request):
    requirements = Requirements.objects.annotate(
        test_count=Count("tracelinks")
    ).filter(test_count=0).order_by("id")

    serializer = RequirementSerializer(
        requirements,
        many=True
    )

    return Response({
        "count": requirements.count(),
        "requirements": serializer.data
    })
