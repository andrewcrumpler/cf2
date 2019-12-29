from django.urls import path
from . import views

urlpatterns = [
    path("1/individual_cf/", views.IndexView.as_view(), name="index"),
]