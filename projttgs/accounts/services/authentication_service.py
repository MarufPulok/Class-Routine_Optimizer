"""
Authentication service.
Following Single Responsibility Principle - handles authentication business logic only.
"""
from typing import Optional, Dict, Any
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from core.services.base import BaseService
from core.exceptions import AuthenticationError, ValidationError


class AuthenticationService(BaseService):
    """
    Service for handling authentication operations.
    Following Dependency Inversion Principle - depends on abstractions.
    """
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user with username and password.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            User instance if authenticated, None otherwise
        """
        user = authenticate(username=username, password=password)
        if user is None:
            self.log_warning(f"Failed authentication attempt for username: {username}")
        return user
    
    def generate_tokens(self, user: User) -> Dict[str, Any]:
        """
        Generate JWT tokens for a user.
        
        Args:
            user: User instance
            
        Returns:
            Dictionary with access and refresh tokens, including expiration timestamps
        """
        try:
            refresh = RefreshToken.for_user(user)
            return {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'access_expires_at': refresh.access_token.payload['exp'],
                'refresh_expires_at': refresh.payload['exp'],
            }
        except Exception as e:
            self.log_error("Error generating tokens", error=e)
            raise AuthenticationError("Failed to generate authentication tokens")
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Perform login operation.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Dictionary with user data and tokens
            
        Raises:
            AuthenticationError: If authentication fails
        """
        user = self.authenticate_user(username, password)
        
        if user is None:
            raise AuthenticationError("Invalid username or password")
        
        if not user.is_active:
            raise AuthenticationError("User account is disabled")
        
        tokens = self.generate_tokens(user)
        
        self.log_info(f"User {username} logged in successfully")
        
        return {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'tokens': tokens,
        }
    
    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh access token using refresh token.
        When ROTATE_REFRESH_TOKENS is enabled, also returns a new refresh token.
        
        Args:
            refresh_token: Refresh token string
            
        Returns:
            Dictionary with new access token, and new refresh token if rotation is enabled,
            including expiration timestamps
            
        Raises:
            AuthenticationError: If token refresh fails
        """
        try:
            from django.conf import settings
            refresh = RefreshToken(refresh_token)
            
            # Get new access token (this may rotate the refresh token if enabled)
            new_access_token = refresh.access_token
            
            result = {
                'access': str(new_access_token),
                'access_expires_at': new_access_token.payload['exp'],
            }
            
            # If rotation is enabled, return new refresh token
            if getattr(settings, 'SIMPLE_JWT', {}).get('ROTATE_REFRESH_TOKENS', False):
                # After accessing access_token, if rotation is enabled, refresh token is rotated
                # The refresh object now represents the new refresh token
                result['refresh'] = str(refresh)
                result['refresh_expires_at'] = refresh.payload['exp']
            
            return result
        except Exception as e:
            self.log_error("Error refreshing token", error=e)
            raise AuthenticationError("Invalid or expired refresh token")

