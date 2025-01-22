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
    path('patients/<int:patient_id>/new/',views.New_visit.as_view(),name='new_visit'),
    path('patients/new_news/',views.New_news.as_view(),name='new_news'),
    path('news/<int:news_id>/delete_news/',views.Delete_news.as_view(),name='delete_news'),
    path('news/<int:news_id>/edit_news/',views.Edit_news.as_view(),name='edit_news'),
    path('patients/<int:patient_id>/edit/',views.Edit_patient.as_view(),name='edit_patient'),
    path('patients/<int:patient_id>/delete/',views.Delete_patient.as_view(),name='delete_patient'),
    path('patients/<int:patient_id>/add_media/',views.add_media,name='add_media'),
    path('patients/<int:patient_id>/<int:photo_id>/delete_entire_media/',views.Delete_entire_media.as_view(),name='delete_entire_media'),
    path('patients/<int:patient_id>/<int:photo_id>/edit_media/',views.Edit_media.as_view(),name='edit_media'),
    path('patients/<int:patient_id>/<int:photo_id>/delete/',views.delete_media,name='delete_media'),
    path('patients/<int:patient_id>/make_pill/',views.create_pill,name='make_pill'),
    path('patients/download_file/<int:patient_id>/',views.download_file,name='download_file'),
    path('patients/download_image/<int:patient_id>/',views.download_image,name='download_image'),


]