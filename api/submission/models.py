from django.db import models
import uuid
from django.contrib.auth.models import User
from api.assignment.models import Assignment

# Create your models here.
class Submission(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    is_evaluated = models.BooleanField(default=False)
    marks_scored = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.assignment_id.title
