from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit-form/', views.submit_form, name='submit_form'),
    path('download-csv/', views.download_csv, name='download_csv'),
]