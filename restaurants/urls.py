from django.urls import path
from .views import fill_db

app_name = 'restaurants'

urlpatterns = [
    path('fill-db/', fill_db, name='fill_db'),
]
