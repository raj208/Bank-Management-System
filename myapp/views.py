from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Account
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from decimal import Decimal


# Create your views here.
def home(request):
    return render(request, 'home.html')


def dashboard(request):
    account, created = Account.objects.get_or_create(user=request.user)
    balance = account.balance
    return render(request, 'dashboard.html', {'balance': balance})




def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')
        
    else:
            form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form':form})



@login_required
def deposit_view(request):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        account = Account.objects.get(user=request.user)
        account.deposit(amount)
        messages.success(request, f'Successfully deposited ${amount:.2f}')
        return redirect('dashboard')  # change to your destination
    return render(request, 'deposit.html')
    # return render(request, 'deposit.html')


@login_required
def withdraw_view(request):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        account = Account.objects.get(user=request.user)
        if account.withdraw(amount):
            messages.success(request, f'Successfully withdrew ${amount:.2f}')
        else:
            messages.error(request, 'Insufficient balance.')
        return redirect('dashboard')
    return render(request, 'withdraw.html')
