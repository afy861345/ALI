from django.urls import path
from . import views
urlpatterns = [
    path('',views.main,name='main'),
    path('boards/<int:board_id>/',views.board,name='board'),
    path('boards/<int:board_id>/topic/<int:topic_id>/',views.topic,name='topic'),
    path('boards/<int:board_id>/new/',views.new_topic,name='new_topic'),

]