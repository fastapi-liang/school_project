"""
URL configuration for school_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path


from .views import StudentsByClassView, StudentByNameView, StudentCreateView, StudentUpdateView,fake_data

urlpatterns = [
    path('students/by_class/', StudentsByClassView.as_view(), name='students_by_class'),
    path('students/by_name/', StudentByNameView.as_view(), name='student_by_name'),
    path('students/', StudentCreateView.as_view(), name='student_create'),
    path('students/<int:pk>/', StudentUpdateView.as_view(), name='student_update'),
    path('test/', fake_data),

]
# pip install djangorestframework==3.14.0