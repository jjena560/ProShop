from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
# isAdminUser basically tells if the user is a isStaff member where isStaff = True
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProductSerializer, UserSerializer, UserSerializerWithToken
from .products import products
from .models import Product
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # we;'re overwriting the validate method and we're serializing more data
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        # this is shown in '/api/users/login/
        for k,v in serializer.items():
            data[k] = v

    # this return validate data 
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    # this serializer class returns the user data
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            # make password takes the string version of the pass and hashes it
            password=make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    # request.user cannot find the user even though technicall we're logged in our admin panel becuase we're using DRAPI
    #authentication and we're looking for a token rather than the default authentication sysytem
    #because in settings.py we configured the authentication class to use the JSON web token
    user = request.user
    # using with token because we need a new token after the modification
    serializer = UserSerializerWithToken(user, many=False) #many means more than one objects

    data = request.data
    # now the modifications
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']

    if(data['password'] != ''):
        user.password = make_password(data['password'])

    user.save()
    
    return Response(serializer.data)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    # request.user cannot find the user even though technicall we're logged in our admin panel becuase we're using DRAPI
    #authentication and we're looking for a token rather than the default authentication sysytem
    #because in settings.py we configured the authentication class to use the JSON web token
    user = request.user
    serializer = UserSerializer(user, many=False) #many means more than one objects
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


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
    
    