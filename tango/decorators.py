from django.conf import settings
from django.shortcuts import redirect


def unauthenticated_required(home_url=settings.LOGIN_REDIRECT_URL):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if request.request.user.is_authenticated:
                return redirect(home_url)
            return view_func(request, *args, **kwargs)

        return wrap

    return decorator
