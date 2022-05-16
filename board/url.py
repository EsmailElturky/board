from unicodedata import name
from django.urls import path
from . import views
import board
urlpatterns = [
    path('',views.BoardListView.as_view(),name="index"),
    path('board/<int:board_id>/',views.board_topics,name='board_topics'),
    path('board/<int:board_id>/new_topics',views.new_topic,name='new topic'),
    path('board/<int:board_id>/topics/<int:topic_id>',views.topic_posts,name="topic_posts"),
    path('board/<int:board_id>/topics/<int:topic_id>/reply',views.reply_topic,name="reply_topic"),
    path('board/<int:board_id>/topics/<int:topic_id>/posts/<int:post_id>/edit',views.PostUpdateView.as_view(),name="edit_post"),


]