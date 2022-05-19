from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, BasePermission

from .models import Order, Address, Config
from .serializers import ConfigSerializer, OrderListSerializer, OrderCreateSerializer, AddressSerializer, OrderUpdateSerializer

# Create your views here.


class OrderListAllView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        return Order.objects.all()


class OrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


def get_config_view(request):

    if request.method == 'GET':
        config = Config.objects.first()
        data = ConfigSerializer(instance=config)
        return JsonResponse(data.data)


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
        total_price = price_per_unit * volume
        serializer.save(volume=volume, address=address,
                        user=user, price_per_unit=price_per_unit, total_price=total_price)


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

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class AddressRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class OrdersListViewWithStatus(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        Order.objects.filter(status="IN_QUEUE")
