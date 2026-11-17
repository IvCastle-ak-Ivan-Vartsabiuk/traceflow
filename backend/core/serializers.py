
from rest_framework import serializers
from .models import (
    Requirements,
    TestCases,
    TraceLinks,
    TestExecutions,
    RequirementHistory,
)



class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirements
        fields = "__all__"

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Назва вимоги не може бути порожньою."
            )

        return value

    def validate_priority(self, value):
        allowed = ["low", "medium", "high"]

        if value not in allowed:
            raise serializers.ValidationError(
                "Пріоритет має бути low, medium або high."
            )

        return value

    def validate_status(self, value):
        allowed = ["draft", "active", "approved", "archived"]

        if value not in allowed:
            raise serializers.ValidationError(
                "Статус має бути draft, active, approved або archived."
            )

        return value

    def validate(self, attrs):
        parent = attrs.get("parent")

        if self.instance and parent:
            if parent.pk == self.instance.pk:
                raise serializers.ValidationError({
                    "parent": "Вимога не може бути батьківською сама для себе."
                })

        return attrs


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCases
        fields = "__all__"

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Назва тест-кейсу не може бути порожньою."
            )
        return value


class TraceLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TraceLinks
        fields = "__all__"

    def validate(self, attrs):
        requirement = attrs.get(
            "requirement",
            getattr(self.instance, "requirement", None)
        )
        test_case = attrs.get(
            "test_case",
            getattr(self.instance, "test_case", None)
        )

        if requirement and test_case:
            existing = TraceLinks.objects.filter(
                requirement=requirement,
                test_case=test_case
            )
            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                raise serializers.ValidationError(
                    "Такий зв'язок уже існує."
                )

        return attrs


class TestExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestExecutions
        fields = "__all__"


class RequirementHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RequirementHistory
        fields = "__all__"
