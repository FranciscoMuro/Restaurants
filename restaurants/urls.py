from django.urls import path
from .views import (fill_db, getRestaurants, postRestaurant,
                    updateRestaurant, deleteRestaurant, getStatistics)

app_name = 'restaurants'
# Here are stored the url for the endpoints
urlpatterns = [
    path('fill-db/', fill_db, name='fill_db'),
    path('', getRestaurants, name='getRestaurants'),
    path('post-restaurant/', postRestaurant, name='postRestaurant'),
    path('update-restaurant/<str:id>', updateRestaurant, name='updateRestaurant'),
    path('delete-restaurant/<str:id>', deleteRestaurant, name='deleteRestaurant'),
    path('statistics/<str:latitudeParam>/<str:longitudeParam>/<str:radiusParam>', getStatistics, name='getStatistics'),
]
