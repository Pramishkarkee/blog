from datetime import datetime


import uuid
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class Blog(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    blog = models.TextField()
    approve = models.BooleanField(default=False)
    created_date = models.DateField(default=datetime.now)
    update_date = models.DateField(default=datetime.now)

class Like(models.Model):
    blog= models.ForeignKey(Blog,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        unique_together=['blog','user']

class Comment(models.Model):
    blog= models.ForeignKey(Blog,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField()