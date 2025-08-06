from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserProfileForm

def register(request):
    """Foydalanuvchi ro'yxatdan o'tish"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            
            # UserProfile allaqachon signal orqali yaratilgan, uni yangilaymiz
            user.userprofile.phone_number = profile_form.cleaned_data['phone_number']
            user.userprofile.bio = profile_form.cleaned_data['bio']
            user.userprofile.save()
            
            # Avtomatik login
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, 'Muvaffaqiyatli ro\'yxatdan o\'tdingiz!')
            return redirect('courses:course_list')
    else:
        form = UserCreationForm()
        profile_form = UserProfileForm()
    
    context = {
        'form': form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/register.html', context)

def profile(request):
    """Foydalanuvchi profili"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil muvaffaqiyatli yangilandi!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/profile.html', context)
