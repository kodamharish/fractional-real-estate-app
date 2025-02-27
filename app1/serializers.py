from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S",read_only=True)
    updated_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S",read_only=True)
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'user_id': {'read_only': True},  # Ensure it's not required in input
            'password': {'write_only': True}
        }
        

        
class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class KYCStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCStatus
        fields = '__all__'

class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = '__all__'

class BankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        fields = '__all__'
    

class AssetSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)
    class Meta:
        model = Asset
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    transaction_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)
    class Meta:
        model = Transaction
        fields = "__all__"
