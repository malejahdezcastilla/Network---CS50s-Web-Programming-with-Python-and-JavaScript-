from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Post, Interaction, Profile_details
import json

def new_post (request):
    if request.method == "POST":
        content = request.POST["post_content"]
        user = User.objects.get (pk=request.user.id)
        post = Post(user=user, content=content)
        post.save()
        
        return HttpResponseRedirect(reverse(index))
    

def index(request):
    posts = Post.objects.all().order_by ("-date_creation")[:10]
    
    return render(request, "network/index.html", {
        "posts":posts,
    })       


def all_posts (request, page):
    posts = Post.objects.all().order_by ("-date_creation")
    posts_per_page= Paginator(posts, 10) 
    page_object = posts_per_page.get_page(page)
    
    return render (request, "network/all_posts.html", {
        "page_object":page_object,

    })
    
def following (request, page):
    current_user= request.user
    list_following= Interaction.objects.filter(followers= current_user)
    posts = Post.objects.all().order_by ("-date_creation")
    posts_from_following = []
    for post in posts:
        for user_followed in list_following:
            if user_followed.followed == post.user:
                posts_from_following.append(post)
                         
    posts_per_page= Paginator(posts_from_following, 10) 
    page_object = posts_per_page.get_page(page)
    print("po",page_object)
    print("pa",page)
    print(posts_per_page)
    
    return render (request, "network/following.html", {
        "message":" To view this section follow other users to see their posts",
        "page_object":page_object,
        "posts_from_following":posts_from_following,
    })

    
def user_profile (request, username, page):
    user = User.objects.get(username=username)
    user_posts = Post.objects.filter(user= user).order_by("-date_creation")
    posts_per_page= Paginator(user_posts, 10) 
    page_objec = posts_per_page.get_page(page)
    num_posts = Post.objects.filter(user=user).count()
    num_following = Interaction.objects.filter (followers= user).count()
    num_followers = Interaction.objects.filter (followed= user).count ()
    followers = Interaction.objects.filter(followed = user).values_list("followers", flat= True)
    following = Interaction.objects.filter(followers= user).values_list("followed", flat= True)
    list_following = User.objects.filter(id__in = following).values_list("username", flat= True)
    list_followers = User.objects.filter(id__in = followers).values_list("username", flat= True)
    profile_imgs= None
    try:
        profile_imgs = Profile_details.objects.get(user=user)
    except:
        Profile_details.DoesNotExist

    return render (request, "network/user_profile.html", {
        "user_posts": user_posts,
        "user" : user,
        "num_posts": num_posts,
        "num_following":num_following,
        "num_followers": num_followers,
        "following": list_following,
        "followers": list_followers,
        "page_objec": page_objec,
        "profile_imgs":profile_imgs,   
    })
    
    
def follow_unfollow (request, username):
    current_user = request.user
    user_to_follow = User.objects.get(username= username)
    
    if request.method == "POST":
        try:
            get_interaction = Interaction.objects.get(followers= current_user, followed = user_to_follow)
        
        except Interaction.DoesNotExist:
        
            try:
                profile_object = User.objects.get(username = username)
            except User.DoesNotExist:
                return HttpResponse (status = 404)
            else:
                profile_to_follow = Interaction(followers= current_user, followed = profile_object)
                profile_to_follow.save ()
        else:
            get_interaction.delete()           
    
    return redirect (reverse("user_profile", args = [username, 1]))


def set_profile_img (request, img_to_set):
    current_user= request.user
    if img_to_set == "cover_img":
        if request.method == "POST":
            try: 
                content = request.POST["cover_img"]
                user_profile_to_set= Profile_details.objects.get(user= current_user)
                user_profile_to_set.cover_pic= content
                user_profile_to_set.save()
                return redirect (reverse("user_profile", args=[current_user, 1]))
            
            except Profile_details.DoesNotExist:
                user_profile_to_set = Profile_details(user= current_user, cover_pic= content)
                user_profile_to_set.save()
                return redirect (reverse("user_profile", args=[current_user, 1]))

    else:
        if request.method == "POST":
            try:
                content = request.POST["profile_img"]
                user_profile_to_set= Profile_details.objects.get(user=current_user)
                user_profile_to_set.avatar_pic= content
                user_profile_to_set.save()
                return redirect (reverse("user_profile", args=[current_user, 1]))
            except Profile_details.DoesNotExist:
                user_profile_to_set = Profile_details(user= current_user, avatar_pic= content)
                user_profile_to_set.save()
                return redirect (reverse("user_profile", args=[current_user, 1]))
                
        
def like_post (request, post_id):
    if request.method == "POST":
        post_liked= Post.objects.get(pk=post_id)
        user= request.user
        post_liked.liked_by.add(user)
        num_likes= post_liked.liked_by.count()
            
        return JsonResponse({"msg":"liked", "num_of_likes": num_likes})


def unlike_post (request, post_id):
    post_unlike= Post.objects.get(pk=post_id)
    user= request.user
    if request.method == "DELETE":
        if user in post_unlike.liked_by.all():
            post_unlike.liked_by.remove(user)
        
        num_likes= post_unlike.liked_by.count() 
        return JsonResponse({"msg":"Unliked", "num_of_likes": num_likes})


def edit_post(request, post_id):
    if request.method == "PUT":
        updated_content= json.loads(request.body)
        post_to_edit= Post.objects.get(pk=post_id)
        post_to_edit.content= updated_content["content"]
        post_to_edit.save()
        return JsonResponse ({"message":"Edited successfully", "new_content": updated_content["content"]})
        

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
