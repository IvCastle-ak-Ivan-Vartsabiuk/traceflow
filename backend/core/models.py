
from django.db import models


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=150)
    email = models.CharField(max_length=254)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'users'


class Requirements(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    parent = models.ForeignKey('self', models.DB_SET_NULL, blank=True, null=True)
    created_by = models.ForeignKey(Users, models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'requirements'


class TestCases(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    steps = models.TextField(blank=True, null=True)
    expected_result = models.TextField(blank=True, null=True)
    needs_review = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_cases'


class TraceLinks(models.Model):
    id = models.BigAutoField(primary_key=True)
    requirement = models.ForeignKey(Requirements, models.DB_CASCADE)
    test_case = models.ForeignKey(TestCases, models.DB_CASCADE)

    class Meta:
        managed = False
        db_table = 'trace_links'
        unique_together = (('requirement', 'test_case'),)


class TestExecutions(models.Model):
    id = models.BigAutoField(primary_key=True)
    test_case = models.ForeignKey(TestCases, models.DB_CASCADE)
    status = models.CharField(max_length=20)
    executed_at = models.DateTimeField(blank=True, null=True)
    executed_by = models.ForeignKey(Users, models.DO_NOTHING, db_column='executed_by', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_executions'


class RequirementHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    requirement = models.ForeignKey(Requirements, models.DB_CASCADE)
    changed_by = models.ForeignKey(Users, models.DO_NOTHING, db_column='changed_by', blank=True, null=True)
    old_data = models.JSONField(blank=True, null=True)
    new_data = models.JSONField(blank=True, null=True)
    changed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'requirement_history'
