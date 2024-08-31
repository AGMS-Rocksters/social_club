from django.urls import path
from posts.views import PostList, PostDetail, CommentList, CommentDetail

app_name = "posts"
urlpatterns = [
    path("v1/", PostList.as_view(), name="post-list"),
    path("v1/<int:pk>/", PostDetail.as_view(), name="post-detail"),
    path("v1/<int:post_id>/comments/", CommentList.as_view(), name="comment-list"),
    path(
        "v1/<int:post_id>/comments/<int:pk>/",
        CommentDetail.as_view(),
        name="comment-detail",
    ),
]
