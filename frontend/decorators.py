from django.contrib.auth.decorators import user_passes_test
from functools import wraps

def admin_required(function=None):
    @wraps(function)  # Maintain the original function's metadata
    def wrapper(*args, **kwargs):
        return user_passes_test(
            lambda u: u.groups.filter(name='Admin').exists(),
            login_url='/login'
        )(*args, **kwargs)
    return wrapper if function is None else wrapper(function)

def staff_required(function=None):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return user_passes_test(
            lambda u: u.groups.filter(name='Staff').exists(),
            login_url='/login'
        )(*args, **kwargs)
    return wrapper if function is None else wrapper(function)

def accountant_required(function=None):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return user_passes_test(
            lambda u: u.groups.filter(name='Accountant').exists(),
            login_url='/login'
        )(*args, **kwargs)
    return wrapper if function is None else wrapper(function)
