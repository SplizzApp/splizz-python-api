from django.urls import path
from users.views import UserDetailView, UserListView, UserCreateView

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('new/', UserCreateView.as_view(), name='user-create'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
