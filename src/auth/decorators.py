from functools import wraps
from fastapi import Depends
from .utils import get_current_active_user, check_user_role
from src.models import User, UserRole


def role_required(allowed_roles):
    """
    Decorator that checks if the current user has the required role(s) to access a route.

    Args:
        allowed_roles (list): A list of roles that are allowed to access the route.

    Returns:
        function: The decorated function.

    Example:
        @role_required(['admin', 'manager'])
        async def protected_route():
            # Code for the protected route
            pass
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_active_user), **kwargs):
            check_user_role(current_user, allowed_roles)
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator


admin_required = role_required([UserRole.ADMIN])
moderator_required = role_required([UserRole.ADMIN, UserRole.MODERATOR])
