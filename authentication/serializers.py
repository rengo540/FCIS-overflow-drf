from rest_framework import serializers
from .models import User


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
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']