from django.urls import path
from . import views
from rest_framework import routers 

app_name='questions'

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'levels',views.LevelViewSet,basename='level')
router.register(r'courses',views.CourseViewSet,basename='course')
router.register(r'questions',views.QuestionViewSet,basename='question')

urlpatterns = [
    
]

urlpatterns += router.urls