from django.db import models

class UploadedPDF(models.Model):
    file = models.FileField(upload_to='pdfs/')
    language = models.CharField(max_length=50)
    audio_file = models.FileField(upload_to='audios/', blank=True, null=True)
    text_file = models.FileField(upload_to='texts/', blank=True, null=True)  # Add a new field for text files
 