from django.urls import path
from accounts.views.register import Register
from accounts.views.login import Login, Logout

app_name = 'accounts'

urlpatterns = [
    path('accounts/register/', Register.as_view(), name='register'),
    path('accounts/login/', Login.as_view(), name='login'),
    path('accounts/logout', Logout.as_view(), name='logout')
]
