from django.urls import path
from . import views


urlpatterns = [
    path('getdatabaseinfo/', views.CheckDatabaseUpdateInfo.as_view()),
    path('getnamelist/', views.GetNamelist_ccs.as_view()),
    path('getcircleid/', views.GetCircleId.as_view()),
    path('randsearchexample/', views.RandSearchExample.as_view()),
    path('getmaintext/',views.GetMaintext.as_view()),
    path('', views.WoxramSearchAPI.as_view()),
]