from django.shortcuts import render,redirect
from . models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage

# Create your views here.
def index(request):
    context = {
        # 'data' : CovidData.objects.all()
    }
    return render(request,'stats/login.html',context)
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            email = form.cleaned_data("email")
            email_subject = "Activate your account"
            email_body = ''
            email_send = EmailMessage(
                email_subject,
                email_body,
                'noreply@covid19data.com',
                [email]
            )
            messages.success(request, f'Your account has been successfully created! You can now login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'stats/register.html',{'form':form})
@login_required
def dashboard(request):
    return render(request, 'stats/dashboard.html')
