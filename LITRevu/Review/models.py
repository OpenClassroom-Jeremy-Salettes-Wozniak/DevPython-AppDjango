from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    review_ticket = models.ForeignKey('ticket.Ticket', on_delete=models.CASCADE)
    review_rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_headline = models.CharField(max_length=128)
    review_body = models.CharField(max_length=8192)
    review_time_created = models.DateTimeField(auto_now_add=True)