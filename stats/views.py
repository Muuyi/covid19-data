from django.shortcuts import render,redirect
from . models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import UserRegisterForm,CsvForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
import csv,io
from decimal import Decimal
# Create your views here.
def index(request):
    context = {
        # 'data' : CovidData.objects.all()
    }
    return render(request,'stats/login.html',context)
#Registration
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
                        total_cases = column[4],	
                        new_cases = column[5],		
                        new_cases_smoothed = Decimal(column[6]),	
                        total_deaths = column[7],	
                        new_deaths = column[8],	
                        new_deaths_smoothed = Decimal(column[9]),	
                        total_cases_per_million	= Decimal(column[10]),
                        new_cases_per_million = Decimal(column[11]),
                        new_cases_smoothed_per_million = Decimal(column[12]),	
                        total_deaths_per_million = column[13],	
                        new_deaths_per_million = Decimal(column[14]),	
                        new_deaths_smoothed_per_million = Decimal(column[15]),	
                        new_tests = column[16],	
                        total_tests = column[17],
                        total_tests_per_thousand = Decimal(column[18]),	
                        new_tests_per_thousand = Decimal(column[19]),	
                        new_tests_smoothed = Decimal(column[20]),	
                        new_tests_smoothed_per_thousand = Decimal(column[21]),	
                        tests_per_case = column[22], 	
                        positive_rate = Decimal(column[23]),	
                        tests_units = column[24],	
                        stringency_index = Decimal(column[25]),	
                        population = column[26],	
                        population_density = Decimal(column[27]),	
                        median_age = Decimal(column[28]),	
                        aged_65_older = Decimal(column[29]),	
                        aged_70_older = Decimal(column[30]),
                        gdp_per_capita = Decimal(column[31]),	
                        extreme_poverty = Decimal(column[32]),
                        cardiovasc_death_rate = Decimal(column[33]),	
                        diabetes_prevalence = Decimal(column[34]),	
                        female_smokers = column[35],	
                        male_smokers = column[36],	
                        handwashing_facilities = column[37],	
                        hospital_beds_per_thousand = Decimal(column[38]),	
                        life_expectancy = Decimal(column[39])
                    )
    return render(request, 'stats/dashboard.html',{'form':form})
#UPLOAD CSV
# def data_upload(request):
#     form = CsvForm(request.POST or None, request.FILES or None)
#     # template = 'dashboard.html'
#     # csv_file = request.FILES['file']
#     # if not csv_file.name.endswith('.csv'):
#     #     messages.error[request,'This is not a csv file']
#     # data_set = csv_file.read().decode('UTF-8')
#     # io_string = io.StringIO(data_set)
#     # next(io_string)
#     # for column in csv.reader[io_string, delimiter=",", quotechar="|"];
#     # _, created = CovidData.objects.update_or_create[
#     #     iso_code = column[0]
#     #     continent = column[1]
#     #     location = column[2]
#     #     date = column[3]
#     #     total_cases = column[4]	
#     #     new_cases = column[5]		
#     #     new_cases_smoothed = column[6]	
#     #     total_deaths = column[7]	
#     #     new_deaths = column[8]	
#     #     new_deaths_smoothed = column[9]	
#     #     total_cases_per_million	= column[10]
#     #     new_cases_per_million = column[11]
#     #     new_cases_smoothed_per_million = column[12]	
#     #     total_deaths_per_million = column[13]	
#     #     new_deaths_per_million = column[14]	
#     #     new_deaths_smoothed_per_million = column[15]	
#     #     new_tests = column[16]	
#     #     total_tests = column[17]
#     #     total_tests_per_thousand = column[18]	
#     #     new_tests_per_thousand = column[19]	
#     #     new_tests_smoothed = column[20]	
#     #     new_tests_smoothed_per_thousand = column[21]	
#     #     tests_per_case = column[22] 	
#     #     positive_rate = column[23]	
#     #     tests_units = column[24]	
#     #     stringency_index = column[25]	
#     #     population = column[26]	
#     #     population_density = column[27]	
#     #     median_age = column[28]	
#     #     aged_65_older = column[29]	
#     #     aged_70_older = column[30]
#     #     gdp_per_capita = column[31]	
#     #     extreme_poverty = column[32]
#     #     cardiovasc_death_rate = column[33]	
#     #     diabetes_prevalence = column[34]	
#     #     female_smokers = column[35]	
#     #     male_smokers = column[36]	
#     #     handwashing_facilities = column[37]	
#     #     hospital_beds_per_thousand = column[38]	
#     #     life_expectancy = column[39]
#     # ]
#     # context = {}
#     return render(request,'stats/dashboard.html',{'form':form})
