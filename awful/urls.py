from django.urls import path
from .views import (
    GroupPermissionView,
    PermissionView,
    MyAppViewCreate,
    MyAppViewList,
    UserCreate
)

urlpatterns = [
    path('', GroupPermissionView.as_view(), name='group_permission_list_create'),
    path('permission/', PermissionView.as_view(), name='group_permission_list_create'),
    path('my-app-create/', MyAppViewCreate.as_view(), name='my_app_create'),
    path('my-app-list/', MyAppViewList.as_view(), name='my_app_list'),
    path('user-create/', UserCreate.as_view(), name='user-create'),
]
