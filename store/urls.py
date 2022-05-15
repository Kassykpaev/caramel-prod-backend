from django.urls import path
from .views import OrderListView, OrderCreateView, AddressCreateListView, AddressRetrieveUpdateDeleteView

urlpatterns = [
    path('orders/', OrderListView.as_view()),
    path('orders/create/', OrderCreateView.as_view()),
    path('addresses/', AddressCreateListView.as_view()),
    path('addresses/<int:pk>', AddressRetrieveUpdateDeleteView.as_view())
]
