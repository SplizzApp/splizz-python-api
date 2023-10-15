# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django.utils import timezone as tim

from users.models import User
from users.serializers import UserSerializer


class UsersPagination(generics.ListAPIView):
    default_limit = 10
    max_limit = 100


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # filter_backends = (DjangoFilterBackend, SearchFilter)
    # filter_fields = ('id',)
    # search_fields = ('first_name', 'last_name')

    # pagination_class = UsersPagination

    # permission_classes = [IsAdminUser]

    def get_queryset(self):
        uid = self.request.query_params.get('id')
        if uid is None:
            return super().get_queryset()

        queryset = User.objects.all()
        queryset = queryset.filter(id=uid)

        return queryset


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    #     try:
    #         uid = User.objects.get('id')
    #         if uid is No


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        uid = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            from django.core.cache import cache
            cache.delete(f"user_data_{uid}")
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            from django.core.cache import cache
            user = response.data
            cache.set(f"user_data_{user['id']}", {
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'email': user['email'],
                'phone': user['phone'],
                'color': user['color'],
                'date_joined': user['date_joined'],
                'modified_timestamp': tim.now(),
                'created_timestamp': user['created_timestamp'],
            })

        return response
