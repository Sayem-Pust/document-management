from rest_framework import permissions


class IsOwnerOrShared(permissions.BasePermission):
    # def has_object_permission(self, request, view, obj):
    #     print(request.user)
    #     print(obj.shared_with.all())
    #     print(request.user in obj.shared_with.all())
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #     return obj.owner == request.user and request.user in obj.shared_with.all()
    # def has_permission(self, request, view):
    #     if view.action == 'list':
    #         return request.user.is_authenticated() and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        print(obj.owner)
        return obj.owner == request.user or request.user in obj.shared_with.all() or request.user.is_superuser


class UpdateOwn(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print(obj.owner)
        return obj.owner == request.user


class OwnerAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print(obj.owner)
        return obj.owner == request.user or request.user.is_superuser
