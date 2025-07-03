from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, SendMoneyForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
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
    account = Account.objects.get(user=request.user)

    if account.is_frozen:
        messages.error(request, "Your account is frozen. Deposits are disabled.")
        return redirect('dashboard')


    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        account = Account.objects.get(user=request.user)
        account.deposit(amount)
        messages.success(request, f'Successfully deposited ${amount:.2f}')
        return redirect('dashboard')  
    return render(request, 'deposit.html')
    # return render(request, 'deposit.html')


@login_required
def withdraw_view(request):
    account = Account.objects.get(user=request.user)
    if account.is_frozen:
        messages.error(request, "Your account is frozen. Withdrawals are disabled.")
        return redirect('dashboard')

    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        account = Account.objects.get(user=request.user)
        if account.withdraw(amount):
            messages.success(request, f'Successfully withdrew ${amount:.2f}')
        else:
            messages.error(request, 'Insufficient balance.')
        return redirect('dashboard')
    return render(request, 'withdraw.html')


# from django.contrib.auth.decorators import user_passes_test

# def is_admin(user):
#     return user.is_authenticated and user.is_admin  # based on your custom User model

# @login_required
# @user_passes_test(is_admin)
# def all_users(request):
#     users = User.objects.all()
#     return render(request, 'all_users.html', {'users': users})

from django.contrib.auth import get_user_model
User = get_user_model()
@login_required
def send_money(request):
    if request.method == 'POST':
        form = SendMoneyForm(request.POST)
        if form.is_valid():
            receiver_username = form.cleaned_data['receiver_username']
            amount = form.cleaned_data['amount']

            try:
                receiver_user = User.objects.get(username=receiver_username)
                sender_account = Account.objects.get(user=request.user)
                receiver_account = Account.objects.get(user=receiver_user)

                if sender_account.balance < amount:
                    messages.error(request, "Insufficient balance.")
                elif receiver_user == request.user:
                    messages.error(request, "You cannot send money to yourself.")
                else:
                    # Perform transfer
                    sender_account.balance -= amount
                    receiver_account.balance += amount
                    sender_account.save()
                    receiver_account.save()

                    # Record transaction
                    Transaction.objects.create(
                        sender=request.user,
                        receiver=receiver_user,
                        amount=amount
                    )
                    messages.success(request, f"Sent ₹{amount} to {receiver_username}.")
                    return redirect('dashboard')  # or wherever your main page is
            except User.DoesNotExist:
                messages.error(request, "Recipient username does not exist.")
    else:
        form = SendMoneyForm()
    return render(request, 'send_money.html', {'form': form})