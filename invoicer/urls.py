# yourappname/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import view_invoices, register_view, dashboard_view, create_invoice_view, edit_invoice_view, user_sales_report
from invoicer import views

app_name = 'invoicer'

urlpatterns = [
    # ... your other views and URLs ...
    path('', views.index, name='invoicer/index'),  # Add this line with your desired view
    path('register/', register_view, name='register'),
    # Authentication URLs using Django's built-in views
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('create_invoice/', create_invoice_view, name='create_invoice'),
    path('view_invoices/', view_invoices, name='view_invoices'),
    path('edit_invoice/<int:invoice_id>/', edit_invoice_view, name='edit_invoice'),
    path('user-sales-report/', user_sales_report, name='user_sales_report'),

   
    # ... other custom URLs ...
]
