from django.shortcuts import get_object_or_404, render
from rest_framework import generics

from .utils import Util
from .serializers import LoginSerializer, ProfileSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle
# Create your views here.



class RegisterApiView(generics.CreateAPIView):
    permission_classes=[AllowAny]
    serializer_class=RegisterSerializer
    throttle_classes=[AnonRateThrottle]
    def create(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        
        #user_data = userr.data
        #user = User.objects.get(username=user_data['username'])
        token = RefreshToken.for_user(user).access_token
        absurl = 'http://'+get_current_site(request).domain+reverse('auth:email-verify')+'?token='+str(token)
        email_body = 'Hi '+ user.username + \
            ' Use the link below to verify your email \n' + absurl
            
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your Account in FCISOverflow'}

        Util.send_email(data)
        return Response({
            "user": UserSerializer(user,context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        },status=status.HTTP_201_CREATED)


class VerifyEmail(generics.RetrieveAPIView):
    
    def retrieve(self, request, *args, **kwargs):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,algorithms=['HS256'])
            print(payload)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)



class Login(generics.CreateAPIView):
    serializer_class = LoginSerializer
    throttle_classes=[AnonRateThrottle,]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_tokens=serializer.save()
        
        return Response(user_tokens,status=status.HTTP_200_OK)
    
    
class Profile(generics.RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    permission_classes=[]
    
    def get_object(self):
        obj=get_object_or_404(User,username=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj