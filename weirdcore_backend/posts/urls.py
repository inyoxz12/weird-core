from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, ReactionViewSet

router = DefaultRouter()
router.register('', PostViewSet, basename='post')

comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
comment_detail = CommentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

reaction_list = ReactionViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
reaction_detail = ReactionViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
})

urlpatterns = [
    path('', include(router.urls)),
    path('<int:post_pk>/comments/', comment_list, name='comment-list'),
    path('<int:post_pk>/comments/<int:pk>/', comment_detail, name='comment-detail'),
    path('<int:post_pk>/reactions/', reaction_list, name='reaction-list'),
    path('<int:post_pk>/reactions/<int:pk>/', reaction_detail, name='reaction-detail'),
]
