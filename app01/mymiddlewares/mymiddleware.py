# -*- coding: utf-8 -*-
"""
Authentication middleware for CRM system.
Restricts access to authenticated users except for whitelisted URLs.
"""
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse


class Auth(MiddlewareMixin):
    """
    Middleware to enforce authentication on protected routes.
    
    Whitelisted URLs (login and register) are accessible without authentication.
    All other routes require a valid session with username.
    """
    
    # URLs that don't require authentication
    white_list = [
        reverse("app01:login"),
        reverse("app01:register")
    ]

    def process_request(self, request):
        """
        Check if request requires authentication.
        
        Args:
            request: Django HTTP request object
            
        Returns:
            Redirect to login if not authenticated, None otherwise
        """
        if request.path not in self.white_list:
            if not request.session.get("username"):
                return redirect("app01:login")
        return None
