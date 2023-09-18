from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .helpers import create_superuser,create_superuser_and_add_level

from authentication.models import User
from ..models import Course, Level, Question
# Create your tests here.
from .test_setup import SetupTestApi


class TestLevels(SetupTestApi):
    
    def test_create_level_without_authenticate(self):
        res = self.client.post(path=self.levels_url,data=self.levels_data[0],format='json')
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_create_level_without_admin_authenticate(self):
        self.client.post(path=self.register_url,data=self.user_data[0],format='json')
        self.client.login(username='ar6029676',password='ararar6029676')
        res = self.client.post(path=self.levels_url,data=self.levels_data[0],format='json')
        self.assertEqual(res.status_code,status.HTTP_403_FORBIDDEN)
    
    def test_create_level_with_admin_authenticate(self):
        response= user=self.client.post(path=self.register_url,data=self.user_data[1],format='json')
        username = response.data['user']['username']
        user = User.objects.get(username=username)
        user.is_staff = True
        user.save()
        self.client.login(username='rengo',password='ararar6029676')
        res = self.client.post(path=self.levels_url,data=self.levels_data[0],format='json')
        level =Level.objects.get(name='first')
        self.assertEqual(level.name,res.data['name'])
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        
        
    def test_authenticated_user_get_levels(self):
        response= self.client.post(path=self.register_url,data=self.user_data[1],format='json')
        username = response.data['user']['username']
        user = create_superuser(username)
        
        self.client.login(username='rengo',password='ararar6029676')
        res = self.client.post(path=self.levels_url,data=self.levels_data[0],format='json')
        self.client.logout()
        
        
        self.client.post(path=self.register_url,data=self.user_data[0],format='json')
        self.client.login(username='ar6029676',password='ararar6029676')
        
        res = self.client.get(path=self.levels_url,format='json')
        self.assertEqual(res.data['results'][0]['name'],'first')
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def test_unauthenticated_user_get_levels(self):
        self.client.post(path=self.register_url,data=self.user_data,format='json')
        res = self.client.get(path=self.levels_url,format='json')
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


class TestCourse(SetupTestApi):
    
    def test_create_course_without_authenticate(self):
        create_superuser_and_add_level(self)
        self.client.logout()
        
        res = self.client.post(path=self.courses_url,data=self.courses_data[0],format='json')
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_create_course_without_admin_authenticate(self):
        create_superuser_and_add_level(self)
        self.client.logout()
        
        self.client.post(path=self.register_url,data=self.user_data[0],format='json')
        self.client.login(username='ar6029676',password='ararar6029676')
        res = self.client.post(path=self.courses_url,data=self.courses_data[0],format='json')
        self.assertEqual(res.status_code,status.HTTP_403_FORBIDDEN)

    def test_create_course_with_admin_authenticate(self):
        create_superuser_and_add_level(self)
        res = self.client.post(path=self.courses_url,data=self.courses_data[0],format='json')
        
        course =Course.objects.get(name='physics')
        self.assertEqual(course.name,res.data['name'])
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)


    def test_authenticated_user_get_courses(self):
        create_superuser_and_add_level(self)
        res = self.client.post(path=self.courses_url,data=self.courses_data[0],format='json')
        self.client.logout()
        
        self.client.post(path=self.register_url,data=self.user_data[0],format='json')
        self.client.login(username='ar6029676',password='ararar6029676')
        
        res = self.client.get(path=self.courses_url,format='json')
        print(res.data)
        self.assertEqual(res.data['results'][0]['name'],'physics')
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def test_unauthenticated_user_get_levels(self):
        res = self.client.get(path=self.courses_url,format='json')
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)
        
        

class QuestionTest(SetupTestApi):
    
    def test_add_question_by_unathenticated_user(self):
        res=self.client.post(path=self.question_url,data=self.question_data[0],format='json')
        self.assertEqual(res.status_code,status.HTTP_403_FORBIDDEN)
        
    def test_add_question_by_authenticated_user(self):
        create_superuser_and_add_level(self)
        self.client.post(path=self.courses_url,data=self.courses_data[0],format='json')
        self.client.logout()
        
        user = self.client.post(path=self.register_url,data=self.user_data[0],format='json')
        self.client.login(username='ar6029676',password='ararar6029676')
        res = self.client.post(path=self.question_url,data=self.question_data[0],format='json')
        question = Question.objects.get(title=res.data['results'][0]['title'])
        self.assertEqual(question.title,res.data['results'][0]['title'])
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
