# PDF metadata model
from django.db import models
from core.models import User
from django.utils import timezone


class Statement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="statements")
    uploaded_file = models.FileField(upload_to="statements/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    raw_text = models.TextField(blank=True)  # OCR output

    def __str__(self):
        return f"Statement {self.id} by {self.user.email}"
