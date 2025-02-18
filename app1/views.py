from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404

# Register API - Create User
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    





# Get All Users
class UserListAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Retrieve, Update, and Delete a Single User
class UserDetailAPIView(APIView):
    def get_object(self, user_id):
        return get_object_or_404(User, user_id=user_id)

    def get(self, request, user_id):
        user = self.get_object(user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        user = self.get_object(user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = self.get_object(user_id)
        user.delete()
        return Response({"message": "User deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


# Login API
class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                return Response({"message": "Login successful!", "user_type": user.user_type}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# Logout API (Dummy for now, can be extended for token-based logout)
class LogoutAPIView(APIView):
    def post(self, request):
        return Response({"message": "Logged out successfully!"}, status=status.HTTP_200_OK)






# Create & List Assets
class AssetListCreateAPIView(APIView):
    def get(self, request):
        assets = Asset.objects.all()
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, Update & Delete an Asset
class AssetDetailAPIView(APIView):
    def get_object(self, asset_id):
        try:
            return Asset.objects.get(asset_id=asset_id)
        except Asset.DoesNotExist:
            return None

    def get(self, request, asset_id):
        asset = self.get_object(asset_id)
        if asset:
            serializer = AssetSerializer(asset)
            return Response(serializer.data)
        return Response({"error": "Asset not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, asset_id):
        asset = self.get_object(asset_id)
        if asset:
            serializer = AssetSerializer(asset, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Asset not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, asset_id):
        asset = self.get_object(asset_id)
        if asset:
            asset.delete()
            return Response({"message": "Asset deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Asset not found"}, status=status.HTTP_404_NOT_FOUND)


# Create & List Transactions
class TransactionListCreateAPIView(APIView):
    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, Update & Delete a Transaction
class TransactionDetailAPIView(APIView):
    def get_object(self, transaction_id):
        try:
            return Transaction.objects.get(transaction_id=transaction_id)
        except Transaction.DoesNotExist:
            return None

    def get(self, request, transaction_id):
        transaction = self.get_object(transaction_id)
        if transaction:
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)
        return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, transaction_id):
        transaction = self.get_object(transaction_id)
        if transaction:
            serializer = TransactionSerializer(transaction, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, transaction_id):
        transaction = self.get_object(transaction_id)
        if transaction:
            transaction.delete()
            return Response({"message": "Transaction deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)