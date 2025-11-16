"""
DRF views for accounts app.
Following Single Responsibility Principle - views handle HTTP request/response only.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import (
    UserRegistrationSerializer,
    LoginSerializer,
    UserSerializer,
    TokenRefreshSerializer,
)
from accounts.services.authentication_service import AuthenticationService
from accounts.services.user_service import UserService
from core.exceptions import AuthenticationError, ValidationError


class RegisterView(APIView):
    """
    User registration endpoint.
    Following Dependency Inversion Principle - depends on service abstraction.
    """
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    
    def __init__(self, **kwargs):
        """Initialize view with service dependencies."""
        super().__init__(**kwargs)
        self.user_service = UserService()
        self.auth_service = AuthenticationService()
    
    def post(self, request):
        """
        Register a new user.
        
        POST /api/accounts/register/
        """
        serializer = UserRegistrationSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = self.user_service.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                first_name=serializer.validated_data.get('first_name', ''),
                last_name=serializer.validated_data.get('last_name', ''),
            )
            
            tokens = self.auth_service.generate_tokens(user)
            
            return Response(
                {
                    'message': 'User registered successfully',
                    'user': UserSerializer(user).data,
                    'tokens': tokens,
                },
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response(
                {'error': str(e.message)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'Registration failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginView(APIView):
    """
    User login endpoint.
    Following Dependency Inversion Principle - depends on service abstraction.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    def __init__(self, **kwargs):
        """Initialize view with service dependencies."""
        super().__init__(**kwargs)
        self.auth_service = AuthenticationService()
    
    def post(self, request):
        """
        Authenticate user and return tokens.
        
        POST /api/accounts/login/
        """
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            result = self.auth_service.login(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
            )
            
            return Response(result, status=status.HTTP_200_OK)
        except AuthenticationError as e:
            return Response(
                {'error': str(e.message)},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {'error': 'Login failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TokenRefreshView(APIView):
    """
    Token refresh endpoint.
    Following Dependency Inversion Principle - depends on service abstraction.
    """
    permission_classes = [AllowAny]
    serializer_class = TokenRefreshSerializer
    
    def __init__(self, **kwargs):
        """Initialize view with service dependencies."""
        super().__init__(**kwargs)
        self.auth_service = AuthenticationService()
    
    def post(self, request):
        """
        Refresh access token.
        
        POST /api/accounts/token/refresh/
        """
        serializer = TokenRefreshSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            result = self.auth_service.refresh_token(
                refresh_token=serializer.validated_data['refresh']
            )
            
            return Response(result, status=status.HTTP_200_OK)
        except AuthenticationError as e:
            return Response(
                {'error': str(e.message)},
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    """
    User logout endpoint.
    Accepts refresh token only - no valid access token required.
    """
    permission_classes = [AllowAny]
    serializer_class = TokenRefreshSerializer
    
    def post(self, request):
        """
        Logout user (blacklist refresh token).
        Works even when access token is expired/invalid.
        
        POST /api/accounts/logout/
        Body: { "refresh": "refresh_token_string" }
        """
        serializer = TokenRefreshSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            refresh_token = serializer.validated_data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(
                {'message': 'Logged out successfully'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': 'Logout failed'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(APIView):
    """
    Get current user profile.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get(self, request):
        """
        Get current user profile.
        
        GET /api/accounts/profile/
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
