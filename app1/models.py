from django.db import models
from django.contrib.auth.hashers import make_password

# class User(models.Model):
#     USER_TYPES = [
#         ('admin', 'Admin'),
#         ('partner', 'Partner'),
#         ('individual', 'Individual'),
#     ]

#     user_id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=50, unique=True)
#     password = models.CharField(max_length=255)  # Hashed password
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=15, unique=True)
#     full_name = models.CharField(max_length=100)
#     user_type = models.CharField(max_length=20, choices=USER_TYPES)  # Defines the type of user
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

    

    

#     def set_password(self, raw_password):
#         self.password = make_password(raw_password)
#         self.save()
#     def __str__(self):
#         return f"self.user_id"

    
class User(models.Model):
    USER_TYPES = [
        ('admin', 'Admin'),
        ('partner', 'Partner'),
        ('individual', 'Individual'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # Hashed password
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)  # Defines the type of user
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')  # Active or Inactive
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def __str__(self):
        return f"{self.user_id} - {self.username} - {self.status}"


class Asset(models.Model):
    ASSET_TYPES = [
        ("land", "Land"),
        ("apartment", "Apartment"),
        ("house", "House"),
        ("commercial", "Commercial Property"),
    ]

    asset_id = models.AutoField(primary_key=True)
    asset_name = models.CharField(max_length=255)
    asset_type = models.CharField(max_length=50, choices=ASSET_TYPES)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    owner_id = models.IntegerField()  # Foreign key (Admin/Partner/Individual) - Handle in API
    owner_type = models.CharField(max_length=20)  # "admin", "partner", "individual"
    asset_image = models.ImageField(upload_to="assets/", null=True, blank=True)  # Image Upload
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "self.asset_id"
    
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("buy", "Buy"),
        ("sell", "Sell"),
        ("rent", "Rent"),
        ("lease", "Lease"),
    ]

    transaction_id = models.AutoField(primary_key=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    buyer_id = models.IntegerField()  # Can be Admin/Partner/Individual
    buyer_type = models.CharField(max_length=20)  # "admin", "partner", "individual"
    seller_id = models.IntegerField()
    seller_type = models.CharField(max_length=20)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"self.transaction_id"
