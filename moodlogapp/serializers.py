from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, DiaryEntryTag
from .models import DiaryEntry
from .models import Tag
from .models import DiaryEntryPhoto


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(email=attrs.get('email'), password=attrs.get('password'))
        if user:
            return attrs
        else:
            raise serializers.ValidationError('Incorrect email or password')


class DiaryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaryEntry
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tagname']

class DiaryEntryTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaryEntryTag
        fields = ['diaryentry', 'tag']

    def create(self, validated_data):
        pass


class DiaryEntryPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaryEntryPhoto
        fields = '__all__'


