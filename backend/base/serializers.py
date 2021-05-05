from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        #this class will takr two things -> model to be serialized -> data to be rendered
        model = Product
        fields = '__all__' # this will rendeer everuthing inside the product model