from django.urls import path
from .views import FeedbackFormView, SuccessView

urlpatterns = [
    path('send/', FeedbackFormView.as_view(), name='feedback'),
     path('success/', SuccessView.as_view(), name='success'),
]
