from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    # Maps the root path of the app (e.g., /exams/) to the list view
    path('', views.exam_list, name='exam_list'),
]