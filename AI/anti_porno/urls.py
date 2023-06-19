from django.urls import path
from .views import check_porno
urlpatterns = [
    path('', check_porno),
    #path('test/', dong)
]