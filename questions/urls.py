from django.urls import path
from . import views
from rest_framework import routers 

app_name='questions'

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'levels',views.LevelViewSet,basename='level')
router.register(r'courses',views.CourseViewSet,basename='course')
router.register(r'questions',views.QuestionViewSet,basename='question')
#router.register(r'answers/question',views.AnswersApi,basename='answer')

urlpatterns = [
    path('answers/question/<slug:slug>',views.AnswersApi.as_view(),name='answer-question-list'),
    path('answers/<int:pk>',views.AnswersDetails.as_view(),name='answer-details'),
    path('answers/<int:pk>/vote-up',views.AnswersVoteUp.as_view(),name='answer-voteup'),
    path('answers/<int:pk>/vote-down',views.AnswersVoteDown.as_view(),name='answer-votedown'),
    
]

urlpatterns += router.urls