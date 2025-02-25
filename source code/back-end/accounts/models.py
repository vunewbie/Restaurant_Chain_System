from establishments.models import Branch, Department

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Tên đăng nhập không được để trống')
        if not email:
            raise ValueError('Email không được để trống')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)

        if password:
            user.set_password(password) # Create user through registration form
        else:
            user.set_unusable_password() # Create user through social authentication
        user.save(using=self._db)

        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    # username, password, email, date_joined are inherited from AbstractUser
    # additonal fields
    phone_number = PhoneNumberField(unique=True, null=True, default=None)
    citizen_id = models.CharField(max_length=12, unique=True, null=True, default=None)
    full_name = models.CharField(max_length=100, blank=True, null=True, default=None)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], default='M')
    date_of_birth = models.DateField(null=True, default=None)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/default_avatar.jpg')
    is_active = models.BooleanField(default=True)
    type = models.CharField(max_length=1, choices=[('A', 'Admin'), ('C', 'Customer'), ('E', 'Employee'), ('M', 'Manager')], default='C')

    # removed fields
    first_name = None
    last_name = None

    # custom user manager
    objects = CustomUserManager()

    # remove is_staff and is_superuser fields but still use them as properties for admin panel
    @property
    def is_staff(self):
        return self.type in ['A', 'E', 'M']
    @property
    def is_superuser(self):
        return self.type == 'A'
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = 'User'

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    resignation_date = models.DateField(null=True, default=None)
    address = models.CharField(max_length=300)
    years_of_experience = models.IntegerField(validators=[MinValueValidator(0)])
    salary = models.IntegerField(validators=[MinValueValidator(0)])

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.full_name
    
    class Meta:
        db_table = 'Manager'

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    resignation_date = models.DateField(null=True, default=None)
    address = models.CharField(max_length=300)

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.full_name
    
    class Meta:
        db_table = 'Employee'

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    culmulative_points = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    total_points = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    tier = models.CharField(max_length=10, choices=[('M', 'Membership'), ('S', 'Silver'), ('G', 'Gold')], default='M')
    last_tier_update = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.full_name
    
    class Meta:
        db_table = 'Customer'
    
