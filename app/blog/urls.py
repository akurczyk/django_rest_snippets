from django.urls import path
from rest_framework import routers

from .views import CategoryListCreateAPIView, CategoryDetailsAPIView, TagListCreateAPIView, TagDetailsAPIView, \
    PostListCreateAPIView, PostDetailsAPIView, CommentListCreateAPIView, CommentDetailsAPIView, \
    CategoryViewSet, TagViewSet, PostViewSet, CommentViewSet

#
# VIEWS
#

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view(), name='api-categories-list'),
    path('categories/<int:pk>/', CategoryDetailsAPIView.as_view(), name='api-categories-details'),

    path('tags/', TagListCreateAPIView.as_view(), name='api-tags-list'),
    path('tags/<int:pk>/', TagDetailsAPIView.as_view(), name='api-tags-details'),

    path('posts/', PostListCreateAPIView.as_view(), name='api-posts-list'),
    path('posts/<int:pk>/', PostDetailsAPIView.as_view(), name='api-posts-details'),

    path('comments/', CommentListCreateAPIView.as_view(), name='api-comments-list'),
    path('comments/<int:pk>/', CommentDetailsAPIView.as_view(), name='api-comments-details'),
]

#
# VIEWSETS
#

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls  # Comment out this line to switch to normal views
