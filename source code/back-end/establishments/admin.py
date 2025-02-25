from django.contrib import admin
from .models import *

# Customizing the admin interface
@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('district', 'city')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'formatted_salary')

    def formatted_salary(self, obj):
        return f"{obj.salary:,.0f}".replace(",", ".")
    formatted_salary.short_description = 'Salary'

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'opening_time', 'closing_time', 'phone_number', 'car_parking_lot', 'motorbike_parking_lot', 'area')

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('branch', 'table_number', 'number_of_seats', 'status')
