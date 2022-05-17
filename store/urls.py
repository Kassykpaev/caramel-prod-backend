from django.urls import path
from .views import OrderListAllView, OrderListView, OrderCreateView, AddressCreateListView, AddressRetrieveUpdateDeleteView, OrderView, get_config_view

urlpatterns = [
    path('config/', get_config_view),
    path('orders/', OrderListView.as_view()),
    path('orders/all/', OrderListAllView.as_view()),
    path('orders/<int:pk>/', OrderView.as_view()),
    path('orders/create/', OrderCreateView.as_view()),
    path('addresses/', AddressCreateListView.as_view()),
    path('addresses/<int:pk>/', AddressRetrieveUpdateDeleteView.as_view())
]
