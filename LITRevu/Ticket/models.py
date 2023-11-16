from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    ticket_title = models.CharField(max_length=128)
    ticket_description = models.CharField(max_length=2048)
    ticket_user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_created = models.DateTimeField(auto_now_add=True)
