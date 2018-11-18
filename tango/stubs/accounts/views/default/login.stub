from django.views import View
from django.urls import reverse
from accounts.models import User
from djangounchained import settings
from django.http import HttpResponse
from accounts.forms import LoginForm
from django.shortcuts import render, redirect
from tango.decorators import unauthenticated_required
from django.contrib.auth import authenticate, login, logout


class Login(View):
    @unauthenticated_required()
    def get(self, request):
        form = LoginForm()

        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            try:
                user = User.objects.get(username=request.POST.get('username'))
                if not user.is_active:
                    form.add_error('username', 'The user is not active.')
                    form.non_field_errors = form.error_class()
            except User.DoesNotExist:
                pass

            return render(request, 'accounts/login.html', {'form': form})


class Logout(View):
    def post(self, request):
        logout(request)

        return redirect(reverse('accounts:login'))
