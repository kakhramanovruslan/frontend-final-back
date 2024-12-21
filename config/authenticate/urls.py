from django.urls import path

from .views import *


urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path('sign-up/', UserRegisterView.as_view(), name='sign-up'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('verify-email/', UserVerifyEmailView.as_view(), name='verify-email'),
    path('send-reset-password-code/', SendResetPasswordCodeView.as_view(), name='send-reset-password-code'),
    path('check-reset-password-code/', CheckResetPasswordCodeView.as_view(), name='check-reset-password-code'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),

    path('get-user-list', UserListView.as_view(), name='get-user-list'),

    path('get-profile-info', ProfileInfoView.as_view(), name='get-profile-info'),
    path('update-profile-info', ProfileInfoUpdateView.as_view(), name='update-profile-info'),
]
