from rest_framework import mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.viewsets import GenericViewSet

from movies_rest_app.auth.serializers import *


class IsStaffPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffPermission])
def get_all_users(request):
    query = User.objects.all()
    s = UserSerializer(instance=query, many=True)
    return Response(data=s.data)


class CreateUserPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff and "is_staff" in request.data:
            return True
        elif "is_staff" not in request.data:
            return True
        else:
            return False


class UserViewSet(mixins.CreateModelMixin, GenericViewSet):

    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [CreateUserPermission]





