from django.urls import path
from .views import BoilersListView, BoilerUpdateModeView, BoilerAddOrderView, BoilerUpdateIfManual, BoilerRetrieveView

urlpatterns = [
    path('', BoilersListView.as_view()),
    path('<int:pk>/update-mode/', BoilerUpdateModeView.as_view()),
    path('<int:pk>/add-order/', BoilerAddOrderView.as_view()),
    path('<int:pk>/update-order/', BoilerUpdateIfManual.as_view()),
    path('<int:pk>/', BoilerRetrieveView.as_view())
]
