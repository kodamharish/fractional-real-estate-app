from django.contrib import admin
from .models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','full_name','email','user_type')
    
admin.site.register(User, UserAdmin)


class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_id','asset_name','asset_type','location')
    
admin.site.register(Asset, AssetAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id','asset','buyer_id','buyer_type')
    
admin.site.register(Transaction, TransactionAdmin)