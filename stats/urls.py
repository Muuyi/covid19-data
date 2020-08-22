from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name='stats/login.html'),name='login'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('datatables-data/',views.DataTableView.as_view(),name='datatables-data'),
    path('activate/<uidb64>/<token>', views.AccountActivateView.as_view(),name='activate')
    # path('data-upload', views.data_upload,name="data_upload")
]