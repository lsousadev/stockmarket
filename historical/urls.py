from django.urls import path

from . import views

app_name = "historical"
urlpatterns = [
    path("", views.index, name="index"),
    path("study", views.study, name="study")
]