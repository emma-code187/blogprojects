from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponseRedirect
from .models import Profile
from django.urls import reverse

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			#password = form.cleaned_data.get('password1')
			#new_user = User.objects.create(username=username, password=password)
			#new_user.save()
			#profile = Profile(user=User.objects.get(username=username))
			#profile.save()
			messages.success(request, f'Your account has been created! You are now able to log in')
			return redirect('login') 
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form': form})

def signin(request):
	username = password = ''
	#if request.user.is_authenticated:
		#return render(request, 'index.html')
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			# Redirect to a success page.
			user = authenticate(request, username=username, password=password)
			print('needed')
			return redirect('profile')

	user = authenticate(request, username=username, password=password)
	print('wanted')
	return HttpResponseRedirect(reverse('login', args=()))

@login_required
def profile(request):
	user = request.user
	username = user.username
	email = user.email
	user.save()
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			user = user
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile') 
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
		context = {'u_form': u_form, 'p_form': p_form}
		return render(request, 'users/profile.html', context)
