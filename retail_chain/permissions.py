from rest_framework import permissions


class IsUserModerator(permissions.BasePermission):
    """
    Ограничение прав доступа только для пользователей из группы moderator.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class IsUserOwner(permissions.BasePermission):
    """
    Ограничение прав доступа только для владельцев объекта.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
