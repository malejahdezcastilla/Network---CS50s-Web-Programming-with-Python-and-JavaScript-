from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass


class Post (models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name= "user_post")
    content= models.CharField(max_length=1000)
    date_creation= models.DateTimeField(auto_now_add= True, null=True)
    liked_by = models.ManyToManyField(User, blank= True, null= True, default= None, related_name= "likes")
    
    def __str__(self):
        return f"Posted by {self.user} on {self.date_creation}" 
    
    
    def post_details(self):
        return {
            "user": self.user,
            "content": self.content,
            "date_creation": self.date_creation.strftime("%b %d %Y, %I:%M %p"),
            "liked_by": self.liked_by,
        }
    # @property
    # def num_likes (self):
    #     numb_likes= self.liked_by.all().count()
        
        # return f" This post has {numb_likes}"


class Interaction(models.Model):
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "followed")
    followers = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "followers")
    
        
    def __str__(self):
        return f" {self.followers} is following {self.followed}"
    
class Profile_details(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name= "user_pics")
    avatar_pic = models.URLField (blank= True, null=True)
    cover_pic= models.URLField (blank= True, null=True)
    
    # def __str__(self):
    #     return f" {self.user} profile details"

    