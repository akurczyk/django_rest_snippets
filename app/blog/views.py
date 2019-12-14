from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from .models import Category, Tag, Post, Comment
from .serializers import CategorySerializer, TagSerializer, PostSerializer, CommentSerializer
from .tasks import delayed_task


#
# PERMISSIONS
#

class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in ('GET', 'HEAD', 'OPTIONS') or \
               request.user.is_staff


class AdminAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in ('GET', 'HEAD', 'OPTIONS', 'POST') or \
               request.user.is_staff or \
               request.user == obj.author


#
# CATEGORY - CUSTOM VIEWS
#

class CategoryListCreateAPIView(APIView):
    permission_classes = [AdminOrReadOnly]

    # List
    def get(self, request):
        queryset = Category.objects.all()

        if api_settings.DEFAULT_PAGINATION_CLASS:
            paginator = api_settings.DEFAULT_PAGINATION_CLASS()
            page = paginator.paginate_queryset(queryset, request, view=self)
            if page:
                serializer = CategorySerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    # Create
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class CategoryDetailsAPIView(APIView):
    permission_classes = [AdminOrReadOnly]

    # Retrieve
    def get(self, request, pk):
        queryset = Category.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(instance)
        return Response(serializer.data)

    # Update
    def put(self, request, pk):
        queryset = Category.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # Partial update
    def patch(self, request, pk):
        queryset = Category.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # Destroy
    def delete(self, request, pk):
        queryset = Category.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        instance.delete()
        return Response(status=HTTP_204_NO_CONTENT)


#
# TAG - GENERIC VIEWS
#

class TagListCreateAPIView(ListCreateAPIView):
    permission_classes = [AdminOrReadOnly]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetailsAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AdminOrReadOnly]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


#
# POST - GENERIC VIEWS
#

class PostListCreateAPIView(ListCreateAPIView):
    permission_classes = [AdminAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailsAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AdminAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


#
# COMMENT - GENERIC VIEWS
#

class CommentListCreateAPIView(ListCreateAPIView):
    permission_classes = [AdminAuthorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetailsAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AdminAuthorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


#
# VIEWSETS
#

class CategoryViewSet(ViewSet):
    permission_classes = [AdminOrReadOnly]

    def list(self, request):
        queryset = Category.objects.all()

        if api_settings.DEFAULT_PAGINATION_CLASS:
            paginator = api_settings.DEFAULT_PAGINATION_CLASS()
            page = paginator.paginate_queryset(queryset, request, view=self)
            if page:
                serializer = CategorySerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    def retrieve(self, request, pk):
        queryset = Category.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(instance)
        return Response(serializer.data)

    def update(self, request, pk):
        queryset = Category.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk):
        queryset = Category.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk):
        queryset = Category.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        instance.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class TagViewSet(ModelViewSet):
    permission_classes = [AdminOrReadOnly]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    # http://127.0.0.1/tags/additional_list_view
    # GET is the default method - it is not necessary to mention it here
    @action(detail=False, methods=['get'])
    def additional_list_view(self, request):
        # RUN TASK WITH CELERY
        delayed_task.delay(123, 456)

        return Response({'aaa': 'bbb'})

    # http://127.0.0.1/tags/PK/additional_detail_view
    # GET is the default method - it is not necessary to mention it here
    @action(detail=True, methods=['get'])
    def additional_detail_view(self, request, pk):
        return Response({'ccc': 'ddd'})


class PostViewSet(ModelViewSet):
    permission_classes = [AdminAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    permission_classes = [AdminAuthorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
