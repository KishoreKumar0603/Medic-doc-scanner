from django.urls import path
from .views import DocumentOCRView

urlpatterns = [
    path('upload/', DocumentOCRView.as_view(), name='upload_document'),
]
