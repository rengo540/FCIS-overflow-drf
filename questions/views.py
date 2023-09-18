from django.forms import model_to_dict
from django.shortcuts import render
from django.db import IntegrityError
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.decorators import action
from rest_framework import status,response,generics,renderers,viewsets
from rest_framework.permissions import SAFE_METHODS,IsAuthenticated,IsAdminUser
from .permissions import UserWhoRequest ,AdminOnlyCanPost,OwnerNotAllowed
from authentication.models import User
from .serializers import  CourseSerializer, LevelSerializer, QuestionSerializer
from django_filters.rest_framework import DjangoFilterBackend,filters
from .models import  Course, Level, Question
from rest_framework import status
# Create your views here.

class QuestionViewSet(viewsets.ModelViewSet):
    queryset =Question.objects.all() 
    serializer_class=QuestionSerializer
    permission_classes=(IsAuthenticated,UserWhoRequest)
    lookup_field='slug'
    lookup_url_kwarg='slug'
    #filter_backends=[DjangoFilterBackend] because it in the project level(settings)
    filterset_fields=['level__name','course']
    ordering_fields=['voteUp','vouteDown','timestamp']
    search_fields=['title','content']
    
    @action(detail=True,methods=['POST']
            ,permission_classes=[IsAuthenticated,OwnerNotAllowed]
            ,name='vote-up')
    def vote_up(self,request,slug=None):
        try:
            print(slug)
            question = self.get_object()
        except Question.DoesNotExist :
            return response.Response({'error':'question not found'},status=status.HTTP_404_NOT_FOUND)

        question.voteUp += 1 
        question.save()
        return response.Response({'message':'voted up successfully'},status=200)
    
    @action(detail=True,methods=['POST']
            ,permission_classes=[IsAuthenticated,OwnerNotAllowed]
            ,name='vote-dowm')
    def vote_down(self,request,slug=None):
        try:
            print(slug)
            question = self.get_object()
        except Question.DoesNotExist :
            return response.Response({'error':'question not found'},status=status.HTTP_404_NOT_FOUND)

        question.voteDown += 1 
        question.save()
        return response.Response({'message':'voted down successfully'},status=200)





class LevelViewSet(viewsets.ModelViewSet):
    queryset=Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes=(IsAuthenticated,AdminOnlyCanPost)
    lookup_field= 'name'
    lookup_url_kwarg= 'name'
    
    

class CourseViewSet(viewsets.ModelViewSet):
    queryset=Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes=(IsAuthenticated,AdminOnlyCanPost)
