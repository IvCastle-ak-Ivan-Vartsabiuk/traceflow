
from django.test.runner import DiscoverRunner
from django.db import connections

from .models import (
    Users,
    Requirements,
    TestCases,
    TraceLinks,
    TestExecutions,
    RequirementHistory,
)


class ExistingTablesTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        result = super().setup_databases(**kwargs)

        connection = connections["default"]

        with connection.schema_editor() as editor:
            for model in [
                Users,
                Requirements,
                TestCases,
                TraceLinks,
                TestExecutions,
                RequirementHistory,
            ]:
                editor.create_model(model)

        return result
