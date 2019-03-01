from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or view.action == 'create':
            return True

        return view.action != 'list' and (request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_superuser

class PostPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or view.action == 'list':
            return True
        
        return view.action != 'list' and (request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_superuser
