from django.urls import path
from . import views

urlpatterns = [path("", views.home, name="home"),
               path("choice", views.choice, name="choice"),
               path("audio", views.audio, name="audio"),
               path("upload", views.upload, name="upload"),
               path("filelist", views.file_list, name="Filelist"),
               path("readfile", views.read_file, name="Readfile"),
]