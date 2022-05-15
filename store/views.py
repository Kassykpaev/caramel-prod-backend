from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Order, Address, Config
from .serializers import OrderListSerializer, OrderCreateSerializer, AddressSerializer, OrderUpdateSerializer

# Create your views here.


class OrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer

    def get_queryset(self):
        return Order.objects.all()

    def perform_create(self, serializer):
        volume = serializer.validated_data.get('volume')
        address = serializer.validated_data.get('address')
        user = self.request.user
        price_per_unit = Config.objects.first().price_per_unit
        serializer.save(volume=volume, address=address, user=user, price_per_unit=price_per_unit)


class OrderRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        return Order.objects.all()


class OrderUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderUpdateSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class AddressCreateListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class AddressRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
