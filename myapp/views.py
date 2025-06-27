from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login

# Create your views here.
def home(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        
    else:
            form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form':form})

# def login(request):
#     return render(request, 'login.html')