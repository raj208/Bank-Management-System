from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SendMoneyForm(forms.Form):
    receiver_username = forms.CharField(max_length=150)
    amount = forms.DecimalField(min_value=0.01, max_digits=12, decimal_places=2)
