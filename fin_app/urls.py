from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.fin_main_page),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='fin/login.html'), name='login'),
    path('expence/', views.expence, name='expence'),
    path('category/<slug:category_slug>/', views.r_cat, name='records_of_category'),
    path('create_record', views.add_record, name='create_record'),
    path('incomes/', views.income, name='income'),
    path('analysis/', views.analysis_view, name='analysis'),
    path('redactor/<int:record_id>/', views.edit_record, name='redactor'),
    path('logout/', auth_views.LogoutView.as_view(template_name='fin/logout.html'), name='logout'),






]
