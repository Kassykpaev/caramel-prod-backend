from django.urls import path
from .views import BoilerUpdateIfAuto, BoilersListView, BoilerUpdateModeView, BoilerAddOrderView, BoilerUpdateIfManual,\
    BoilerRetrieveView, BoilerUpdateStatusView

urlpatterns = [
    path('', BoilersListView.as_view()),
    path('<int:pk>/update-mode/', BoilerUpdateModeView.as_view()),
    path('<int:pk>/add-order/', BoilerAddOrderView.as_view()),
    path('<int:pk>/update-order/manual', BoilerUpdateIfManual.as_view()),
    path('<int:pk>/update-order/auto', BoilerUpdateIfAuto.as_view()),
    path('<int:pk>/update-status', BoilerUpdateStatusView.as_view()),
    path('<int:pk>/', BoilerRetrieveView.as_view())
]
