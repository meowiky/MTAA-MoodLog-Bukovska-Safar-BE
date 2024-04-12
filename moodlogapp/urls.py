from django.urls import path
from . import views
from .views import create_tag

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('entries/create/', views.create_diary_entry, name='create_diary_entry'),
    path('entries/<int:entry_id>/modify/', views.modify_diary_entry, name='modify_diary_entry'),
    path('entries/<int:entry_id>/add_tag/', views.add_tag, name='add_tag'),
    path('tags/create/', create_tag, name='create_tag'),
    path('friendrequest/<int:user_id>/<int:friend_id>/', views.sendfriendrequest, name='send_request'),
    path('friendaccept/<int:user_id>/<int:friend_id>/', views.acceptfriendrequest, name='accept_request'),
    path('frienddecline/<int:user_id>/<int:friend_id>/', views.declinefriendrequest, name='decline_request'),
    path('friends/<int:user_id>/', views.getallfriends, name='get_friends'),
]