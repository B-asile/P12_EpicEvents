from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer
from .models import User
from core.permissions import UsersAccessRight


class UserApiView(viewsets.ModelViewSet):
    """
    USERS SECTION
    ==========
    Permissions:
    Management Group Members: CRUD Permissions
    Sales Group Members : Update Own Password
    Support Group Members: Update Own Password
    ==========
    Filters:
    Management Group: View All
    Sales & Support Group: View Own User Profile
    ==========
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, UsersAccessRight )

    def get_queryset(self):
        # if user = SuperUser of is in Management Group, show all users
        if self.request.user.is_superuser or self.request.user.groups.filter(name__in=['management']).exists():
            return User.objects.all()
        # if user is in Support or Sales Group, Show only himself
        if self.request.user.groups.filter(name__in=['support', 'sales']).exists():
            return User.objects.filter(pk=self.request.user.pk)