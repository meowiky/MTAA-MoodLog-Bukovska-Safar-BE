from django.urls import path
from . import views
from .views import get_weekly_emotion_stats, get_monthly_emotion_stats, get_yearly_emotion_stats, \
    get_diary_entries_ordered, remove_tag_from_entry, delete_diary_entry

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('entries/create/', views.create_diary_entry, name='create_diary_entry'),
    path('entries/<int:entry_id>/modify/', views.modify_diary_entry, name='modify_diary_entry'),
    path('entries/<int:entry_id>/add_tag/', views.add_tag, name='add_tag'),
    path('tags/create/', views.create_tag, name='create_tag'),
    path('friend_requests/send/<int:friend_id>/', views.send_friend_request, name='send_request'),
    path('friend_requests/accept/<int:friend_id>/', views.accept_friend_request, name='accept_request'),
    path('friend_requests/decline/<int:friend_id>/', views.decline_friend_request, name='decline_request'),
    path('friends/', views.get_all_friends, name='get_friends'),
    path('change_name/', views.change_name, name='change_name'),
    path('change_email/', views.change_email, name='change_email'),
    path('change_password/', views.change_password, name='change_password'),
    path('tags/', views.list_user_tags, name='list_user_tags'),
    path('stats/emotions/weekly/', get_weekly_emotion_stats, name='weekly-emotion-stats'),
    path('stats/emotions/monthly/', get_monthly_emotion_stats, name='monthly-emotion-stats'),
    path('stats/emotions/yearly/', get_yearly_emotion_stats, name='yearly-emotion-stats'),
    path('entries/ordered/', get_diary_entries_ordered, name='get_diary_entries_ordered'),
    path('send_message/<int:friend_id>/', views.send_message, name='send_message'),
    path('get_messages/<int:friend_id>/', views.get_messages, name='get_messages'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('change_notifications/', views.change_notifications, name='change_notifications'),
    path('entries/<int:entry_id>/remove_tag/<int:tag_id>/', remove_tag_from_entry, name='remove_tag_from_entry'),
    path('entries/<int:entry_id>/delete/', delete_diary_entry, name='delete_diary_entry'),
]
