from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    設定只有作者本人才可以編輯 snippets
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
