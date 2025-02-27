from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserType)
admin.site.register(Status)
admin.site.register(KYCStatus)
admin.site.register(KYC)
admin.site.register(BankDetails)
admin.site.register(AssetType)








class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id','username','full_name','email','user_type')
    readonly_fields = ("user_id",)  # Prevents modification in the admin panel

    
admin.site.register(User, UserAdmin)


class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_id','asset_name','asset_type','location')
    
admin.site.register(Asset, AssetAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id','asset','buyer_id','buyer_type')
    
admin.site.register(Transaction, TransactionAdmin)