from .views import PostView, PostDetailView, CommentView
from django.urls import path

urlpatterns = [
    path('', PostView.as_view({
        'post': 'create',
        'get': 'list'
    }), name='blogs'),
    path('<str:title>/', PostDetailView.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
    }), name='blog-detail'),
    path('<str:title>/comments/', CommentView.as_view({
        'post': 'create'
    }), name='comments')
]
