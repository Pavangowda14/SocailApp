from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Post, Likepost, Followers
from django.contrib.auth.decorators import login_required
from itertools import chain
import random


@login_required(login_url="signin")
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = Followers.objects.filter(follower=request.user.username)

    for user in user_following:
        user_following_list.append(user)

    for username in user_following_list:
        feed_list = Post.objects.filter(user=username)
        feed.append(feed_list)

    feeds = list(chain(*feed))

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [
        x for x in list(all_users) if (x not in list(user_following_all))
    ]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [
        x for x in list(new_suggestions_list) if (x not in list(current_user))
    ]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(
        request,
        "index.html",
        {
            "user_profile": user_profile,
            "posts": feeds,
            "suggestions_username_profile_list": suggestions_username_profile_list,
        },
    )


@login_required(login_url="signin")
def likepost(request):
    username = request.user.username
    post_id = request.GET.get("post_id")

    post = Post.objects.get(id=post_id)

    like_filter = Likepost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = Likepost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes += 1
        post.save()
        return redirect("/")
    else:
        like_filter.delete()
        post.no_of_likes -= 1
        post.save()
        return redirect("/")


@login_required(login_url="signin")
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_posts_length = len(user_posts)

    follower = request.user.username
    user = pk

    if Followers.objects.filter(follower=follower, user=user).first():
        button_text = "unfollow"
    else:
        button_text = "follow"

    followers = len(Followers.objects.filter(user=pk))
    following = len(Followers.objects.filter(follower=pk))

    context = {
        "user_object": user_object,
        "user_profile": user_profile,
        "user_posts": user_posts,
        "user_posts_length": user_posts_length,
        "button_text": button_text,
        "followers": followers,
        "following": following,
    }
    return render(request, "profile.html", context)


@login_required(login_url="signin")
def follow(request):
    if request.method == "POST":
        follower = request.POST["follower"]
        user = request.POST["user"]

        if Followers.objects.filter(follower=follower, user=user).first():
            delete_follower = Followers.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect("/profile/" + user)
        else:
            new_follower = Followers.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect("/profile/" + user)
    else:
        return redirect("/")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmpassword = request.POST["ConfirmPassword"]

        if password == confirmpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username Exist")
                return redirect("signup")
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()

                auth.login(request, user)

                # Check if the user is active
                if user.is_active:
                    # Create a profile for the user
                    new_profile = Profile.objects.create(user=user, id_user=user.id)
                    new_profile.save()
                    return redirect("setting")
                else:
                    messages.error(request, "User is not active")
                    return redirect("signup")
        else:
            messages.error(request, "Passwords do not match")
            return redirect("signup")
    else:
        return render(request, "signup.html")


@login_required(login_url="signin")
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == "POST":
        username = request.POST["username"]
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for user in username_object:
            username_profile.append(user.id)

        for id in username_profile:
            profile_list = Profile.objects.filter(id_user=id)
            username_profile_list.append(profile_list)

        username_profile_list = list(chain(*username_profile_list))

    return render(
        request,
        "search.html",
        {"user_profile": user_profile, "username_profile_list": username_profile_list},
    )


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.error(request, "user not found")
            return redirect("signin")
    else:
        return render(request, "signin.html")


@login_required(login_url="signin")
def custom_logout(request):
    auth.logout(request)
    return redirect("signin")


@login_required(login_url="signin")
def setting(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        if request.FILES.get("image") == None:
            image = user_profile.profileimg

        if request.FILES.get("image") != None:
            image = request.FILES.get("image")

        bio = request.POST["bio"]
        location = request.POST["location"]

        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return redirect("setting")

    return render(request, "setting.html", {"user_profile": user_profile})


@login_required(login_url="signin")
def upload(request):
    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get("upload_image")
        caption = request.POST["caption"]

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect("/")
    return redirect("/")
