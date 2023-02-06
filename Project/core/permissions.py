from rest_framework import permissions, exceptions

from datetime import datetime
import logging
logger = logging.getLogger('user_actions')

logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] "%(message)s" %(levelname)s %(name)s', datefmt='%d/%b/%Y %H:%M:%S')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

class UsersAccessRight(permissions.BasePermission):
    def has_permission(self, request, view):
        # SuperUser = CRUD
        if request.user.is_superuser:
            logger.info(f"{datetime.now().strftime('%d/%b/%Y %H:%M:%S')} - "
                        f"User {request.user.email} is a superuser "
                        f"and has full access to {request.method} {view.__class__.__name__}")
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
                    logger.info(f"{datetime.now().strftime('%d/%b/%Y %H:%M:%S')} - "
                                f"{request.user.email} Authorized access {view.__class__.__name__}")
                    return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name__in=['support', 'sales']).exists():
            if request.method in ["PATCH"]:
                if 'password' not in str(request.data) and len(request.data) > 1:
                    logger.warning(f"{datetime.now().strftime('%d/%b/%Y %H:%M:%S')} - "
                                   f"{request.user.email} try to modify object {obj.id} "
                                   f"in {view.__class__.__name__} with {request.method} PERMISSION DENIED")
                    return False
        logger.info(f"{datetime.now().strftime('%d/%b/%Y %H:%M:%S')} - "
                    f"{request.user.email} Authorized access object {obj.id} "
                    f"in {view.__class__.__name__}")
        return True


class SecurityGroupCustomers(permissions.BasePermission):
    def has_permission(self, request, view):
        # SuperUser = CRUD
        if request.user.is_superuser:
            logger.info(f"{datetime.now().strftime('%d/%b/%Y %H:%M:%S')} - "
                        f"User {request.email} is a superuser "
                        f"and has full access to {request.method} {view.__class__.__name__}")
            return True
        # Dictionary to manage access by group
        groups = {
            'management': ['GET', 'HEAD', 'OPTIONS', 'POST', 'PUT', 'PATCH', 'DELETE'],
            'sales': ['GET', 'HEAD', 'OPTIONS', 'POST', 'PUT', 'PATCH'],
            'support': ['GET', 'HEAD', 'OPTIONS'],
        }
        # Check group name and return Authorization for the api-method asked
        for name, methods in groups.items():
            if request.user.groups.filter(name=name).exists():
                if request.method in methods:
                    logger.info(f"{datetime.now().strftime('%d/%b/%Y %H:%M:%S')} - "
                                f"{request.user.email} Authorized access {view.__class__.__name__} ")
                    return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="sales").exists():
            if request.method in ["PUT", "PATCH"]:
                if obj.sales_contact != request.user:
                    logger.warning(f"{datetime.now().strftime('%d/%b/%Y %H:%M:%S')} - "
                                   f"{request.user.email} try to modify object {obj.id} "
                                   f"in {view.__class__.__name__} with {request.method} PERMISSION DENIED")
                    return False
        logger.info(f"{datetime.now().strftime('%d/%b/%Y %H:%M:%S')} - "
                    f"{request.user.email} Authorized access object {obj.id} "
                    f"in {view.__class__.__name__}")
        return True

class SecurityGroupContracts(permissions.BasePermission):
    def has_permission(self, request, view):
        # SuperUser = CRUD
        if request.user.is_superuser:
            logger.info(f"{datetime.now().strftime('%d/%b/%Y %H:%M:%S')} - "
                        f"User {request.user.email} is a superuser "
                        f"and has full access to {request.method} {view.__class__.__name__}")
            return True
        # Dictionary to manage access by group
        groups = {
            'management': ['GET', 'HEAD', 'OPTIONS', 'POST', 'PUT', 'PATCH', 'DELETE'],
            'sales': ['GET', 'HEAD', 'OPTIONS', 'POST', 'PUT', 'PATCH'],
            'support': ['GET', 'HEAD', 'OPTIONS'],
        }
        # Check group name and return Authorization for the api-method asked
        for name, methods in groups.items():
            if request.user.groups.filter(name=name).exists():
                if request.method in methods:
                    logger.info(f"{datetime.now().strftime('%d/%b/%Y %H:%M:%S')} - "
                                f"{request.user.email} Authorized access {view.__class__.__name__} ")
                    return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="sales").exists():
            if request.method in ["PUT", "PATCH"]:
                if obj.sales_contact != request.user:
                    logger.warning(f"{datetime.now().strftime('%d/%b/%Y %H:%M:%S')} - "
                                   f"{request.user.email} try to modify object {obj.id} "
                                   f"in {view.__class__.__name__} with {request.method} PERMISSION DENIED")
                    return False
        logger.info(f"{datetime.now().strftime('%d/%b/%Y %H:%M:%S')} - "
                    f"{request.user.email} Authorized access object {obj.id} "
                    f"in {view.__class__.__name__}")
        return True

class SecurityGroupEvents(permissions.BasePermission):
    def has_permission(self, request, view):
        # SuperUser = CRUD
        if request.user.is_superuser:
            logger.info(f"{datetime.now().strftime('%d/%b/%Y %H:%M:%S')} - "
                        f"User {request.user.email} is a superuser "
                        f"and has full access to {request.method} {view.__class__.__name__}")
            return True
        # Dictionary to manage access by group
        groups = {
            'management': ['GET', 'HEAD', 'OPTIONS', 'POST', 'PUT', 'PATCH', 'DELETE'],
            'sales': ['GET', 'HEAD', 'OPTIONS', 'PUT', 'PATCH'],
            'support': ['GET', 'HEAD', 'OPTIONS', 'PUT', 'PATCH'],
        }
        # Check group name and return Authorization for the api-method asked
        for name, methods in groups.items():
            if request.user.groups.filter(name=name).exists():
                if request.method in methods:
                    logger.info(f"{datetime.now().strftime('%d/%b/%Y %H:%M:%S')} - "
                                f"{request.user.email} Authorized access {view.__class__.__name__}")
                    return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="sales").exists():
            if request.method in ["PUT", "PATCH"]:
                if obj.sales_contact != request.user:
                    logger.warning(f"{datetime.now().strftime('%d/%b/%Y %H:%M:%S')} - "
                                   f"{request.user.email} try to modify object {obj.id} "
                                   f"in {view.__class__.__name__} with {request.method} PERMISSION DENIED")
                    return False
        if request.user.groups.filter(name="support").exists():
            if request.method in ['PUT', 'PATCH']:
                if obj.support_contact != request.user:
                    logger.warning(f"{datetime.now().strftime('%d/%b/%Y %H:%M:%S')} - "
                                   f"{request.user.email} try to modify object {obj.id} "
                                   f"in {view.__class__.__name__} with {request.method} PERMISSION DENIED")
                    return False
        logger.info(f"{datetime.now().strftime('%d/%b/%Y %H:%M:%S')} - "
                    f"{request.user.email} Authorized access object {obj.id} "
                    f"in {view.__class__.__name__}")
        return True

