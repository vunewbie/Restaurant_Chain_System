from .models import User
from social_core.exceptions import AuthForbidden

def check_existing_user(backend, uid, user=None, *args, **kwargs):
    email = kwargs.get('response', {}).get('email')
    
    if email and User.objects.filter(email=email).exists():
        return {'user': User.objects.get(email=email)}
    
    return {}

def create_user_if_not_exists(backend, details, user=None, *args, **kwargs):
    if user:
        return {'user': user}

    email = details.get('email')
    full_name = details.get('fullname', details.get('name'))
    
    if not email:
        raise AuthForbidden(backend)
    
    user = User.objects.create_user(
        username=email.split('@')[0],
        email=email,
        full_name=full_name,
        password=None
    )
    user.set_unusable_password()
    user.save()
    
    return {'user': user}
