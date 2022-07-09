# Utils
import math
import pandas as pd
from restaurants.point import Point
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
    processedRestaurant = restaurant_serializer(
        restaurantToUpdate, data=newRestaurantData)
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


# This function get the statistics for the restaurants
# GET
# latitudeParam = latitude of the origin point
# longitudeParam = longitude of the origin point
# radiusParam = radius of the origin point
@csrf_exempt
def getStatistics(request, latitudeParam, longitudeParam, radiusParam):
    # we parse the parameters to a float value to make the calculations
    latitude = float(latitudeParam)
    longitude = float(longitudeParam)
    radius = float(radiusParam)
    # declare the variables that are going to store the values
    countRestaurants = 0
    countRating = 0
    dstRestaurant = []
    # get the restaurants values from the data base
    restaurants = restaurant.objects.all()
    # here convert the values of the coordinates to radians to work with them
    radiants = degToRadians(latitude, longitude)
    # Here we call the object point to store th values of the coordinates
    originPoint = Point(radiants[0], radiants[1])
    # We iterate the restaurants of the db
    for res in restaurants:
        # here we convert to radians of the destiny point and make the new object for that
        radiants = degToRadians(res.lat, res.lng)
        destinyPoint = Point(radiants[0], radiants[1])
        distance = getDistance(originPoint, destinyPoint)
        print(distance)\
        # here we check if the distance is less than radius if it is less we add a new restaurant to those ones are close to the origin
        if (distance <= radius):
            countRestaurants += 1
            countRating += res.rating
            dstRestaurant.append(res.rating)

    frameRestaurant = pd.DataFrame(dstRestaurant)
    stdRating = frameRestaurant.std()[0]
    averageRating = countRating/countRestaurants
    # return the calculations
    response = {
        "count": countRestaurants,
        "avg": averageRating,
        "std": stdRating,
    }
    return JsonResponse(response, safe=False)

# originPint = this is the origin pont how is the center of the circle
# destinyPint = this is the  point to calculate de distance within the origin point
# also here is used the distance formula of two points
def getDistance(originPoint, destinyPoint):
    originSinLatitude = math.sin(originPoint.getLatitude())
    originCosLatitude = math.cos(originPoint.getLatitude())
    destinySinLatitude = math.sin(destinyPoint.getLatitude())
    destinyCosLatitude = math.cos(destinyPoint.getLatitude())
    # this is the cos of the destiny longitude point minus origin longitude point
    cosDLongMinusOLong = math.cos(
        destinyPoint.getLongitude() - originPoint.getLongitude())
    distance = 3963.0*math.acos((originSinLatitude*destinySinLatitude) +
                                originCosLatitude*destinyCosLatitude*cosDLongMinusOLong)
    return (distance*1.609344)*1000

# here is a function to convert latitude and longitude to radians
def degToRadians(latitude, longitude):
    convertedLatitude = latitude / (180/math.pi)
    convertedLongitude = longitude / (180/math.pi)
    return [convertedLatitude, convertedLongitude]
