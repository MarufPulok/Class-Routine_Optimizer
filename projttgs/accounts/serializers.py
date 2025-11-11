"""
DRF serializers for accounts app.
Following DTO Pattern - separate domain models from API representation.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Profile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserRegistrationSerializer(serializers.Serializer):
    """
    Serializer for user registration.
    Following Interface Segregation Principle - specific serializer for registration.
    """
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    password_confirm = serializers.CharField(write_only=True, min_length=8, required=True)
    first_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    
    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs
    
    def validate_username(self, value):
        """Validate username uniqueness."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
    def validate_email(self, value):
        """Validate email uniqueness."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Following Interface Segregation Principle - specific serializer for login.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class TokenRefreshSerializer(serializers.Serializer):
    """Serializer for token refresh."""
    refresh = serializers.CharField(required=True)


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'date_of_birth', 'photo', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

