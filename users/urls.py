from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    # authentication
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    # path('logout/', UserLogoutView.as_view(), name='logout'),

    # register and activate account
    path('register/', RegistrationView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('confirm-email/<uidb64>/<token>/', ActivateAccountView.as_view(), name='confirm-email'),

    # change password
    path('password-change/', ChangePasswordView.as_view(), name='password-change'),
    path('password-change/done/', ChangePasswordDoneView.as_view(), name='password-change-done'),

    # reset password
    path('password-reset/', ResetPasswordView.as_view(), name='password-reset'),
    path('password-reset/done/', ResetPasswordDoneView.as_view(), name='password-reset-done'),
    path('password-reset/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='password-reset-confirm'),
    path('password-reset/complete/', ResetPasswordCompleteView.as_view(), name='password-reset-complete'),
]
