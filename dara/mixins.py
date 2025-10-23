"""
Authentication and Permission Mixins for API Views

This module provides reusable authentication and permission classes
that can be inherited by API views throughout the application.
"""

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
from user.models import User as CustomUser
from django.contrib.auth import get_user_model

User: CustomUser = get_user_model()


class AuthenticatedAPIView(APIView):
    """
    Base API View with Token Authentication enabled.
    
    All views inheriting from this class will require authentication
    using Django REST Framework's Token Authentication.
    
    Usage:
        class MyView(AuthenticatedAPIView):
            def get(self, request):
                # Your logic here
                pass
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class OptionalAuthAPIView(APIView):
    """
    API View with optional authentication.
    
    Authentication is attempted but not required. Use this when you want
    to provide different behavior for authenticated vs anonymous users.
    
    Usage:
        class MyView(OptionalAuthAPIView):
            def get(self, request):
                if request.user.is_authenticated:
                    # Authenticated user logic
                    pass
                else:
                    # Anonymous user logic
                    pass
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = []


# Role-based Permission Classes
class IsPharmacist(BasePermission):
    """
    Permission class that only allows pharmacists to access the view.
    """
    message = "Only pharmacists can perform this action."
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        try:
            custom_user = User.objects.get(name=request.user.username)
            return custom_user.role == 'pharmacist'
        except User.DoesNotExist:
            return False


class IsTechnician(BasePermission):
    """
    Permission class that only allows technicians to access the view.
    """
    message = "Only technicians can perform this action."
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Import here to avoid circular imports
        from user.models import User as User
        
        try:
            custom_user = User.objects.get(name=request.user.username)
            return custom_user.role == 'technician'
        except User.DoesNotExist:
            return False


class IsPharmacistOrTechnician(BasePermission):
    """
    Permission class that allows both pharmacists and technicians to access the view.
    """
    message = "You must be a pharmacist or technician to perform this action."
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        try:
            custom_user = User.objects.get(name=request.user.username)
            return custom_user.role in ['pharmacist', 'technician']
        except User.DoesNotExist:
            return False


# Role-based API Views
class PharmacistAPIView(AuthenticatedAPIView):
    """
    API View that requires the user to be a pharmacist.
    
    Usage:
        class MyView(PharmacistAPIView):
            def get(self, request):
                # Only pharmacists can access this
                pass
    """
    permission_classes = [IsAuthenticated, IsPharmacist]


class TechnicianAPIView(AuthenticatedAPIView):
    """
    API View that requires the user to be a technician.
    
    Usage:
        class MyView(TechnicianAPIView):
            def get(self, request):
                # Only technicians can access this
                pass
    """
    permission_classes = [IsAuthenticated, IsTechnician]


class PharmacistOrTechnicianAPIView(AuthenticatedAPIView):
    """
    API View that requires the user to be either a pharmacist or technician.
    
    Usage:
        class MyView(PharmacistOrTechnicianAPIView):
            def get(self, request):
                # Both pharmacists and technicians can access this
                pass
    """
    permission_classes = [IsAuthenticated, IsPharmacistOrTechnician]


# Helper Mixin for getting user role
class UserRoleMixin:
    """
    Mixin that provides helper methods to get user role information.
    
    Usage:
        class MyView(AuthenticatedAPIView, UserRoleMixin):
            def get(self, request):
                role = self.get_user_role(request)
                if role == 'pharmacist':
                    # Pharmacist logic
                    pass
    """
    
    def get_user_role(self, request):
        """Get the role of the authenticated user."""
        try:
            custom_user = User.objects.get(name=request.user.username)
            return custom_user.role
        except User.DoesNotExist:
            return None
    
    def get_custom_user(self, request):
        """Get the custom user object for the authenticated user."""
        try:
            return User.objects.get(name=request.user.username)
        except User.DoesNotExist:
            return None
    
    def is_pharmacist(self, request):
        """Check if the authenticated user is a pharmacist."""
        return self.get_user_role(request) == 'pharmacist'
    
    def is_technician(self, request):
        """Check if the authenticated user is a technician."""
        return self.get_user_role(request) == 'technician'

