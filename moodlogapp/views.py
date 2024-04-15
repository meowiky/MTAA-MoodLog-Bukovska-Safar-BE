from django.contrib.auth import authenticate
from django.db.models import Q, Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models.functions import TruncDay
import calendar
from rest_framework.parsers import FileUploadParser
from rest_framework.decorators import parser_classes
from django.db import IntegrityError
from django.db.models import Q

from .models import User, DiaryEntry, DiaryEntryTag, Tag, DiaryEntryPhoto, Friendship, Message
from .serializers import UserSerializer, AuthTokenSerializer, DiaryEntryTagSerializer, TagSerializer, DiaryEntryPhotoSerializer
from .serializers import DiaryEntrySerializer, FriendshipRequestSerializer, FriendshipModifySerializer, FriendsSerializer
from .serializers import SendMessageSerializer, GetMessagesSerializer, ChangeNotificationSerializer, EmotionStatsSerializer

@api_view(['POST'])
def register(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        try:
            user = serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            if 'unique constraint' in str(e):
                return Response({'email': ['A user with that email already exists.']}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serialized = AuthTokenSerializer(data=request.data)
    if serialized.is_valid():
        user = authenticate(email=serialized.validated_data['email'],
                            password=serialized.validated_data['password'])
        if user:
            from rest_framework.authtoken.models import Token
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_diary_entry(request):
    serializer = DiaryEntrySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def modify_diary_entry(request, entry_id):
    try:
        diary_entry = DiaryEntry.objects.get(id=entry_id, user=request.user)
    except DiaryEntry.DoesNotExist:
        return Response({'message': 'DiaryEntry not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = DiaryEntrySerializer(diary_entry, data=request.data)
    else:
        serializer = DiaryEntrySerializer(diary_entry, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_diary_entry(request, entry_id):
    try:
        diary_entry = DiaryEntry.objects.get(id=entry_id, user=request.user)
    except DiaryEntry.DoesNotExist:
        return Response({'message': 'DiaryEntry not found'}, status=status.HTTP_404_NOT_FOUND)

    diary_entry.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tag(request):
    serializer = TagSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_tag(request, entry_id):
    tag_name = request.data.get('tagname')

    try:
        diary_entry = DiaryEntry.objects.get(id=entry_id, user=request.user)
    except DiaryEntry.DoesNotExist:
        return Response({'message': 'DiaryEntry not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        tag = Tag.objects.get(tagname=tag_name, user=request.user)
    except Tag.DoesNotExist:
        return Response({'message': 'Tag not found'}, status=status.HTTP_404_NOT_FOUND)

    diary_entry_tag, created = DiaryEntryTag.objects.get_or_create(
        diaryentry=diary_entry,
        tag=tag,
        user=request.user
    )

    serializer = DiaryEntryTagSerializer(diary_entry_tag)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_tag_from_entry(request, entry_id, tag_id):
    try:
        diary_entry = DiaryEntry.objects.get(id=entry_id, user=request.user)
    except DiaryEntry.DoesNotExist:
        return Response({'message': 'DiaryEntry not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        tag = Tag.objects.get(id=tag_id, user=request.user)
    except Tag.DoesNotExist:
        return Response({'message': 'Tag not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        diary_entry_tag = DiaryEntryTag.objects.get(
            diaryentry=diary_entry,
            tag=tag,
            user=request.user
        )
        diary_entry_tag.delete()
        return Response({'message': 'Tag removed from entry'}, status=status.HTTP_204_NO_CONTENT)
    except DiaryEntryTag.DoesNotExist:
        return Response({'message': 'Tag not associated with this diary entry'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request, friend_id):
    user = request.user
    if user.pk == friend_id:
        return Response({'error': 'You cannot send a friend request to yourself.'}, status=status.HTTP_400_BAD_REQUEST)

    friend = get_object_or_404(User, pk=friend_id)
    friendship_exists = Friendship.objects.filter(
        (Q(status='PEN') | Q(status='ACC')),
        (Q(user1=user, user2=friend) | Q(user1=friend, user2=user))
    ).exists()
    if friendship_exists:
        return Response({'error': 'Friend request already sent or connection exists.'}, status=status.HTTP_400_BAD_REQUEST)

    data = {'user1': user.id, 'user2': friend.id, 'status': 'PEN', 'sender': user.id}
    serializer = FriendshipRequestSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, friend_id):
    user = request.user
    friend = get_object_or_404(User, pk=friend_id)

    try:
        friendship = Friendship.objects.get(
            user1=friend, user2=user, status='PEN', sender=friend.id
        )
    except Friendship.DoesNotExist:
        return Response({'error': 'You do not have permission to accept this friend request'}, status=status.HTTP_403_FORBIDDEN)

    serializer = FriendshipModifySerializer(friendship, data={'status': 'ACC'}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def decline_friend_request(request, friend_id):
    user = request.user
    friend = get_object_or_404(User, pk=friend_id)

    if user.id > friend_id:
        user, friend = friend, user

    friendship = get_object_or_404(Friendship, user1=user, user2=friend)
    serializer = FriendshipModifySerializer(friendship, data={'status': 'DEC'}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_friends(request):
    user = request.user
    friends1 = Friendship.objects.filter(user1=user, status='ACC').select_related("user2").values_list("user2__name", "user2__email").distinct()
    friends2 = Friendship.objects.filter(user2=user, status='ACC').select_related("user1").values_list("user1__name", "user1__email").distinct()
    friends = friends1.union(friends2)

    serializer = FriendsSerializer(friends, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_name(request):
    user = request.user
    new_name = request.data.get('name')
    if new_name:
        user.name = new_name
        user.save()
        return Response({'message': 'Name updated successfully.'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid request, name is required.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_email(request):
    user = request.user
    new_email = request.data.get('email')
    if new_email:
        if User.objects.filter(email=new_email).exists():
            return Response({'error': 'This email is already in use.'}, status=status.HTTP_400_BAD_REQUEST)
        user.email = new_email
        user.save()
        return Response({'message': 'Email updated successfully.'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid request, email is required.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    if user.check_password(old_password):
        if old_password == new_password:
            return Response({'error': 'New password cannot be the same as the old password.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
    return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_tags(request):
    tags = Tag.objects.filter(user=request.user).order_by('tagname')
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_weekly_emotion_stats(request):
    today = timezone.now().date()
    a_week_ago = today - timezone.timedelta(days=7)

    weekly_entries = DiaryEntry.objects.filter(
        user=request.user,
        date__range=[a_week_ago, today]
    )

    emotion_stats = weekly_entries.values('emotion') \
        .annotate(count=Count('id')) \
        .order_by('emotion')

    serializer = EmotionStatsSerializer(emotion_stats, many=True)

    number_of_days = weekly_entries.annotate(day=TruncDay('date')).values('day').distinct().count()

    stats = {
        'emotion_stats': serializer.data,
        'number_of_days_with_entry': number_of_days,
        'number_of_days': 7
    }

    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_monthly_emotion_stats(request):
    today = timezone.now().date()
    a_month_ago = today - relativedelta(months=1)

    monthly_entries = DiaryEntry.objects.filter(
        user=request.user,
        date__range=[a_month_ago, today]
    )

    emotion_stats = monthly_entries.values('emotion') \
        .annotate(count=Count('id')) \
        .order_by('emotion')

    _, total_days_in_month = calendar.monthrange(today.year, today.month)

    number_of_days = monthly_entries.annotate(day=TruncDay('date')).values('day').distinct().count()

    serializer = EmotionStatsSerializer(emotion_stats, many=True)

    stats = {
        'emotion_stats': serializer.data,
        'number_of_days_with_entry': number_of_days,
        'number_of_days': total_days_in_month
    }

    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_yearly_emotion_stats(request):
    today = timezone.now().date()
    a_year_ago = today - relativedelta(years=1)

    yearly_entries = DiaryEntry.objects.filter(
        user=request.user,
        date__range=[a_year_ago, today]
    )

    emotion_stats = yearly_entries.values('emotion') \
        .annotate(count=Count('id')) \
        .order_by('emotion')

    number_of_days = yearly_entries.annotate(day=TruncDay('date')).values('day').distinct().count()

    serializer = EmotionStatsSerializer(emotion_stats, many=True)

    total_days_in_year = 365 + calendar.isleap(today.year)

    stats = {
        'emotion_stats': serializer.data,
        'number_of_days_with_entry': number_of_days,
        'number_of_days': total_days_in_year
    }

    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_diary_entries_ordered(request):
    diary_entries = DiaryEntry.objects.filter(user=request.user).order_by('-date')

    serializer = DiaryEntrySerializer(diary_entries, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request, friend_id):
    user=request.user
    friend=get_object_or_404(User, pk=friend_id)
    request.data['sender']=user.id
    request.data['receiver']=friend.id
    serializer = SendMessageSerializer(data = request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request, friend_id):
    user=request.user
    friend=get_object_or_404(User, pk=friend_id)
    
    messages = Message.objects.filter(Q(sender=user, receiver=friend) | Q(sender=friend, receiver=user))
    messages_to_update = messages.filter(sender=friend, read_at=None)
    if messages_to_update:
        messages_to_update.update(read_at=timezone.now())
    serializer = GetMessagesSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_message(request, message_id):
    user=request.user
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return Response({'message': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

    if message.sender!=user:
        return Response({'error': 'You are not authorized to delete this message'}, status=status.HTTP_401_UNAUTHORIZED)
    message.delete()
    return Response({'message': 'Message deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_notifications(request):
    user=request.user

    notification=user.notification
    if notification:
        notification=False
    else:
        notification=True
    
    serializer = ChangeNotificationSerializer(user, data={'notification': notification}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([FileUploadParser])
def add_photo_to_entry(request, entry_id):
    try:
        diary_entry = DiaryEntry.objects.get(id=entry_id, user=request.user)
    except DiaryEntry.DoesNotExist:
        return Response({'message': 'DiaryEntry not found'}, status=status.HTTP_404_NOT_FOUND)

    file_serializer = DiaryEntryPhotoSerializer(data=request.data)

    if file_serializer.is_valid():
        file_serializer.save(diaryentry=diary_entry)
        return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_diary_entries(request):
    keyword = request.query_params.get('keyword', None)

    if keyword is not None:
        diary_entries = DiaryEntry.objects.filter(
            Q(title__icontains=keyword) | Q(text__icontains=keyword),
            user=request.user
        ).order_by('-date')

        serializer = DiaryEntrySerializer(diary_entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Keyword parameter is missing.'}, status=status.HTTP_400_BAD_REQUEST)
