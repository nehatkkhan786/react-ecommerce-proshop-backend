from os import access
from rest_framework import serializers
from .models import Product, Order, OrderItem, ShippingAddress
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializers(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only= True)
    isAdmin = serializers.SerializerMethodField(read_only= True)


    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'first_name', 'last_name', 'email', 'name', 'isAdmin']

    def get_name(self, obj):
        name = obj.first_name
        if name == "":
            name = obj.email
        return name
    
    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff


class UserSerializersWithToken(UserSerializers):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'first_name', 'last_name', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)



class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ShippingAddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'

class OrderItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializers(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    users = serializers.SerializerMethodField(read_only= True)

    class Meta:
        model = Order
        fields = '__all__'
    
    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializer =OrderItemSerializers(items, many=True)
        return serializer.data

    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializers(obj.shippingaddress, many=False).data
        except:
            address = False    
        return address

    def get_users(self, obj):
        user = obj.user
        serializer = UserSerializers(user, many=False)
        return serializer.data





