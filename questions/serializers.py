
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Course, Level, Question
#import bleach





class LevelSerializer (serializers.ModelSerializer):
    class Meta:
        model=Level
        fields='__all__'
        
        
class CourseSerializer(serializers.ModelSerializer):
    level= serializers.SlugRelatedField(queryset=Level.objects.all(),
                                        slug_field='name')
    class Meta:
        model=Course
        fields=['name','level']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']



class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    course = serializers.SlugRelatedField(queryset=Course.objects.all(),slug_field='name')
    level = serializers.SlugRelatedField(queryset=Level.objects.all(),slug_field='name')
    
    class Meta:
        model=Question
        fields=['user','course','level','title','slug','content','timestamp','voteUp','voteDown']
        read_only_fields = ['voteUp','voteDown','timestamp','slug']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user     
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)