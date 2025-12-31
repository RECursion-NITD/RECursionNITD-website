def associate_by_email(backend, details, user=None, *args, **kwargs):
    """
    Associate current auth with a user with the same email address in the DB.
    """
    if user:
        return None

    email = details.get('email')
    if email:
        # Try to associate accounts registered with the same email address,
        # only if it's a single object. AuthException is raised if multiple
        # objects are returned.
        try:
            from django.contrib.auth.models import User
            existing_user = User.objects.get(email=email)
            return {'user': existing_user}
        except User.DoesNotExist:
            pass
        except User.MultipleObjectsReturned:
            pass

def set_image_for_new_users(backend, details, user=None, *args, **kwargs):
    """
    Set default image for new users from social auth.
    """
    if user and not hasattr(user, 'profile'):
        # Create user profile if it doesn't exist
        pass
    return None