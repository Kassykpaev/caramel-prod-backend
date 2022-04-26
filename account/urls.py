from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from account.views import EmailTokenObtainPairView, SendPasswordResetEmailView, UserChangePasswordView, UserProfileView, UserRegistrationView, UserPasswordResetView, UserRequestView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    # path('login/', UserLoginView.as_view(), name='login'),
    path('login/', EmailTokenObtainPairView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(),
         name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/',
         UserPasswordResetView.as_view(), name='reset-password'),
    path('forms/', UserRequestView.as_view(), name='forms'),
]
