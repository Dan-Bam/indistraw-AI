from django.urls import path
from .views import check_porno
urlpatterns = [
    path('/<str:movie_name>/', check_porno()),
]
