from django.urls import path
from .views import youtube_sentiment

urlpatterns = [
    path('', youtube_sentiment, name='youtube_sentiment'),
]
