from blog.models import Post, Comment


def get_posts_all():
    return Post.objects.all()


def get_comments_all():
    return Comment.objects.all()


def get_post_by_title(title:str):
    return Post.objects.filter(title=title).first()
