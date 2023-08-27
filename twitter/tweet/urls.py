from django.urls import path
from .views import (
    PostRetriveCreateDeleteAPIView,
    PostListAPIView,
    FollowingPostListAPIView,
)


app_name = "tweet"
urlpatterns = [
    path(
        "api/post/<int:post_id>/", PostRetriveCreateDeleteAPIView.as_view(), name="post"
    ),
    path("api/post/", PostListAPIView.as_view(), name="posts"),
    path(
        "api/followings_posts/",
        FollowingPostListAPIView.as_view(),
        name="followings_posts",
    ),
]
