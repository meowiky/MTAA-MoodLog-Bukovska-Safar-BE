from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, AuthTokenSerializer

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
