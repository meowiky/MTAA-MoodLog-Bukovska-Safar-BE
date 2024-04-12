from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, DiaryEntry, DiaryEntryTag, Tag, DiaryEntryPhoto, Friendship


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


class FriendshipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = '__all__'


class FriendshipModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ['status']       


class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email']
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj[0]

    def get_email(self, obj):
        return obj[1]

