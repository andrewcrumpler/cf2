from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("register", include("register.urls")),
    path("projects/", include("projects.urls")),
    path("projects/", include("individual_cf.urls")),
    path('', include("django.contrib.auth.urls"),name='login'),
]
