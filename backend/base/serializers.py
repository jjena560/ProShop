from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, Order, OrderItem, ShippingAddress

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
    # this will give us an empty token field which wecan fll by get_toke method
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



class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only = True)
    user = serializers.SerializerMethodField(read_only = True)
    shippingAddress = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Order
        fields = '__all__'

    #  obj is that order object
    def get_orderItems(self, obj):
        item = obj.orderitem_set.all()
        serializer = OrderItemSerializer(item, many = True)
        return serializer.data

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many = False)
        return serializer.data

    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(obj.shippingAddres, many = False)
        except:
            address = False
        return address

