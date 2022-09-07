from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfilePicUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feed-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request, username):
    # user = get_object_or_404(User, username=username)
    try:
        user = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        print("here")
        raise Http404
    is_this_user = user == request.user
    return render(request, 'users/profile.html', {'ouser': user, 'is_this_user': is_this_user})


@login_required
def toggle_follow(request, pk, action):
    if request.method != 'POST':
        return redirect('feed-home')
    ouser = get_object_or_404(User, pk=pk)
    user = request.user
    if action == 'follow':
        user.profile.following.add(ouser.profile)
        return JsonResponse({"success": True}, status=200)
    elif action == 'unfollow':
        user.profile.following.remove(ouser.profile)
        return JsonResponse({"success": True}, status=200)
    return JsonResponse({"success": False}, status=400)


@login_required
def edit(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        pic_form = ProfilePicUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid() and pic_form.is_valid():
            print(u_form.is_valid())
            u_form.save()
            p_form.save()
            pic_form.save()
            return redirect('profile-edit')
        else:
            print("invalid")
            print(request.user.username)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        pic_form = ProfilePicUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'pic_form': pic_form,
        'user': User.objects.get(pk=request.user.id)
    }
    return render(request, 'users/edit.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('change-password')
        else:
            print('invalid')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/passwordchange.html', {'form': form})