from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from rest_framework import status,response,generics,renderers,viewsets
from rest_framework.permissions import IsAuthenticated

from authentication.models import User
from .models import Group, Membership
from rest_framework.decorators import action

from .serializer import GroupSerilaizer
from .permssions import IsAdminOfGroupToEdit
# Create your views here.
# chat/views.py


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class=GroupSerilaizer
    permission_classes=[IsAuthenticated,IsAdminOfGroupToEdit]
    lookup_field='slug'
    lookup_url_kwarg='slug'
    def get_queryset(self):
        user = self.request.user
        queryset = Group.objects.filter(member=user)
        return queryset
    
    
    @action(methods=['PUT'],detail=True,permission_classes=[IsAdminOfGroupToEdit])
    def add_member(self,request,slug=None):
        username = request.POST.get('username')
        user=get_object_or_404(User,username=username)
        group = self.get_object()
        try:
            group.member.add(user)
            Membership.objects.create(person=user,group=group)
        except:
            return response.Response({'error':'this user in the group already'},status=status.HTTP_400_BAD_REQUEST)
        return response.Response({'username':username},status=status.HTTP_201_CREATED)

    @action(methods=['PUT'],detail=True,permission_classes=[IsAdminOfGroupToEdit])
    def delete_member(self,request,slug=None):
        username = request.POST.get('username')
        user=get_object_or_404(User,username=username)
        group = self.get_object()
        
        group.member.remove(user)
        membership = get_object_or_404(Membership,person=user,group=group)
        membership.delete()
        
        return response.Response({},status=status.HTTP_200_OK)



def room(request):
    token = request.GET.get('token','')
    user_groups = Group.objects.filter(member=request.user)
    serilaizer = GroupSerilaizer(user_groups,many=True)
    
    return render(request, "room.html", {'token':token,
                                         'user_groups':serilaizer.data})