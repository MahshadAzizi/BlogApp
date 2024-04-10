from rest_framework.permissions import IsAuthenticated
from blog.queries import get_posts_all, get_comments_all
from blog.serializers import PostSerializer, CreateCommentSerializer
from customize.views import CustomViewSet


class PostView(CustomViewSet):
    queryset = get_posts_all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ['get', 'post']


class PostDetailView(CustomViewSet):
    queryset = get_posts_all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ['get', 'post', 'patch']
    lookup_field = 'title'


class CommentView(CustomViewSet):
    queryset = get_comments_all()
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ['post']

