from django.urls import path
from .views import (fill_db, getRestaurants, postRestaurant,
                    updateRestaurant, deleteRestaurant)

app_name = 'restaurants'

urlpatterns = [
    path('fill-db/', fill_db, name='fill_db'),
    path('', getRestaurants, name='getRestaurants'),
    path('post-restaurant/', postRestaurant, name='postRestaurant'),
    path('update-restaurant/<str:id>', updateRestaurant, name='updateRestaurant'),
    path('delete-restaurant/<str:id>', deleteRestaurant, name='deleteRestaurant'),
]
