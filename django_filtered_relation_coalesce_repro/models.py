from django.db.models import (
    BooleanField,
    CASCADE,
    Case,
    CharField,
    F,
    FilteredRelation,
    ForeignKey,
    Manager,
    Model,
    Q,
    When,
)
from django.db.models.functions import Coalesce


class Worker(Model):
    name = CharField(max_length=255)


class Company(Model):
    name = CharField(max_length=255)


class WorkerPreference(Model):
    company = ForeignKey(Company, on_delete=CASCADE, related_name="worker_preferences")
    worker = ForeignKey(Worker, on_delete=CASCADE, related_name="worker_preferences")
    allow_assignments = BooleanField()


class JobManager(Manager):
    def with_actual_worker_data_broken(self):
        return self.annotate(
            job_worker_preference=FilteredRelation(
                relation_name="company__worker_preferences",
                condition=Q(
                    company__worker_preferences__worker=Coalesce(F("worker"), F("worker_substitutions__worker")),
                    company__worker_preferences__company=F("company"),
                )
            ),
            is_allowed=Case(When(job_worker_preference__allow_assignments=True, then=1), default=0, output_field=BooleanField())
        )

    def with_actual_worker_data_workaround(self):
        return self.annotate(
            actual_worker=Coalesce(F("worker"), F("worker_substitutions__worker")),
            job_worker_preference=FilteredRelation(
                relation_name="company__worker_preferences",
                condition=Q(
                    company__worker_preferences__worker=F("actual_worker"),
                    company__worker_preferences__company=F("company"),
                )
            ),
            is_allowed=Case(When(job_worker_preference__allow_assignments=True, then=1), default=0, output_field=BooleanField())
        )


class Job(Model):
    objects = JobManager()

    company = ForeignKey(Company, on_delete=CASCADE, related_name="jobs")
    worker = ForeignKey(Worker, on_delete=CASCADE, related_name="jobs")


class WorkerSubstitution(Model):
    job = ForeignKey(Job, on_delete=CASCADE, related_name="worker_substitutions")
    worker = ForeignKey(Worker, on_delete=CASCADE, related_name="worker_substitutions")

