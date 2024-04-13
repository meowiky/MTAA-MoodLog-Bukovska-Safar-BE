from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, DiaryEntry, DiaryEntryTag, Tag, DiaryEntryPhoto, Friendship, Message


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
        fields = ('photo', 'diaryentry')

    def create(self, validated_data):
        photo_instance = DiaryEntryPhoto.objects.create(**validated_data)
        return photo_instance


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


class EmotionStatsSerializer(serializers.Serializer):
    emotion = serializers.CharField(max_length=2)
    count = serializers.IntegerField()


class SendMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class GetMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['text', 'sent_at', 'read_at', 'sender', 'receiver']


class ChangeNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['notification']