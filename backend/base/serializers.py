from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only = True)
    _id = serializers.SerializerMethodField(read_only = True)
    isAdmin = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = User
        fields = ['_id', 'username', 'email', 'name', 'isAdmin']

    def get_isAdmin(self, obj):
        # is_staff is an inbuilt django function we're just changing the name to isAdmin
        return obj.is_staff

    def get__id(self, obj):
        return obj.id

    # self is the serializer itself and obj is the user
    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name

# this will be used when a user resets the account or when the user first registers
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = User
        fields = ['_id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        #  refresh token won't be able to authnticate that's why we need access token
        return str(token.access_token)
        




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        #this class will takr two things -> model to be serialized -> data to be rendered
        model = Product
        fields = '__all__' # this will rendeer everuthing inside the product model