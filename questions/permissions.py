from rest_framework.permissions import SAFE_METHODS,BasePermission




class AdminOnlyCanPost(BasePermission):
    def has_permission(self,request,view):
        if request.method in SAFE_METHODS:
            return True
        else:
            if request.user.is_staff:
                return True
            return False


class UserWhoRequestCanPost(BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user  

class OwnerNotAllowed(BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in SAFE_METHODS:
            return False
        return obj.user != request.user  
