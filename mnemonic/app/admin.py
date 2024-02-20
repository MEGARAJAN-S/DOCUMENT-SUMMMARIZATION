from django.contrib import admin
from .models import login
from .models import FileUpload,AudioUpload
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('description', 'file', 'uploaded_at')
    list_filter = ('uploaded_at', )
    search_fields = ('description', )

class AudioUploadAdmin(admin.ModelAdmin):
    list_display = ('description', 'file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('description',)
# Register your models here.
admin.site.register(login)
admin.site.register(FileUpload, FileUploadAdmin)
admin.site.register(AudioUpload,AudioUploadAdmin)