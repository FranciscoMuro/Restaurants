# Utils
from math import fabs
import pandas as pd
# Decorators
from django.views.decorators.csrf import csrf_exempt
# Json
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
# Models
from .models import restaurant
# Serializers
from .serializers import restaurant_serializer

# We use pandas to read the csv
@csrf_exempt
def fill_db(request):
    # here we see if we have the right file
    csvFile = request.FILES['restaurants']
    if not csvFile.name.endswith('.csv'):
        return JsonResponse('The file selected is not a csv file', safe=False)
    # Read the csv file with pandas an turn it into a data frame to get the values of the csv
    restaurantCsv = pd.read_csv(csvFile)
    restaurantDf = pd.DataFrame(restaurantCsv)
    for restaurantIterator in restaurantDf.itertuples():
        # Here we make an iteration of the data frame and turn it into a restaurant object to save it in the db.
        restaurantModel = restaurant(
            id=restaurantIterator.id,
            rating=restaurantIterator.rating,
            name=restaurantIterator.name,
            site=restaurantIterator.site,
            email=restaurantIterator.email,
            phone=restaurantIterator.phone,
            street=restaurantIterator.street,
            city=restaurantIterator.city,
            state=restaurantIterator.state,
            lat=restaurantIterator.lat,
            lng=restaurantIterator.lng,
        )
        restaurantModel.save()
    return JsonResponse('CSV has been read correctly', safe=False)


# This function is to get all the restaurants
# GET
@csrf_exempt
def getRestaurants(request):
    restaurants = restaurant.objects.all()
    processedRestaurants = restaurant_serializer(restaurants, many=True)
    return JsonResponse(processedRestaurants.data, safe=False)

# This function is to add a new restaurant
# POST
@csrf_exempt
def postRestaurant(request):
    newRestaurant = JSONParser().parse(request)
    processedRestaurant = restaurant_serializer(data=newRestaurant)
    if processedRestaurant.is_valid():
        processedRestaurant.save()
        return JsonResponse('The new restaurant was added successfully', safe=False)
    return JsonResponse('Something went wrong creating a new restaurant', safe=False)

# This function is to update a restaurant
# PUT
# id = is the parameter that we are going to use to get the restaurant that we gonna update
@csrf_exempt
def updateRestaurant(request, id):
    newRestaurantData = JSONParser().parse(request)
    # Here we used the objects get to search the restaurant with the id
    restaurantToUpdate = restaurant.objects.get(id=id)
    processedRestaurant = restaurant_serializer(restaurantToUpdate, data=newRestaurantData)
    if processedRestaurant.is_valid():
        processedRestaurant.save()
        return JsonResponse('The new data for the restaurant was added successfully', safe=False)
    return JsonResponse('Something went wrong updating the restaurant with id='+id, safe=False)

# This function is to delete a restaurant
# DELETE
# id = is the parameter that we are going to use to get the restaurant that we gonna delete
@csrf_exempt
def deleteRestaurant(request, id):
    # Here we used the objects get to search the restaurant with the id
    restaurantToUpdate = restaurant.objects.get(id=id)
    restaurantToUpdate.delete()
    return JsonResponse('The restaurant was deleted successfully with id='+id, safe=False)

