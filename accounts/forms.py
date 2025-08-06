from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'avatar', 'bio']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': '+998 XX XXX XX XX'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'O\'zingiz haqida...'}),
        }
        labels = {
            'phone_number': 'Telefon raqami',
            'avatar': 'Avatar',
            'bio': 'Haqida',
        } 