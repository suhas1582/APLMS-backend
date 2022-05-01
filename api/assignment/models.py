from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Assignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    due_date = models.DateTimeField()
    max_marks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    standard = models.IntegerField()
    section = models.CharField(max_length=3)

    def __str__(self):
        return self.title

    
