from django.urls import path
from .views import OrderListView, OrderCreateView

urlpatterns = [
    path('', OrderListView.as_view()),
    path('create/', OrderCreateView.as_view())
]
