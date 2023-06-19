from django.urls import path
from .views import check_porno, dong
urlpatterns = [
    path('/<str:movie_name>/', check_porno()),
    path('test/', dong())
]