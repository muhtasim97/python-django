from django.urls import path
from store import views
from .views import Signup,Login,Index,Cart,logout,Checkout,Orders
urlpatterns=[
    path('',Index.as_view(),name='homepage'),
    path('signup',Signup.as_view(),name='signup'),
    path('login',Login.as_view(),name='login'),
    path('cart',Cart.as_view(),name='cart'),
    path('checkout',Checkout.as_view(),name='checkout'),
     path('orders',Orders.as_view(), name='orders'),
    path('logout',views.logout, name='logout')
]