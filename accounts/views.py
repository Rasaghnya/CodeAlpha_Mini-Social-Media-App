from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from .forms import ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            Profile.objects.get_or_create(user=user)  # Create profile if it doesn't exist
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def view_profile(request):
    return render(request, 'accounts/view_profile.html',{'profile': request.user.profile})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def follow_user(request, user_id):
    profile_to_follow = get_object_or_404(Profile, id=user_id)
    if request.user == profile_to_follow.user:
        return redirect('view_profile')  # Can't follow yourself
    if request.user in profile_to_follow.followers.all():
        profile_to_follow.followers.remove(request.user)
    else: 
        profile_to_follow.followers.add(request.user)
    return redirect('profile_detail', user_id=user_id)

@login_required
def profile_detail(request, user_id):
    profile = get_object_or_404(Profile, id=user_id)
    is_following = request.user in profile.followers.all()
    return render(request, 'accounts/profile_detail.html', {'profile': profile, 'is_following': is_following})