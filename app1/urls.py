from django.urls import path
from .views import *

urlpatterns = [
    path("api/auth/login/", LoginAPIView.as_view(), name="login"),
    path("api/auth/logout/", LogoutAPIView.as_view(), name="logout"),

    path("api/users/register/", RegisterAPIView.as_view(), name="user-register"),
    path("api/users/", UserListAPIView.as_view(), name="user-list"),
    path("api/users/<int:user_id>/", UserDetailAPIView.as_view(), name="user-detail"),

    path("api/assets/", AssetListCreateAPIView.as_view(), name="asset-list-create"),
    path("api/assets/<int:asset_id>/", AssetDetailAPIView.as_view(), name="asset-detail"),
    
    path("api/transactions/", TransactionListCreateAPIView.as_view(), name="transaction-list-create"),
    path("api/transactions/<int:transaction_id>/", TransactionDetailAPIView.as_view(), name="transaction-detail"),

    
]
