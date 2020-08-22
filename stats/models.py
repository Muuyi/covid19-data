from django.db import models

# Create your models here.
class CsvFile(models.Model):
    file_name = models.FileField(upload_to='csvs')
    uploaded_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.file_name
class CovidData(models.Model):
    iso_code = models.CharField(max_length=255,null=True)
    continent = models.CharField(max_length=255,null=True)
    location = models.CharField(max_length=255,null=True)
    date = models.DateField(null=True)
    total_cases = models.IntegerField(null=True)	
    new_cases = models.IntegerField(null=True)		
    new_cases_smoothed = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    total_deaths = models.IntegerField(null=True)	
    new_deaths = models.IntegerField(null=True)	
    new_deaths_smoothed = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    total_cases_per_million	= models.DecimalField(max_digits=20,decimal_places=4,null=True)
    new_cases_per_million = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    new_cases_smoothed_per_million = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    total_deaths_per_million = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    new_deaths_per_million = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    new_deaths_smoothed_per_million = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    new_tests = models.IntegerField(null=True)	
    total_tests = models.IntegerField(null=True)	
    total_tests_per_thousand = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    new_tests_per_thousand = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    new_tests_smoothed = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    new_tests_smoothed_per_thousand = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    tests_per_case = models.IntegerField(null=True) 	
    positive_rate = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    tests_units = models.CharField(max_length=255,null=True)	
    stringency_index = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    population = models.IntegerField(null=True)	
    population_density = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    median_age = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    aged_65_older = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    aged_70_older = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    gdp_per_capita = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    extreme_poverty = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    cardiovasc_death_rate = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    diabetes_prevalence = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    female_smokers = models.IntegerField(null=True)	
    male_smokers = models.IntegerField(null=True)	
    handwashing_facilities = models.IntegerField(null=True)	
    hospital_beds_per_thousand = models.DecimalField(max_digits=20,decimal_places=4,null=True)	
    life_expectancy = models.DecimalField(max_digits=20,decimal_places=4,null=True)
    def __str__(self):
        return self.date
    class Meta:
        ordering = ['date']
