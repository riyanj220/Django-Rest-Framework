from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import *

urlpatterns = [
    path('auth/',obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #api/token is tarha hone chahiye ye paths 
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('',api_home, name  = 'api_home'),
]