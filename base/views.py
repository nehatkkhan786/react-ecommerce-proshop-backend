from itertools import product
from unicodedata import category
from urllib import response
from django.shortcuts import render
from .models import Product, Order, ShippingAddress, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from .serializers import ProductSerializers,UserSerializers, UserSerializersWithToken, OrderSerializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import  status

# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self,attrs):
        data = super().validate(attrs)
        serializer = UserSerializersWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializers = ProductSerializers(products, many=True)
    return Response(serializers.data)

@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializers = ProductSerializers(product)
    return Response(serializers.data)

@api_view(['POST'])
def RegisterUser(request): 
    try:

        data = request.data
        user = User.objects.create(
            first_name = data['name'],
            username = data['email'],
            email = data['email'],
            password = make_password(data['password'])
        )
        serializer = UserSerializersWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail' 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializers(user, many=False)
    return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request):
    user = request.user
    serializer = UserSerializersWithToken(user, many=False)
    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])
    user.save()
    return Response(serializer.data)
    

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializers(users, many=True) 
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createOrder(request):
    user = request.user
    data = request.data

    orderItems = data['orderItems']
    if orderItems and len(orderItems) ==0:
        return Response({'message':'No Order Items'}, status=status.HTTP_400_BAD_REQUEST) 
    else:
        # Create an Order
        order = Order.objects.create(
            user= user,
            payment_method= data['paymentMethod'],
            taxPrice = data['taxPrice'],
            shippingPrice = data['shippingPrice'],
            totalPrice = data['totalPrice']
        )

        # Create Shipping Address
        shippingAddress = ShippingAddress.objects.create(
            order = order,
            address = data['shippingAddress']['address'],
            state = data['shippingAddress']['state'],
            city = data['shippingAddress']['city'],
            pincode = data['shippingAddress']['pincode'],
            phone = data['shippingAddress']['phone']
        )

        # Create Order Items and set the order to orderItem relationship

        for i in orderItems:
            product = Product.objects.get(_id=i['product'])

            item = OrderItem.objects.create(
                product=product,
                order=order,
                name= product.name,
                qty = i['qty'],
                price = i['price'],
                image= product.image.url,
            )
            # Update the stock of the product
            product.countInStock -= int(item.qty)
            product.save()

        # Serialize the data and send it in response
        serializer = OrderSerializers(order, many=False )
        return Response(serializer.data)




# Get all the orders of a user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    order = user.order_set.all()
    serializer = OrderSerializers(order, many=True)
    return Response(serializer.data)


# Get a single order by user 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    user = request.user
    order = Order.objects.get(_id=pk)
    try:
        if user.is_staff or order.user == user:
            serializer = OrderSerializers(order, many=False)
            return Response(serializer.data)
        else:
            return Response({'message':'Not authorized to view this order'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'message':'Order Not Found'}, status= status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    product = Product.objects.get(_id=pk )
    product.delete()
    return Response({'message':'Product Deleted successfully'})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    user = request.user
    data = request.data
    product = Product.objects.create(
        user=user,
        name=data['name'],
        image=data['image'],
        brand=data['brand'],
        category= data['category'],
        description=data['description'],
        price=data['price'],
        countInStock=data['countInStock']
    )
    product.save()
    serializer = ProductSerializers(product, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def editProduct(request, pk):
    data = request.data
    product = Product.objects.get(_id=pk)
    product.name = data['name']
    product.image = data['image']
    product.brand = data['brand']
    product.category = data['category']
    product.price = data['price']
    product.countInStock = data['countInStock']
    product.save()
    serializer = ProductSerializers(product, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)




