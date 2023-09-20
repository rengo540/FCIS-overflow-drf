
from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Answer, Course, Level, Question,UploadedFile
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
        

class FileSerializer (serializers.ModelSerializer):
    class Meta:
        model=UploadedFile
        fields=['attached_file']



class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField()
    course = serializers.SlugRelatedField(queryset=Course.objects.all(),slug_field='name')
    level = serializers.SlugRelatedField(queryset=Level.objects.all(),slug_field='name')
    answers_list = serializers.HyperlinkedIdentityField(view_name='questions:answer-question-list',lookup_field='slug')
    upload_files = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)
    files = FileSerializer(many=True,read_only=True)

    class Meta:
        model=Question
        fields=['user','course','level','title','slug','content','timestamp','voteUp','voteDown','answers_list','upload_files','files']
        read_only_fields = ['voteUp','voteDown','timestamp','slug']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        # Handle multiple uploaded files
        uploaded_files = self.context['request'].FILES.getlist('upload_files')
        if 'upload_files' in validated_data:
            validated_data.pop('upload_files')
        question = super().create(validated_data)

        # Create UploadedFile instances for each uploaded file
        for uploaded_file in uploaded_files:
            UploadedFile.objects.create(attached_file=uploaded_file, question=question)

        return question
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Answer
        fields=['id','user','question','content','timestamp','voteUp','voteDown']
        read_only_fields=['timestamp','voteUp','voteDown','user','question']
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user     
        question_slug=self.context['kwargs']['slug']
        question = Question.objects.get(slug=question_slug)
        validated_data['question']=question
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data['user'] = instance.user     
        
        question = Question.objects.get(pk=instance.question.id)
        print(question)
        validated_data['question']=question
        print('heeeereeee')
        return super().update(instance, validated_data)
    
    
class AnswerVoteSerilaizer(serializers.ModelSerializer):
    class Meta:
        model=Answer
        fields=['id','user','question','content','timestamp','voteUp','voteDown']
        read_only_fields=['timestamp','user','content','question']
        
    def update(self, instance, validated_data):
        validated_data['user'] = instance.user     
        
        question = Question.objects.get(pk=instance.question.id)
        print(question)
        validated_data['question']=question
        return super().update(instance, validated_data)