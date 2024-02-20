
from django import forms
from .models import FileUpload, AudioUpload

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['description', 'file']

class AudioUploadForm(forms.ModelForm):
    class Meta:
        model = AudioUpload
        fields = ['description', 'file']