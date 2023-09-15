from django.conf import settings
from django.test import TestCase
import jwt
from rest_framework.test import APITestCase
from django.urls import reverse

from .models import User
# Create your tests here.


class TestAuthentication(APITestCase):
    
    def setUp(self):
            self.register_url = reverse('auth:register')
            self.login_url = reverse('auth:login')

            self.user_data = {
                'email': 'ar6029676@gmail.com',
                'username': 'ar6029676',
                'password': 'ararar6029676',
                're_password':'ararar6029676'
            }

            return super().setUp()


    def test_register_without_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code,400)
        
    def test_register_successfully(self):
        res = self.client.post(self.register_url,data=self.user_data,format='json')
        self.assertEqual(res.data['user']['username'],self.user_data['username'])
        self.assertEqual(res.status_code,201)
        
    def test_login_with_unverified_email(self):
        self.client.post(self.register_url,data=self.user_data,format='json')
        res = self.client.post(path=self.login_url,data=self.user_data,format='json')
        self.assertEqual(res.status_code,401)
        
    def test_login_with_verified_email(self):
        response = self.client.post(self.register_url,data=self.user_data,format='json')
        username = response.data['user']['username']
        user = User.objects.get(username=username)
        user.is_verified = True
        user.save()
        res = self.client.post(path=self.login_url,data=self.user_data,format='json')
        #test token = user 
        token = res.data['access']
        payload = jwt.decode(token, settings.SECRET_KEY,algorithms=['HS256'])
        user_token = User.objects.get(id=payload['user_id'])
        
        self.assertEqual(user.username,user_token.username)
        self.assertEqual(res.status_code,200)

        