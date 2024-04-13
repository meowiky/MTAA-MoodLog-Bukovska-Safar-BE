from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count
from dateutil.relativedelta import relativedelta
from django.db.models.functions import TruncDay
import calendar

from .models import User, DiaryEntry, DiaryEntryTag, Tag, DiaryEntryPhoto, Friendship
from .serializers import UserSerializer, AuthTokenSerializer, DiaryEntryTagSerializer, TagSerializer, \
    DiaryEntryPhotoSerializer, EmotionStatsSerializer
from .serializers import DiaryEntrySerializer, FriendshipRequestSerializer, FriendshipModifySerializer, FriendsSerializer

@api_view(['POST'])
def register(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        user = serialized.save()
        if user:
            return Response(serialized.data, status=status.HTTP_201_CREATED)
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
    print(request.META.get('HTTP_AUTHORIZATION'))
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tag(request):
    serializer = TagSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request, friend_id):
    user = request.user
    friend = get_object_or_404(User, pk=friend_id)

    if user.id > friend_id:
        user, friend = friend, user

    friendship_exists = Friendship.objects.filter(
        (Q(status='PEN') | Q(status='ACC')), user1=user, user2=friend
    ).exists()
    if friendship_exists:
        return Response({'error': 'Friend request already sent or connection exists.'}, status=status.HTTP_400_BAD_REQUEST)

    data = {'user1': user.id, 'user2': friend.id, 'status': 'PEN'}
    serializer = FriendshipRequestSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, friend_id):
    user = request.user
    friend = get_object_or_404(User, pk=friend_id)

    friendship = get_object_or_404(Friendship, user2=user, user1=friend, status='PEN', sender=1)
    if friendship:
        serializer = FriendshipModifySerializer(friendship, data={'status': 'ACC'}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'You do not have permission to accept this friend request'}, status=status.HTTP_403_FORBIDDEN)


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

    emotion_stats = weekly_entries.values('emotion').annotate(count=Count('emotion'))

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

    emotion_stats = monthly_entries.annotate(day=TruncDay('date'))\
                                   .values('day', 'emotion')\
                                   .annotate(count=Count('emotion'))\
                                   .order_by('day', 'emotion')

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

    emotion_stats = yearly_entries.annotate(day=TruncDay('date'))\
                                  .values('day', 'emotion')\
                                  .annotate(count=Count('emotion'))\
                                  .order_by('day', 'emotion')

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


