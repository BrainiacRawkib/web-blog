from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    # path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
