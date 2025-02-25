from django.urls import path
from .views import *

urlpatterns = [
    path("auth/login/", LoginAPIView.as_view(), name="login"),
    path("auth/logout/", LogoutAPIView.as_view(), name="logout"),

    path("users/register/", RegisterAPIView.as_view(), name="user-register"),
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("users/<int:user_id>/", UserDetailAPIView.as_view(), name="user-detail"),

    

    path("assets/", AssetListCreateAPIView.as_view(), name="asset-list-create"),
    path("assets/<int:asset_id>/", AssetDetailAPIView.as_view(), name="asset-detail"),
    
    path("transactions/", TransactionListCreateAPIView.as_view(), name="transaction-list-create"),
    path("transactions/<int:transaction_id>/", TransactionDetailAPIView.as_view(), name="transaction-detail"),

    # KYC URLs
    path('kyc/', KYCListCreateAPIView.as_view(), name='kyc-list-create'),
    path('kyc/<int:kyc_id>/', KYCDetailAPIView.as_view(), name='kyc-detail'),

    # KYC Status URLs
    path('kyc-status/', KYCStatusListCreateAPIView.as_view(), name='kyc-status-list-create'),
    path('kyc-status/<int:kyc_status_id>/', KYCStatusDetailAPIView.as_view(), name='kyc-status-detail'),

    # Bank Details URLs
    path('bank-details/', BankDetailListCreateAPIView.as_view(), name='bank-details-list-create'),
    path('bank-details/<int:bank_detail_id>/', BankDetailDetailAPIView.as_view(), name='bank-detail'),

    # User Types URLs
    path('user-types/', UserTypeListCreateAPIView.as_view(), name='user-types-list-create'),
    path('user-types/<int:type_id>/', UserTypeDetailAPIView.as_view(), name='user-type-detail'),

    # Status URLs
    path('status/', StatusListCreateAPIView.as_view(), name='status-list-create'),
    path('status/<int:status_id>/', StatusDetailAPIView.as_view(), name='status-detail'),

    
]
