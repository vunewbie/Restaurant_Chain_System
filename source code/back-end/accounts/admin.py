from .models import *
from django.contrib import admin

# custom display for User in admin panel
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'citizen_id', 'full_name', 'is_active', 'type')
                    
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'branch')

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'branch')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'cumulative_points', 'total_points', 'tier', 'last_tier_update')
