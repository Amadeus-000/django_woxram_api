from django.urls import path
from . import views


urlpatterns = [
    path('circle/', views.getCircle.as_view()),
    path('cv/', views.getCV.as_view()),
    path('sw/', views.getScenariowriter.as_view()),
    path('voicedata/', views.getVoicedata.as_view()),
    path('searchexample/', views.getSearchExample.as_view()),
    path('memodata/', views.getMemodata.as_view()),
]