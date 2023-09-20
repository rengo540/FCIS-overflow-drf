from django.forms import model_to_dict
from django.shortcuts import render
from django.db import IntegrityError
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.decorators import action
from rest_framework import status,response,generics,renderers,viewsets
from rest_framework.permissions import SAFE_METHODS,IsAuthenticated,IsAdminUser
from .permissions import UserWhoRequestCanPost ,AdminOnlyCanPost,OwnerNotAllowed
from authentication.models import User
from .serializers import  AnswerSerializer, AnswerVoteSerilaizer, CourseSerializer, LevelSerializer, QuestionSerializer
from django_filters.rest_framework import DjangoFilterBackend,filters
from .models import  Answer, Course, Level, Question
from rest_framework import status
# Create your views here.

class QuestionViewSet(viewsets.ModelViewSet):
    queryset =Question.objects.all() 
    serializer_class=QuestionSerializer
    permission_classes=(IsAuthenticated,UserWhoRequestCanPost)
    lookup_field='slug'
    lookup_url_kwarg='slug'
    #filter_backends=[DjangoFilterBackend] because it in the project level(settings)
    filterset_fields=['level__name','course__name']
    ordering_fields=['voteUp','vouteDown','timestamp']
    search_fields=['title','content']
    
    @action(detail=True,methods=['POST']
            ,permission_classes=[IsAuthenticated,OwnerNotAllowed]
            ,name='vote-up')
    def vote_up(self,request,slug=None):
        try:
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
            question = self.get_object()
        except Question.DoesNotExist :
            return response.Response({'error':'question not found'},status=status.HTTP_404_NOT_FOUND)

        question.voteDown += 1 
        question.save()
        return response.Response({'message':'voted down successfully'},status=200)

    # @action(detail=True
    #         ,methods=['GET','POST']
    #         ,permission_classes=[IsAuthenticated]
    #         ,name='answers'
    #         )
    # def answers(self,request,slug=None):
    #     if request.method =='GET':
    #         answers_list = Answer.objects.filter(question__slug=slug)
    #         serilaizer = AnswerSerializer(answers_list,many=True)
    #         return response.Response(serilaizer.data,status=status.HTTP_200_OK)
    #     else:
    #         serilaizer = AnswerSerializer(data=request.data)
    #         serilaizer.is_valid(raise_exception=True)
    #         serilaizer.save()
    #         return response.Response(serilaizer.data,status=status.HTTP_201_CREATED)
        
class AnswersApi(generics.ListCreateAPIView):
    serializer_class=AnswerSerializer
    ordering_fields=['voteUp','vouteDown','timestamp']
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        question = Question.objects.get(slug=self.kwargs['slug'])
        return Answer.objects.filter(question=question)
    def get_serializer_context(self):
        return {'request':self.request,
                'kwargs':self.kwargs}
        
    # def get_permissions(self):
    #     if self.action=='list' or self.action=="create":
    #         permission_classes=[IsAuthenticated]
    #     elif self.action=='update' or self.action=='retrieve':
    #         permission_classes=[IsAuthenticated,UserWhoRequestCanPost]
    #     elif self.action=='partial_updata':
    #         permission_classes=[IsAuthenticated,OwnerNotAllowed]
            
    #     return permission_classes

class AnswersDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=AnswerSerializer
    permission_classes=[IsAuthenticated,UserWhoRequestCanPost]
    queryset=Answer.objects.all()
    
    def get_serializer_context(self):
        return {'request':self.request,
                'kwargs':self.kwargs}

class AnswersVoteUp(generics.UpdateAPIView):
    serializer_class=AnswerVoteSerilaizer
    permission_classes=[IsAuthenticated,OwnerNotAllowed]
    queryset=Answer.objects.all()
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        voteUp = instance.voteUp + 1
        serializer = self.get_serializer(instance, data={'voteUp':voteUp}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)

class AnswersVoteDown(generics.UpdateAPIView):
    serializer_class=AnswerVoteSerilaizer
    permission_classes=[IsAuthenticated,OwnerNotAllowed]
    queryset=Answer.objects.all()
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        voteDown = instance.voteDown + 1
        serializer = self.get_serializer(instance, data={'voteDown':voteDown}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)


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
