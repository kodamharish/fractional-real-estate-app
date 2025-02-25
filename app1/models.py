from django.db import models
from django.contrib.auth.hashers import make_password
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class UserType(models.Model):
    type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)  # Example: 'admin', 'partner', 'individual'

    def __str__(self):
        return self.name

class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)  # Example: 'active', 'inactive'

    def __str__(self):
        return self.name

class KYCStatus(models.Model):
    kyc_status_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)  # Example: 'pending', 'verified', 'rejected'

    def __str__(self):
        return self.name



def user_kyc_upload_path(instance, filename):
    """Generate a dynamic file path for user KYC documents based on user ID."""
    user_id = instance.user.user_id 
    return os.path.join("kyc_documents", str(user_id), filename)



class KYC(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="kyc_details")
    kyc_id = models.AutoField(primary_key=True)

    # PAN Card
    pan_number = models.CharField(max_length=10, unique=True, blank=True, null=True)  # Format: ABCDE1234F
    pan_pdf = models.FileField(upload_to=user_kyc_upload_path, blank=True, null=True)  # Upload PAN PDF

    # Aadhaar Card
    aadhaar_number = models.CharField(max_length=12, unique=True, blank=True, null=True)  # 12-digit Aadhaar
    aadhaar_pdf = models.FileField(upload_to=user_kyc_upload_path, blank=True, null=True)  # Upload Aadhaar PDF
    kyc_status = models.ForeignKey(KYCStatus, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}  ({self.kyc_status})"
    




def user_image_upload_path(instance, filename):
    """Save user image in a temp folder initially, then rename it after saving the user."""
    ext = filename.split('.')[-1]  # Get file extension
    return os.path.join("user_images", "temp", f"temp.{ext}")  # Store in temp first




class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # Store hashed password
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[("male", "Male"), ("female", "Female"), ("other", "Other")], null=True, blank=True)
    

    user_type = models.ForeignKey(UserType, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    kyc_status = models.ForeignKey(KYCStatus, on_delete=models.SET_NULL, null=True, blank=True)

    added_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="added_users")
    user_image = models.ImageField(upload_to=user_image_upload_path, blank=True, null=True)  # Custom path
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if it's a new user
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)  # Save user first to get user_id

        if is_new and self.user_image:  # Rename image after saving user_id
            ext = self.user_image.name.split('.')[-1]
            new_filename = f"{self.user_id}.{ext}"
            new_path = os.path.join("user_images", new_filename)

            # Move the file from temp to the correct path
            old_path = self.user_image.path
            if default_storage.exists(old_path):
                with default_storage.open(old_path, 'rb') as file_content:
                    default_storage.save(new_path, ContentFile(file_content.read()))
                default_storage.delete(old_path)  # Delete temp file

            # Update model to use new filename
            self.user_image.name = new_path
            super().save(update_fields=["user_image"])  # Save again with updated path

        

    def __str__(self):
        return f"{self.user_id}"

class BankDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="bank_details")
    bank_id = models.AutoField(primary_key=True)
    account_holder_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50, unique=True)
    ifsc_code = models.CharField(max_length=20)
    branch_name = models.CharField(max_length=255)
    upi_id = models.CharField(max_length=100, blank=True, null=True)  # Optional

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.bank_name} ({self.account_number})"







class AssetType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


def asset_image_upload_path(instance, filename):
    """Save asset image in a temp folder first."""
    ext = filename.split('.')[-1]  # Get file extension
    return os.path.join("asset_images", "temp", f"temp.{ext}")  # Store in temp first


def asset_document_upload_path(instance, filename):
    """Save asset document in a temp folder first."""
    ext = filename.split('.')[-1]  # Get file extension
    return os.path.join("asset_documents", "temp", f"temp.{ext}")  # Store in temp first


class Asset(models.Model):
    asset_id = models.AutoField(primary_key=True)
    asset_type = models.ForeignKey(AssetType, on_delete=models.SET_NULL, null=True)

    asset_name = models.CharField(max_length=255, null=True)
    asset_code = models.CharField(max_length=50, unique=True, null=True)
    description = models.TextField(blank=True, null=True)

    # Purchase Details
    purchase_date = models.DateField(null=True)
    purchase_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    vendor_supplier = models.CharField(max_length=255, null=True)
    invoice_number = models.CharField(max_length=100, unique=True, null=True)

    # Depreciation & Valuation
    depreciation_method = models.CharField(max_length=100, null=True)
    depreciation_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)  # In percentage
    useful_life_years = models.IntegerField(null=True)
    current_value = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    # Location & Assignment
    location = models.CharField(max_length=255, null=True)
    department = models.CharField(max_length=255, null=True)
    assigned_to = models.CharField(max_length=255, blank=True, null=True)

    # Image and Document Upload (Renamed using asset_id)
    asset_image = models.ImageField(upload_to=asset_image_upload_path, null=True, blank=True)
    documents = models.FileField(upload_to=asset_document_upload_path, blank=True, null=True)

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

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if it's a new asset
        super().save(*args, **kwargs)  # Save first to get asset_id

        # Handle Image Renaming
        if is_new and self.asset_image:
            ext = self.asset_image.name.split('.')[-1]
            new_filename = f"{self.asset_id}.{ext}"
            new_path = os.path.join("asset_images", new_filename)

            old_path = self.asset_image.path
            if default_storage.exists(old_path):
                with default_storage.open(old_path, 'rb') as file_content:
                    default_storage.save(new_path, ContentFile(file_content.read()))
                default_storage.delete(old_path)  # Delete temp file

            self.asset_image.name = new_path
            super().save(update_fields=["asset_image"])  # Save again with updated path

        # Handle Document Renaming
        if is_new and self.documents:
            ext = self.documents.name.split('.')[-1]
            new_filename = f"{self.asset_id}.{ext}"
            new_path = os.path.join("asset_documents", new_filename)

            old_path = self.documents.path
            if default_storage.exists(old_path):
                with default_storage.open(old_path, 'rb') as file_content:
                    default_storage.save(new_path, ContentFile(file_content.read()))
                default_storage.delete(old_path)  # Delete temp file

            self.documents.name = new_path
            super().save(update_fields=["documents"])  # Save again with updated path

    def __str__(self):
        return f"{self.asset_id}"
    

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
