from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from .products import products
from .models import Product

# Create your views here.

def getRouter(request):
    return JsonResponse('Hello', safe = False)

@api_view(['GET'])
# #the response will only work if you have this decorator before the function
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True) #many means more than one objects
    return Response(serializer.data)

@api_view(['GET']) 
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many= False) #many means more than one objects
    return Response(serializer.data)
    
    