from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default='avatar.svg')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Region(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.DecimalField(decimal_places=15, max_digits=100, default=42.8746)
    longitude = models.DecimalField(decimal_places=15, max_digits=100, default=74.5698)
    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class ImageModel(models.Model):
    message = models.CharField(max_length=200, default='image')
    info = models.TextField(null=True)
    image = models.ImageField(null=True, default='avatar.svg')
    def __str__(self):
        return self.message

class Sight(models.Model):
    name = models.CharField(max_length=200)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    images = models.ManyToManyField(ImageModel, related_name='imgs', blank=True)
    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    sights = models.ManyToManyField(Sight, related_name='sights', blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    images = models.ManyToManyField(ImageModel, related_name='photos', blank=True)

    # id = models.UUIDField(primary_key=True)

    class Meta:
        ordering = ['-updated', 'created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.body[0:50]


class Activity(models.Model):
    name = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name

class Day(models.Model):
    name = models.CharField(max_length=200)
    title = models.TextField(null=True, blank=True)
    rooms = models.ManyToManyField(Room, related_name='rooms', blank=True)
    images = models.ManyToManyField(ImageModel, related_name='images', blank=True)
    activities = models.ManyToManyField(Activity, related_name='activities', blank=True)
    def __str__(self):
        return self.name

class Tour(models.Model):
    name = models.CharField(max_length=200)
    title = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    images = models.ManyToManyField(ImageModel, related_name='pictures', blank=True)
    days = models.ManyToManyField(Day, related_name='days', blank=True)
    def __str__(self):
        return self.name


def create_superuser(self, email, full_name, profile_picture, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not full_name:
            raise ValueError("User must have a full name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.full_name = full_name
        user.set_password(password)
        user.profile_picture = profile_picture
        user.admin = True
        user.staff = True
        user.active = True
        user.save(using=self._db)
        return user