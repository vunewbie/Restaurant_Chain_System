from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

class Area(models.Model):
    district = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    unique_together = [['district', 'city']]

    def __str__(self):
        return f'{self.district}, {self.city}'
    
    class Meta:
        db_table = 'Area'

class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    salary = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Department'

class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=200, unique=True)
    opening_time = models.TimeField(default='08:00:00')
    closing_time = models.TimeField(default='23:00:00')
    phone_number = PhoneNumberField(unique=True)
    car_parking_lot = models.BooleanField(default=True)
    motorbike_parking_lot = models.BooleanField(default=True)

    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Branch'

class Table(models.Model):
    table_number = models.IntegerField(validators=[MinValueValidator(0)])
    number_of_seats = models.IntegerField(validators=[MinValueValidator(0)])
    status = models.CharField(max_length=10, choices = [('A', 'Available'), ('R', 'Reserved'), ('O', 'Occupied')], default='A')

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bàn số {self.table_number} của {self.branch.name}"
    
    unique_together = [['table_number', 'branch']]
    
    class Meta:
        db_table = 'Table'
