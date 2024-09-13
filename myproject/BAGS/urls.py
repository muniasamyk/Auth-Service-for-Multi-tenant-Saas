from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, OrganizationViewSet, RoleViewSet, MemberViewSet
from .views import sign_in, sign_up, reset_password, invite_member, delete_member, update_member_role

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'members', MemberViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('signin/', sign_in),
    path('signup/', sign_up),
    path('reset_password/', reset_password),
    path('invite_member/', invite_member),
    path('delete_member/', delete_member),
    path('update_member_role/', update_member_role),
]
