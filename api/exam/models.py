from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class Exam(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exam_type = models.CharField(max_length=50)
    exam_date = models.DateTimeField()
    subject = models.CharField(max_length=50)
    max_marks = models.IntegerField()
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE)
    standard = models.IntegerField()
    section = models.CharField(max_length=3)

    def __str__(self):
        return self.exam_type
