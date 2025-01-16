from django.db import models
from django.conf import settings

# Create your models here.

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    phone_number = models.CharField(max_length=15, unique=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Changed related_name here
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customuser',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Changed related_name here
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )

    def __str__(self):
        return self.username



class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.state}"



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Shipped', 'Shipped')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    razorpay_payment_id = models.CharField(max_length=255)
    razorpay_order_id = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=50, choices=[('Success', 'Success'), ('Failed', 'Failed'), ('Pending', 'Pending'),])
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.payment_status}"





class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


    
class Product(models.Model):
    product_name = models.CharField(max_length=255, default='Unnamed Product')
    name = models.CharField(max_length=100, default='Unnamed Product')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(default='No description available')
    created_at = models.DateTimeField(auto_now_add=True)
    product_description = models.TextField(default='No product description')
    price = models.FloatField(default=0.00)
    category_name = models.ManyToManyField(Category, default=None)  # Can be an empty list if no categories are assigned
    brand = models.CharField(max_length=255, default='N/A')
    color = models.CharField(max_length=50, default='N/A')
    size = models.CharField(max_length=50, default='N/A')
    quantity = models.IntegerField(default=0)
    availability = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)
    reviews = models.IntegerField(default=0)
    expiry_date = models.DateField(default='2025-01-01')  # Set a sensible default date
    shipping_cost = models.FloatField(default=0.0)
    seller_name = models.CharField(max_length=255, default='Unknown Seller')
    seller_rating = models.FloatField(default=0.0)

    image = models.CharField(max_length=255,  default='products/default.jpg') 


    def __str__(self):
        return self.name
    








    

from django.db import models

class Orders(models.Model):
    customer_name = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=20, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')])
    is_fulfilled = models.BooleanField(default=False)
    issue_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('resolved', 'Resolved')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"


