from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users_photos/%Y/%m/%d/', default='avatar.png')
    facebook = models.URLField()
    twitter = models.URLField()
    linkedin = models.URLField()

    def __str__(self):
        return f'{self.user.username}'
