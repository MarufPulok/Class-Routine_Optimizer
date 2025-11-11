"""
User service.
Following Single Responsibility Principle - handles user management business logic only.
"""
from typing import Optional, Dict, Any
from django.contrib.auth.models import User
from django.db import IntegrityError

from core.services.base import BaseService
from core.exceptions import ValidationError, DatabaseError
from accounts.models import Profile


class UserService(BaseService):
    """
    Service for handling user management operations.
    Following Dependency Inversion Principle - depends on abstractions.
    """
    
    def create_user(self, username: str, email: str, password: str, **extra_fields) -> User:
        """
        Create a new user.
        
        Args:
            username: Username
            email: Email address
            password: Password
            **extra_fields: Additional user fields
            
        Returns:
            Created User instance
            
        Raises:
            ValidationError: If validation fails
            DatabaseError: If creation fails
        """
        if not username:
            raise ValidationError("Username is required")
        
        if not email:
            raise ValidationError("Email is required")
        
        if not password:
            raise ValidationError("Password is required")
        
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                **extra_fields
            )
            # Create profile for the user
            Profile.objects.create(user=user)
            
            self.log_info(f"User {username} created successfully")
            return user
        except IntegrityError as e:
            if 'username' in str(e).lower():
                raise ValidationError("Username already exists")
            elif 'email' in str(e).lower():
                raise ValidationError("Email already exists")
            raise DatabaseError(f"Error creating user: {str(e)}")
        except Exception as e:
            self.log_error("Error creating user", error=e)
            raise DatabaseError(f"Error creating user: {str(e)}")
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User instance or None
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            username: Username
            
        Returns:
            User instance or None
        """
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
    
    def update_user(self, user: User, **kwargs) -> User:
        """
        Update user information.
        
        Args:
            user: User instance to update
            **kwargs: Fields to update
            
        Returns:
            Updated User instance
            
        Raises:
            ValidationError: If validation fails
            DatabaseError: If update fails
        """
        try:
            for key, value in kwargs.items():
                if key == 'password':
                    user.set_password(value)
                else:
                    setattr(user, key, value)
            user.save()
            
            self.log_info(f"User {user.username} updated successfully")
            return user
        except Exception as e:
            self.log_error("Error updating user", error=e)
            raise DatabaseError(f"Error updating user: {str(e)}")

