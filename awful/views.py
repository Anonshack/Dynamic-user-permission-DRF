from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import GroupSerializer, MyUserSerializer, PermissionSerializer, MyappSerializer
from django.contrib.auth.models import Permission, Group
from .models import MyUser, Myapp
from rest_framework.exceptions import PermissionDenied


class GroupPermissionView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class PermissionView(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class MyAppViewCreate(generics.CreateAPIView):
    queryset = Myapp.objects.all()
    serializer_class = MyappSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.has_perm('awful.add_myapp'):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise PermissionDenied()


class MyAppViewList(generics.ListAPIView):
    queryset = Myapp.objects.all()
    serializer_class = MyappSerializer

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('awful.view_myapp'):
            return Myapp.objects.all()
        else:
            raise PermissionDenied()


class UserCreate(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        groups_data = self.request.data.get('groups', [])
        permissions_data = self.request.data.get('permissions', [])
        for group_id in groups_data:
            try:
                group = Group.objects.get(id=group_id)
                user.groups.add(group)
            except Group.DoesNotExist:
                return Response({'error': f'Group with id {group_id} does not exist'},
                                status=status.HTTP_400_BAD_REQUEST)
        for permission_id in permissions_data:
            try:
                permission = Permission.objects.get(id=permission_id)
                user.user_permissions.add(permission)
            except Permission.DoesNotExist:
                return Response({'error': f'Permission with id {permission_id} does not exist'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
