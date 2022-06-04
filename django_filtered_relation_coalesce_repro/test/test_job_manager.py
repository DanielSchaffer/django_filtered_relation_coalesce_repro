from django.test import TestCase

from django_filtered_relation_coalesce_repro.models import Job


class JobManagerTests(TestCase):

    def test_with_actual_worker_data_broken(self):
        qs = Job.objects.with_actual_worker_data_broken()
        print(str(qs.query))

        list(qs)

    def test_with_actual_worker_data_workaround(self):
        qs = Job.objects.with_actual_worker_data_workaround()
        print(str(qs.query))

        list(qs)
