from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserFollows(models.Model):
    userfollows_id = models.AutoField(primary_key=True)
    userfollows_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_by')
    userfollows_follows = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('userfollows_user', 'userfollows_follows')
