from django.urls import path
from . import views


urlpatterns = [
    path('getdatabaseinfo/', views.CheckDatabaseUpdateInfo.as_view(), name="getdatabaseinfo"),
    path('getnamelist/', views.GetNamelist_ccs.as_view(), name="getnamelist"),
    path('getcircleid/', views.GetCircleId.as_view(), name="getcircleid"),
    path('randsearchexample/', views.RandSearchExample.as_view(),name="randsearchexample"),
    path('', views.WoxramSearchAPI.as_view(), name="WoxramSearchAPI"),
]