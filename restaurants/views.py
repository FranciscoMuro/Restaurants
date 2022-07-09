from django.http import JsonResponse
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from .models import restaurant

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
