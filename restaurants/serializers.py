from rest_framework import serializers
from .models import restaurant


class restaurant_serializer(serializers.ModelSerializer):
    class Meta:
        model = restaurant
        fields = (
            'id',
            'rating',
            'name',
            'site',
            'email',
            'phone',
            'street',
            'city',
            'state',
            'lat',
            'lng',
        )
