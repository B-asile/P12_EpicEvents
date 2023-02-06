from rest_framework import permissions, exceptions


class UsersAccessRight(permissions.BasePermission):
    def has_permission(self, request, view):
        # SuperUser = CRUD
        if request.user.is_superuser:
            return True
        # Dictionary to manage access by group
        groups = {
            'management': ['GET', 'HEAD', 'OPTIONS', 'POST', 'PUT', 'PATCH', 'DELETE'],
            'sales': ['GET', 'HEAD', 'OPTIONS', 'PATCH'],
            'support': ['GET', 'HEAD', 'OPTIONS', 'PATCH'],
        }
        # Check group name and return Authorization for the api-method asked
        for name, methods in groups.items():
            if request.user.groups.filter(name=name).exists():
                if request.method in methods:
                    return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name__in=['support', 'sales']).exists():
            if request.method in ["PATCH"]:
                if 'password' not in str(request.data) and len(request.data) > 1:
                    return False
        return True


class SecurityGroupCustomers(permissions.BasePermission):
    def has_permission(self, request, view):
        # SuperUser = CRUD
        if request.user.is_superuser:
            return True
        # Dictionary to manage access by group
        groups = {
            'management': ['GET', 'HEAD', 'OPTIONS', 'POST', 'PUT', 'PATCH', 'DELETE'],
            'sales': ['GET', 'HEAD', 'OPTIONS'],
            'support': ['GET', 'HEAD', 'OPTIONS'],
        }
        # Check group name and return Authorization for the api-method asked
        for name, methods in groups.items():
            if request.user.groups.filter(name=name).exists():
                if request.method in methods:
                    return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="sale").exists():
            if request.method in ["PUT", "PATCH"]:
                if obj.sales_contact != request.user:
                    return False
        return True


class SecurityGroupEvents(permissions.BasePermission):
    def has_permission(self, request, view):
        # SuperUser = CRUD
        if request.user.is_superuser:
            return True
        # Dictionary to manage access by group
        groups = {
            'management': ['GET', 'HEAD', 'OPTIONS', 'POST', 'PUT', 'PATCH', 'DELETE'],
            'sales': ['GET', 'HEAD', 'OPTIONS', 'POST', 'PUT', 'PATCH'],
            'support': ['GET', 'HEAD', 'OPTIONS', 'POST', 'PUT', 'PATCH'],
        }
        # Check group name and return Authorization for the api-method asked
        for name, methods in groups.items():
            if request.user.groups.filter(name=name).exists():
                if request.method in methods:
                    return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="sales").exists():
            if request.method in ["PUT", "PATCH"]:
                if obj.sales_contact != request.user:
                    return False
        if request.user.groups.filter(name="support").exists():
            if request.method in ["PUT", "PATCH", 'POST']:
                if obj.support_contact != request.user:
                    return False
        return True
