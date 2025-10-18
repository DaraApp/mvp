from django.urls import path
from . import views

urlpatterns = [
    path('pharmacy-item/', views.PharmacyItemView.as_view(), name='pharmacy-item'),
]
