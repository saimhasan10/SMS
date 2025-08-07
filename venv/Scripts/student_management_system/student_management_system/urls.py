
from django.contrib import admin
from django.urls import path, include
from students import views as students_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students/', include('students.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('',students_views.home, name='home'),
]
