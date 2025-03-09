from django.db import models
from django.contrib.auth.models import User  # Import the User model

class UploadedPDF(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Add this line
    file = models.FileField(upload_to='pdfs/')
    language = models.CharField(max_length=50)
    audio_file = models.FileField(upload_to='audios/', blank=True, null=True)
    text_file = models.FileField(upload_to='texts/', blank=True, null=True)