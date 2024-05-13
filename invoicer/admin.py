from django.contrib import admin

# Register your models here
from .models import UserProfile, Invoice, DailyTotal

admin.site.register(UserProfile)
admin.site.register(Invoice)
admin.site.register(DailyTotal)

