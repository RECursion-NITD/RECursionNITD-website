from django.shortcuts import redirect

def user_is_admin(url):
    def method_wrapper(function):
        def wrap(request, *args, **kwargs):
            if request.user.profile.role == '1' or request.user.profile.role == '2':
                return function(request, *args, **kwargs)
            else:
                return redirect(url)
        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrap
    return method_wrapper