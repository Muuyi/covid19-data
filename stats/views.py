from django.shortcuts import render,redirect
from . models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import UserRegisterForm

# Create your views here.
def index(request):
    context = {
        # 'data' : CovidData.objects.all()
    }
    return render(request,'stats/index.html',context)
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f'Account created for { username}!')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'stats/register.html',{'form':form})
