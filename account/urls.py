from django.urls import path
from . import views


urlpatterns = [
    path('getmemoid/', views.GetMemoPublicId.as_view(), name="getmemoid"),
    path('csrf-token/',views.get_csrf_token),
    path('addwork/', views.AddworkForUser.as_view()),
]