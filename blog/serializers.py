from rest_framework import serializers

from blog.models import Post, Comment
from blog.queries import get_post_by_title
from user.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'comments']

    def get_fields(self):
        fields = super(CommentSerializer, self).get_fields()
        fields['comments'] = CommentSerializer(many=True)
        return fields


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at', 'comments']

    def create(self, validated_data):
        user = self.context['request'].user
        return Post.objects.create(user=user, **validated_data)


class CreateCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    sub_comment = serializers.SlugRelatedField(queryset=Comment.objects.all(), slug_field='id', write_only=True,
                                               required=False)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'sub_comment']

    def create(self, validated_data):
        post_title = self.context['request'].parser_context.get('kwargs').get(
            'title')
        post = get_post_by_title(title=post_title)
        user = self.context['request'].user
        return Comment.objects.create(post=post, user=user, **validated_data)
