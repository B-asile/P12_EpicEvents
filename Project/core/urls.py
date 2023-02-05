from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserApiView

router = routers.DefaultRouter()

router.register(r'users', UserApiView)
router_users = routers.NestedSimpleRouter(router, r'users', lookup='users')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("", include(router.urls)),
    path("", include(router_users.urls)),
]