from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(write_only=True,
                                        required=True,
                                        )
    class Meta:
        model = User
        fields = ('id','username','email','password','re_password')
        extra_kwargs = {
            'password':{'write_only': True},
            
        }
        
    def validate(self, attrs):
        if not (attrs['password']==attrs['re_password']):
            raise serializers.ValidationError('the two passwords are not equal')
        
        
        return super().validate(attrs)

    def create(self, validated_data):
    
        return User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['email'],
                                        password=validated_data['password'])

# User serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','created_at','section','birthdate','major','profile_pic']
        read_only_fields =['username','email','created_at']
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
        
        
class LoginSerializer(serializers.Serializer):
    username= serializers.CharField(write_only=True,required=True)
    password = serializers.CharField(write_only=True,required=True)
    
    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        
        user = authenticate(username=username,password=password)
        
        if user is None :
            raise AuthenticationFailed(detail='invalid credentials , try again')
        if not user.is_active:
            raise AuthenticationFailed(detail='account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed(detail='this account is not verified')
        
        
        return user.tokens()