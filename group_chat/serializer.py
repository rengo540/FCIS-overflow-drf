

from .models import Group, Membership
from rest_framework import serializers


class GroupSerilaizer (serializers.ModelSerializer):
    class Meta:
        model=Group
        fields=['name','slug']
        read_only_fields=['slug']
        
    def create(self, validated_data):
        user=self.context['request'].user
        validated_data['member']=[user]
        #validated_data['is_admin']=True
        group =super().create(validated_data)
        Membership.objects.create(person=user,group=group,is_admin=True)        
        return group