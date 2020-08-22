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
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email = user.email
            email_subject = "Activate your account"
            msg = render_to_string('stats/activate.html',
                {
                    'user':user,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':generate_token.make_token(user)
                }
            )
            email_body = ''
            email_send = EmailMessage(
                email_subject,
                msg,
                'noreply@muuyiandrew.com',
                [email]
            )
            email_send.send()
            messages.success(request, f'Your account has been successfully created! You can now login')
            return redirect('login')
        else:
            form = UserRegisterForm()
        return render(request, 'stats/register.html',{'form':form})
#Dashboard
@login_required
def dashboard(request):
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
                        new_cases = int(float('0'+column[5])),		
                        new_cases_smoothed = Decimal('0'+column[6]),	
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
    return render(request, 'stats/dashboard.html',{'form':form})
#ACTIVATE ACCOUNT VIEW
class AccountActivateView(View):
    def get(sef,request,uidb64,token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as e:
            user = None
        if ser is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
            messages.info(request,'Account activated successfully!Login to continue!')
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
            qs = qs.filter(name__istartswith=search)

        # more advanced example using extra parameters
        filter_customer = self.request.GET.get('customer', None)

        if filter_customer:
            customer_parts = filter_customer.split(' ')
            qs_params = None
            for part in customer_parts:
                q = Q(customer_firstname__istartswith=part)|Q(customer_lastname__istartswith=part)
                qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
        return qs