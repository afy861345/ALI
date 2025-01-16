from django.urls import path
from . import views
urlpatterns = [
    path('',views.main,name='main'),
    path('boards/<int:board_id>/',views.board,name='board'),
    path('boards/<int:board_id>/topic/<int:topic_id>/',views.topic,name='topic'),
    path('boards/<int:board_id>/new/',views.new_topic,name='new_topic'),
    path('boards/<int:board_id>/topic/<int:topic_id>reply/',views.reply,name='reply'),
    path('boards/<int:board_id>/topic/<int:topic_id>/post/<int:post_id>/edit_post/',views.Edit_post.as_view(),name='edit_post'),
    path('patients/',views.Patients.as_view(),name='patients'),
    path('patients/add_patient/',views.Add_Patient.as_view(),name='add_patient'),
    path('patients/<int:patient_id>/',views.get_patient,name='patient'),
    path('patients/new_news/',views.New_news.as_view(),name='new_news'),

]