from .views import RegisterApiView,VerifyEmail
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'authentication'
urlpatterns = [
    path('register',RegisterApiView.as_view(),name='register'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
