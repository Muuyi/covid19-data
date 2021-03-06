from django.shortcuts import render,redirect
from . models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import UserRegisterForm,CsvForm
from django.views import View
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
import csv,io
from decimal import Decimal
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from . utils import generate_token
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
# Create your views here.
class LoginView(View):
    def get(self,request):
        return render(request,'stats/login.html')
#Registration
class RegistrationView(View):
    def get(self,request):
        form = UserRegisterForm()
        return render(request,'stats/register.html',{'form':form})
    def post(self,request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if not User.objects.filter(email=email).exists():
            if len(password) < 6:
                messages.error(request,'Password is too short')
                return render(request,'stats/register.html')
            user = User.objects.create_user(username=username,email=email)
            user.set_password(password)
            user.is_active = False
            user.save()
            email_subject = "Activate your account"
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            link = reverse('activate',kwargs={'uidb64':uidb64,'token':generate_token.make_token(user)})
            current_site = get_current_site(request).domain
            activate_url = 'http://'+current_site+link
            email_body = 'Hi '+user.username+'\n Please click the link below to activate your account \n'+activate_url
            email_send = EmailMessage(
                email_subject,
                email_body,
                'noreply@muuyiandrew.com',
                [email]
            )
            email_send.send(fail_silently=False)
            messages.info(request, f'Your account has been successfully created!Login to your email address to activate your account')
            return redirect('login')
        else:
            messages.warning(request, f'This email already exists! Please use another email')
            return redirect('register')
#Dashboard
@login_required
def dashboard(request):
    dt = CovidData.objects.all()[0:100]
    form = CsvForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvForm()
        obj = CsvFile.objects.latest("uploaded_time")
        with open(obj.file_name.path, 'r') as f:
            reader = csv.reader(f)
            for i,column in enumerate(reader):
                if i == 0:
                    pass
                # elif i<10:
                #     print(column)
                # else:
                #     break;
                else:
                    CovidData.objects.update_or_create(
                        iso_code = column[0],
                        continent = column[1],
                        location = column[2],
                        date = column[3],
                        total_cases = int(float('0'+column[4])),	
                        new_cases = column[5],		
                        new_cases_smoothed = column[6],	
                        total_deaths = int(float('0'+column[7])),	
                        new_deaths = int(float('0'+column[8])),	
                        new_deaths_smoothed = Decimal('0'+column[9]),	
                        total_cases_per_million	= Decimal('0'+column[10]),
                        new_cases_per_million = Decimal('0'+column[11]),
                        new_cases_smoothed_per_million = Decimal('0'+column[12]),	
                        total_deaths_per_million = Decimal('0'+column[13]),	
                        new_deaths_per_million = Decimal('0'+column[14]),	
                        new_deaths_smoothed_per_million = Decimal('0'+column[15]),	
                        new_tests = int(float('0'+column[16])),	
                        total_tests = int(float('0'+column[17])),
                        total_tests_per_thousand = Decimal('0'+column[18]),	
                        new_tests_per_thousand = Decimal('0'+column[19]),	
                        new_tests_smoothed = Decimal('0'+column[20]),	
                        new_tests_smoothed_per_thousand = Decimal('0'+column[21]),	
                        tests_per_case = int(float('0'+column[22])), 	
                        positive_rate = Decimal('0'+column[23]),	
                        tests_units = column[24],	
                        stringency_index = Decimal('0'+column[25]),	
                        population = int(float('0'+column[26])),	
                        population_density = Decimal('0'+column[27]),	
                        median_age = Decimal('0'+column[28]),	
                        aged_65_older = Decimal('0'+column[29]),	
                        aged_70_older = Decimal('0'+column[30]),
                        gdp_per_capita = Decimal('0'+column[31]),	
                        extreme_poverty = Decimal('0'+column[32]),
                        cardiovasc_death_rate = Decimal('0'+column[33]),	
                        diabetes_prevalence = Decimal('0'+column[34]),	
                        female_smokers = int(float('0'+column[35])),	
                        male_smokers = int(float('0'+column[36])),	
                        handwashing_facilities = int(float('0'+column[37])),	
                        hospital_beds_per_thousand = Decimal('0'+column[38]),	
                        life_expectancy = Decimal('0'+column[39])
                    )
    return render(request, 'stats/dashboard.html',{'form':form,'dt':dt})
#ACTIVATE ACCOUNT VIEW
class AccountActivateView(View):
    def get(sef,request,uidb64,token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if not generate_token.check_token(user,token):
                messages.info(request,'Your account is already activated!Login to continue!')
                return redirect('login')
        except Exception as e:
            user = None
        if user is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
            messages.success(request,'Account activated successfully!Login to continue!')
            return redirect('login')
        return render(request,'stats/activate_failed.html',status=401)
##DATATABLE VIEW
class DataTableView(BaseDatatableView):
    model = CovidData
    columns = ['iso_code','continent','location','date','total_cases','new_cases','new_cases_smoothed','total_deaths','new_deaths','new_deaths_smoothed','total_cases_per_million','new_cases_per_million','new_cases_smoothed_per_million','total_deaths_per_million','new_deaths_per_million','new_deaths_smoothed_per_million','new_tests','total_tests','total_tests_per_thousand','new_tests_per_thousand','new_tests_smoothed','new_tests_smoothed_per_thousand','tests_per_case','positive_rate','tests_units','stringency_index','population','population_density','median_age','aged_65_older','aged_70_older','gdp_per_capita','extreme_poverty','cardiovasc_death_rate','diabetes_prevalence','female_smokers','male_smokers','handwashing_facilities','hospital_beds_per_thousand','life_expectancy']
    order_columns = ['iso_code','continent','location','date','total_cases','new_cases','new_cases_smoothed','total_deaths','new_deaths','new_deaths_smoothed','total_cases_per_million','new_cases_per_million','new_cases_smoothed_per_million','total_deaths_per_million','new_deaths_per_million','new_deaths_smoothed_per_million','new_tests','total_tests','total_tests_per_thousand','new_tests_per_thousand','new_tests_smoothed','new_tests_smoothed_per_thousand','tests_per_case','positive_rate','tests_units','stringency_index','population','population_density','median_age','aged_65_older','aged_70_older','gdp_per_capita','extreme_poverty','cardiovasc_death_rate','diabetes_prevalence','female_smokers','male_smokers','handwashing_facilities','hospital_beds_per_thousand','life_expectancy']
    max_display_length = 500

    def filter_queryset(self, qs):
            # use parameters passed in GET request to filter queryset

        # simple example:
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(iso_code__icontains=search) | Q(continent__icontains=search) | Q(location__icontains=search) | Q(date__icontains=search) | Q(total_cases__icontains=search) | Q(new_cases__icontains=search))
        return qs