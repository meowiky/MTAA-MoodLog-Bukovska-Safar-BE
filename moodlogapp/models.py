from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, password=password, name=name)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    notification = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Emotion(models.TextChoices):
    VERY_HAPPY = 'VH', 'Very Happy'
    HAPPY = 'H', 'Happy'
    NEUTRAL = 'N', 'Neutral'
    ANGRY = 'A', 'Angry'
    SAD = 'S', 'Sad'

class Tag(models.Model):
    tagname = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.tagname

    class Meta:
        unique_together = ('user', 'tagname')

class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    emotion = models.CharField(max_length=2, choices=Emotion.choices)
    location = models.CharField(max_length=255, blank=True, null=True)

class DiaryEntryTag(models.Model):
    diaryentry = models.ForeignKey(DiaryEntry, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class DiaryEntryPhoto(models.Model):
    diaryentry = models.ForeignKey(DiaryEntry, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/')

class FriendshipStatus(models.TextChoices):
    ACCEPTED = 'ACC', 'Accepted'
    PENDING = 'PEN', 'Pending'
    DECLINED = 'DEC', 'Declined'
    
class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_user2')
    status = models.CharField(max_length=3, choices=FriendshipStatus.choices, default='PEN')
    sender = models.IntegerField(choices=[(1, 'User1'), (2, 'User2')], default=1)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_receiver')
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

