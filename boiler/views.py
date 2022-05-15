import datetime

from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from .serializers import BoilerSerializer, BoilerModeUpdateSerializer, BoilerAddOrderSerializer, \
    BoilerUpdateOrderProgress, BoilerRetrieveSerializer
from .models import Boiler
from .constants import MAKING_TIME


# Create your views here.


class BoilersListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoilerSerializer

    def get_queryset(self):
        return Boiler.objects.all()


class BoilerUpdateModeView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoilerModeUpdateSerializer

    def get_queryset(self):
        return Boiler.objects.all()


class BoilerAddOrderView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoilerAddOrderSerializer

    def get_queryset(self):
        return Boiler.objects.all()

    def perform_update(self, serializer):
        time_ending = datetime.datetime.now() + datetime.timedelta(milliseconds=MAKING_TIME)
        status = "IN_PROGRESS"
        serializer.save(ending_time_of_iteration=time_ending, status=status)


class BoilerUpdateIfManual(generics.UpdateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = BoilerUpdateOrderProgress

    def get_queryset(self):
        return Boiler.objects.all()

    def perform_update(self, serializer):
        pk = self.kwargs.get('pk')
        boiler = self.get_queryset().get(pk=pk)
        engine_voltage = serializer.validated_data.get('engine_voltage')
        print(boiler, engine_voltage)
        if boiler.mode == "MANUAL" and engine_voltage > 0 and boiler.status == "IN_PROGRESS":
            serializer.save()
        else:
            raise PermissionDenied(detail='boiler not in working mode or sent not valid prams', code=403)


class BoilerRetrieveView(generics.RetrieveAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = BoilerRetrieveSerializer

    def get_queryset(self):
        return Boiler.objects.all()
