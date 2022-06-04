from django.test import TestCase

from django_filtered_relation_coalesce_repro.models import Job


class JobManagerTests(TestCase):

    def test_with_actual_worker_data_broken(self):
        list(Job.objects.with_actual_worker_data_broken())

    def test_with_actual_worker_data_workaround(self):
        list(Job.objects.with_actual_worker_data_workaround())
