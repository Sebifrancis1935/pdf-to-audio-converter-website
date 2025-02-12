from django import forms
from .models import UploadedPDF


class UploadPDFForm(forms.ModelForm):
    class Meta:
        model = UploadedPDF
        fields = ['file', 'language']

class UploadAudioForm(forms.ModelForm):
    class Meta:
        model = UploadedPDF
        fields = ['audio_file', 'language']
