from rest_framework import permissions, exceptions


class UsersAccessRight(permissions.BasePermission):
    def has_permission(self, request, view):
        # Read access by default
        if request.method in permissions.SAFE_METHODS:
            return True
        # SuperUser and Managers CRUD Access
        if request.user.is_superuser or request.user.groups.filter(name__in=['management']).exists():
            return True
        # Sales and Support Team only access to Own Password update action
        # For User in Group Sales or Support, active OPTION top of the page and Patch the new password
        if request.user.groups.filter(name__in=['sales', 'support']).exists():
            if request.method in ['PATCH', 'PUT']:
                # N'autoriser que la modification du password
                return True

