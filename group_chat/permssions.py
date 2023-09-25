from django.shortcuts import get_object_or_404
from rest_framework.permissions import SAFE_METHODS,BasePermission
from .models import Membership


class IsAdminOfGroupToEdit(BasePermission):
    def has_object_permission(self, request, view, obj):
        
        if request.method in ['PUT','PATCH','DELETE']:
           if get_object_or_404(Membership,person=request.user,group=obj).is_admin:
               return True
        else:
            return True
        return False