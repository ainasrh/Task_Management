from functools import wraps
from typing import Callable

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from rest_framework.permissions import BasePermission


# =========================
# DRF Permission Classes
# =========================

class IsSuperAdmin(BasePermission):
    """Allow access only to authenticated users with role == 'superadmin'."""

    def has_permission(self, request, view) -> bool:
        user = getattr(request, "user", None)
        return bool(user and user.is_authenticated and getattr(user, "role", "") == "superadmin")


class IsAdmin(BasePermission):
    """Allow access only to authenticated users with role == 'admin'."""

    def has_permission(self, request, view) -> bool:
        user = getattr(request, "user", None)
        return bool(user and user.is_authenticated and getattr(user, "role", "") == "admin")


class IsAdminOrSuperAdmin(BasePermission):
    """Allow access to authenticated users with role in {'admin', 'superadmin'}."""

    def has_permission(self, request, view) -> bool:
        user = getattr(request, "user", None)
        return bool(user and user.is_authenticated and getattr(user, "role", "") in {"admin", "superadmin"})


class IsRegularUser(BasePermission):
    """Allow access only to authenticated users with role == 'user'."""

    def has_permission(self, request, view) -> bool:
        user = getattr(request, "user", None)
        return bool(user and user.is_authenticated and getattr(user, "role", "") == "user")


class IsSelfOrAdminOrSuperAdmin(BasePermission):
    """Object-level access if the user is the owner or has admin/superadmin role.

    Expects the view to set get_object() that returns an instance with an
    attribute/field that can be compared to request.user (commonly `user` or `assigned_to`).
    Override `get_owner(obj)` on the view for custom ownership resolution if needed.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        user = getattr(request, "user", None)
        if not (user and user.is_authenticated):
            return False

        role = getattr(user, "role", "")
        if role in {"admin", "superadmin"}:
            return True

        # Try common ownership attributes
        owner = getattr(obj, "user", None) or getattr(obj, "assigned_to", None) or getattr(obj, "owner", None)
        return owner == user


# =========================
# Django View Decorators (for HTML views)
# =========================

def _redirect_no_access() -> HttpResponse:
    # Centralized no-access redirect target; update the URL name if needed
    return redirect("no_access")


def superadmin_required(view_func: Callable) -> Callable:
    @wraps(view_func)
    def _wrapped(request: HttpRequest, *args, **kwargs):
        user = getattr(request, "user", None)
        if user and user.is_authenticated and getattr(user, "role", "") == "superadmin":
            return view_func(request, *args, **kwargs)
        return _redirect_no_access()

    return _wrapped


def admin_required(view_func: Callable) -> Callable:
    @wraps(view_func)
    def _wrapped(request: HttpRequest, *args, **kwargs):
        user = getattr(request, "user", None)
        if user and user.is_authenticated and getattr(user, "role", "") == "admin":
            return view_func(request, *args, **kwargs)
        return _redirect_no_access()

    return _wrapped


def admin_or_superadmin_required(view_func: Callable) -> Callable:
    @wraps(view_func)
    def _wrapped(request: HttpRequest, *args, **kwargs):
        user = getattr(request, "user", None)
        if user and user.is_authenticated and getattr(user, "role", "") in {"admin", "superadmin"}:
            return view_func(request, *args, **kwargs)
        return _redirect_no_access()

    return _wrapped

