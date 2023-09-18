from django.urls import reverse
from rest_framework.test import APITestCase


class SetupTestApi (APITestCase):

    
    def setUp(self) -> None:
        
        
        self.questions_url = reverse('questions:question-list')
        self.question_url = reverse('questions:question-detail',kwargs={'slug': 'default-slug'})
        self.courses_url = reverse('questions:course-list')
        self.levels_url = reverse('questions:level-list')
        self.register_url = reverse('auth:register')

        #frehsman , sophomore , junior , senior ,postgrad
        self.levels_data=[{
            "name":'first',
            "nickname":'frehsman'
        },{
            "name":'second',
            "nickname":'sophomore'
        },{
            "name":'third',
            "nickname":'junior'
        }]
        
        self.courses_data=[{
            'name':'physics',
            'level':'first'
        },
        {
            'name':'english',
            'level':'first'
        },
        {
            'name':'oop',
            'level':'second'
        },]
        
        self.question_data= [{
            'title':'my first question what is',
            'content':'my first question what is ',
            'course':'physics',
            'level':'first'
        },{
            'title':'my second question what is',
            'content':'my second question what is ',
            'course':'physics',
            'level':'first'
        },]
        
        self.user_data = [{
                'email': 'ar6029676@gmail.com',
                'username': 'ar6029676',
                'password': 'ararar6029676',
                're_password':'ararar6029676'
            },{
                'email': 'rengo@gmail.com',
                'username': 'rengo',
                'password': 'ararar6029676',
                're_password':'ararar6029676'
            }
                          ]
        return super().setUp()