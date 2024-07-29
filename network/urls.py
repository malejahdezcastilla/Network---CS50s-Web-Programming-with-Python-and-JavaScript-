
from django.urls import path

from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all_posts/<int:page>", views.all_posts, name="all_posts"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("user_profile/<username>/<int:page>", views.user_profile, name="user_profile"),
    path("f_uf/<username>", views.follow_unfollow, name="follow_unfollow"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("like/<int:post_id>", views.like_post, name="like"),
    path("unlike/<int:post_id>", views.unlike_post, name="unlike"),
    path("following/<int:page>", views.following, name="following"),
    path("set_profile_img/<str:img_to_set>", views.set_profile_img, name="set_profile_img"),
]
