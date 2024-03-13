from django.contrib import admin
from .models import UploadedPDF


@admin.register(UploadedPDF)
class UploadedPDFAdmin(admin.ModelAdmin):
    list_display = ('get_file_name', 'language', 'audio_file')

    def get_file_name(self, obj):
        return obj.file.name.split('/')[-1]
    get_file_name.short_description = 'File Name'
