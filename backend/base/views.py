from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
# isAdminUser basically tells if the user is a isStaff member where isStaff = True
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProductSerializer, UserSerializer, UserSerializerWithToken, OrderSerializer
from .products import products
from .models import Product, Order, OrderItem, ShippingAddress, Review
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import status 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSlidingSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import datetime


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

    if data['password'] != '':
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
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = User.objects.get(id = pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request, pk):
    
    user = User.objects.get(id = pk)
     

    data = request.data
    # now the modifications
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.is_staff = data['isAdmin']


    user.save()
    serializer = UserSerializer(user, many=False)
    
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    userForDeletion = User.objects.get(id = pk)
    userForDeletion.delete()
    return Response("user was deleted")


@api_view(['GET'])
# #the response will only work if you have this decorator before the function
def getProducts(request):
    # if a user search an item, its gonna get the param by keyword so anything keyword= 
    query = request.query_params.get('keyword')

    if query == None:
        query = ''
    #  this means if the any part of product name contains the query 
    # i in icontains means no case sensititive
    products = Product.objects.filter(name__icontains = query).order_by('-createdAt')

    # Pagination 
    # now we want to paginate the filtered data
    page  = request.query_params.get('page') # this will store the page we want to see

    paginator = Paginator(products, 4) # takes in the query set to be paginated and the numer of products to be showed in a single page
    # now on every page we have two products

    

    try:
        products = paginator.page(page) #this will open the page given and render those two products
    except PageNotAnInteger:
        products = paginator.page(1) # first page
    except EmptyPage:
        products = paginator.page(paginator.num_pages) #last page

    if page == None:
        page = 1
    
    
    # sometimes the frontend passes the page as string
    page = int(page)
        

    serializer = ProductSerializer(products, many=True) #many means more than one objects
    return Response({'products': serializer.data, 'page':page, 'pages': paginator.num_pages})


@api_view(['GET'])
def getTopProducts(request):
    products = Product.objects.filter(rating__gte=4).order_by('-rating')[0:5]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET']) 
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many= False) #many means more than one objects
    return Response(serializer.data)


@api_view(['POST']) 
@permission_classes([IsAdminUser])
def createProduct(request):
    user = request.user
    product = Product.objects.create(
        user = user,
        name = 'sample_name',
        price = 0,
        brand = 'apple',
        countInStock = 0,
        category = 'sample category',
        description = ''
        )
    
    serializer = ProductSerializer(product, many= False)
    # returning the product data and this is gonna fill out the form
    return Response(serializer.data)



@api_view(['PUT']) 
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    data = request.data
    product = Product.objects.get(_id=pk)
    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.countInStock = data['countInStock']
    product.category = data['category']
    product.description = data['description']

    product.save()

    serializer = ProductSerializer(product, many= False) #many means more than one objects
    return Response(serializer.data)


@api_view(['DELETE']) 
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    productToBeDeleted = Product.objects.get(_id=pk)
    productToBeDeleted.delete() 
    return Response("Product was deleted")


@api_view(['POST']) 
@permission_classes([IsAdminUser])
def uploadImage(request):
    data = request.data
    product_id = data['product_id']
    product = Product.objects.get(_id = product_id)

    # this will get the image that is being send from the frontend
    product.image = request.FILES.get('image')

    product.save()
    return Response("Image Uploaded")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    user = request.user
    product = Product.objects.get(_id=pk)
    data = request.data

    # 1 - Review already exists
    alreadyExists = product.review_set.filter(user=user).exists()
    if alreadyExists:
        content = {'detail': 'Product already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 2 - No Rating or 0
    elif data['rating'] == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 3 - Create review
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment'],
        )

        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        product.rating = total / len(reviews)
        product.save()

        return Response('Review Added')



    




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data

    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:

        # (1) Create order by using the Order model

        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice']
        )

        # (2) Create shipping address using the Shipping Model

        shipping = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country'],
        )

        # (3) Create order items and set order to orderItem relationship
        for i in orderItems:
            # i is the single orderItem and product is its id => "i['product]"
            product = Product.objects.get(_id=i['product'])

            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i['qty'],
                price=i['price'],
                image=product.image.url,
            )

            # (4) Update stock

            product.countInStock -= item.qty
            product.save()

        # this will be serialized and the order will be passed as obj
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])    
def getMyOrders(request):
    user = request.user
    # this is gonna get all the child objects 
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many = True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAdminUser])    
def getOrders(request): 
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many = True)
    return Response(serializer.data)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):

    user = request.user

    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response({'detail': 'Not authorized to view this order'},
                     status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    order = Order.objects.get(_id=pk)

    order.isPaid = True
    order.paidAt = datetime.now()
    order.save()

    return Response('Order was paid')


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request, pk):
    order = Order.objects.get(_id=pk)

    order.isDelivered = True
    order.deliveredAt = datetime.now()
    order.save()

    return Response('Order was delivered')


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request, pk):
    order = Order.objects.get(_id=pk)

    order.isDelivered = True
    order.deliveredAt = datetime.now()
    order.save()

    return Response('Order was delivered')
