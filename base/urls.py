from django.urls import path

from .views import deleteProduct, getOrderById, getProducts,getProduct, MyTokenObtainPairView, getUserProfile, getUsers, RegisterUser, updateUser, createOrder, getMyOrders, createProduct,editProduct

urlpatterns = [
    
    path('products/', getProducts),
    path('product/<str:pk>/',getProduct),


    path('users/login/', MyTokenObtainPairView.as_view()),
    path('getusers/', getUsers),
    path('users/profile/', getUserProfile),
    path('users/profile/update/', updateUser),
    path('users/register/', RegisterUser),
    path('myorders/', getMyOrders),

    path('orders/createorder/', createOrder),
    path('order/<int:pk>/', getOrderById),

    # Admin Routes
    path('products/create_product/', createProduct),
    path('deleteproduct/<int:pk>/', deleteProduct),
    path('product/edit/<int:pk>/', editProduct),
]