from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.text import slugify

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

from .models import Etkinlik

class EtkinlikForm(forms.ModelForm):
    class Meta:
        model = Etkinlik
        fields = ['title', 'isActive', 'date', 'description', 'adress', 'category', 'image']

    def save(self, commit=True):
        instance = super(EtkinlikForm, self).save(commit=False)
        instance.slug = slugify(instance.title)  # Başlıktan slug oluştur
        if commit:
            instance.save()
        return instance
