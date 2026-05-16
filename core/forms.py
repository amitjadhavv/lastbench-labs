from django import forms
from django.contrib.auth.models import User
from .models import Profile, Skill

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password_confirm(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password_confirm')
        if p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return p2

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'experience_years', 'portfolio_url', 'github_url', 'linkedin_url', 'skills']
        widgets = {
            'skills': forms.CheckboxSelectMultiple(),
        }
