from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Sum, Q

from .forms import InvoiceForm
from .models import Invoice, DailyTotal


def index(request):
    return render(request, 'invoicer/index.html')  # Adjust this based on your project structure

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Log in the user after successful registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)

            # Redirect to the login page
            login_url = reverse('login')  # 'login' should be the name of your login URL pattern
            return redirect(login_url)
    else:
        form = UserCreationForm()

    return render(request, 'invoicer/register.html', {'form': form})


def dashboard_view(request):
    user_id = request.user.id
    return render(request, 'invoicer/dashboard.html', {'user_id': user_id})


# @login_required
# def create_invoice_view(request):
#     if request.method == 'POST':
#         form = InvoiceForm(request.POST)
#         if form.is_valid():
#             # Process the form data and save the invoice
#             invoice = form.save(commit=False)
#             invoice.user = request.user  # Set the creator's user ID
#             invoice.save()
#             messages.success(request, 'Invoice created successfully.')
#             return redirect('dashboard')  # Adjust the redirect URL
#     else:
#         form = InvoiceForm()

#     return render(request, 'invoicer/create_invoice.html', {'form': form})

from django.http import JsonResponse

@login_required
def create_invoice_view(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            # Process the form data and save the invoice
            invoice = form.save(commit=False)
            invoice.user = request.user  # Set the creator's user ID
            invoice.save()
            # Return a JSON response indicating success
            return JsonResponse({'success': True, 'message': 'Invoice created successfully.'})
    else:
        form = InvoiceForm()

    return render(request, 'invoicer/create_invoice.html', {'form': form})


from .models import DailyTotal

@login_required
def view_invoices(request):
    # Get the search query from the request GET parameters
    query = request.GET.get('q', '')

    # Fetch invoices for both the creator and the recipient
    user_invoices = Invoice.objects.filter(Q(user=request.user) | Q(manual_user_id=request.user.id))

    # Apply search query filtering
    user_invoices = user_invoices.filter(
        Q(invoice_number__icontains=query) | Q(description__icontains=query)
    )

    # Get the current date
    today = timezone.now().date()
    current_month = today.month
    current_day = today.day

    # Get or create DailyTotal instance for the current user
    daily_total, created = DailyTotal.objects.get_or_create(user=request.user)

    # Check if the current day is different from the last calculated day
    if current_day != daily_total.last_calculated_day:
        # Reset the daily totals and update the last calculated day in the database
        daily_total.total_amount_day = 0
        daily_total.last_calculated_day = current_day
        daily_total.save()

    # Calculate total amount for the day
    total_amount_day = user_invoices.filter(date_created__date=today).aggregate(Sum('amount'))['amount__sum'] or 0

    # Calculate total monthly amount
    this_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    total_amount_month = user_invoices.filter(date_created__gte=this_month).aggregate(Sum('amount'))['amount__sum'] or 0

    # Update the daily total in the database
    daily_total.total_amount_day = total_amount_day
    daily_total.save()

    return render(request, 'invoicer/view_invoices.html', {
        'invoices': user_invoices,
        'query': query,
        'total_amount_day': total_amount_day,
        'total_amount_month': total_amount_month,
    })



@login_required
def edit_invoice_view(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id, user=request.user)

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            # Add success message if needed
    else:
        form = InvoiceForm(instance=invoice)

    return render(request, 'invoicer/edit_invoice.html', {'form': form, 'invoice': invoice})


def user_sales_report(request):
    user_id = request.GET.get('user_id')
    invoices = None
    total_amount_day = None
    total_amount_month = None

    if user_id:
        # Fetch invoices for the specified user
        invoices = Invoice.objects.filter(user_id=user_id)
        
        # Calculate daily total
        today = timezone.now().date()
        total_amount_day = invoices.filter(date_created__date=today).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Calculate monthly total
        this_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        total_amount_month = invoices.filter(date_created__gte=this_month).aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'invoicer/user_sales_report.html', {
        'invoices': invoices,
        'total_amount_day': total_amount_day,
        'total_amount_month': total_amount_month,
        'user_id': user_id,
    })