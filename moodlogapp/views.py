from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, DiaryEntryTag
from .serializers import UserSerializer, AuthTokenSerializer, DiaryEntryTagSerializer
from rest_framework.permissions import IsAuthenticated
from .models import DiaryEntry
from .serializers import DiaryEntrySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import Tag
from .serializers import TagSerializer
from .models import DiaryEntryPhoto
from .serializers import DiaryEntryPhotoSerializer

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



