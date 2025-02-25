from django.db import models
from django.contrib.auth.hashers import make_password

    
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
    KYC_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'), 
    ]


    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # Hashed password
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)  # Defines the type of user
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')  # Active or Inactive
    kyc_status = models.CharField(max_length=10, choices=KYC_STATUS_CHOICES, default='pending')  # Pending, Verified, Rejected
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def __str__(self):
        return f"{self.user_id}"


class Asset(models.Model):
    ASSET_TYPES = [
        ("land", "Land"),
        ("apartment", "Apartment"),
        ("house", "House"),
        ("commercial", "Commercial Property"),
    ]

    #asset_id = models.AutoField(primary_key=True)
    #asset_name = models.CharField(max_length=255)
    #asset_type = models.CharField(max_length=50, choices=ASSET_TYPES)
    #location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    owner_id = models.IntegerField(null=True)  # Foreign key (Admin/Partner/Individual) - Handle in API
    owner_type = models.CharField(max_length=20,null=True)  # "admin", "partner", "individual"
    asset_image = models.ImageField(upload_to="assets/", null=True, blank=True)  # Image Upload
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)


    # Basic Asset Information
    asset_id = models.AutoField(primary_key=True)
    asset_name = models.CharField(max_length=255,null=True)
    asset_type = models.CharField(max_length=50, choices=ASSET_TYPES,null=True)
    asset_code = models.CharField(max_length=50, unique=True,null=True)  # Asset Code/ID
    description = models.TextField(blank=True, null=True)

    # Purchase Details
    purchase_date = models.DateField(null=True)
    purchase_cost = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    vendor_supplier = models.CharField(max_length=255,null=True)
    invoice_number = models.CharField(max_length=100, unique=True,null=True)

    # Depreciation & Valuation
    depreciation_method = models.CharField(max_length=100,null=True)
    depreciation_rate = models.DecimalField(max_digits=5, decimal_places=2,null=True)  # In percentage
    useful_life_years = models.IntegerField(null=True)
    current_value = models.DecimalField(max_digits=15, decimal_places=2,null=True)

    # Location & Assignment
    location = models.CharField(max_length=255,null=True)
    department = models.CharField(max_length=255,null=True)
    assigned_to = models.CharField(max_length=255, blank=True, null=True)
    documents = models.FileField(upload_to="asset_documents/", blank=True, null=True)  # File Upload

    # Maintenance & Condition
    last_maintenance_date = models.DateField(blank=True, null=True)
    next_maintenance_due = models.DateField(blank=True, null=True)
    condition = models.CharField(max_length=255, blank=True, null=True)

    # Disposal Details
    disposal_date = models.DateField(blank=True, null=True)
    disposal_method = models.CharField(max_length=255, blank=True, null=True)
    disposal_value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

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
