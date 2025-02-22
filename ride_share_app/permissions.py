from rest_framework.permissions import BasePermission

class IsUserRoleAdmin(BasePermission):
    """
    Custom permission to grant access only to users with the 'admin' role under UserAccount.
    """
    def has_permission(self, request, view):
        if hasattr(request.user, 'user_account'):
            return request.user.user_account.role == 'admin'
        return False