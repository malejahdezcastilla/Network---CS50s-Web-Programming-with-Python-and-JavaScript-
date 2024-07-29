from django.contrib import admin
from .models import Post, User, Interaction, Profile_details

# Register your models here.
admin.site.register(Post)
admin.site.register(User)
admin.site.register(Interaction)
admin.site.register(Profile_details)