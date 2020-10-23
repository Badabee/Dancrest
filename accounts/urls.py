from django.urls import path
from . import views
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordChangeView,
)

urlpatterns = [
	path('register', views.RegistrationView.as_view(), name='register'),
	path('login', LoginView.as_view(), name='login'),
	path('logout', LogoutView.as_view(), name='logout'),
	path('password/reset', PasswordResetView.as_view(), name='password-reset'),
	path('password/reset/confirm', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
	path('password/change', PasswordChangeView.as_view(), name='password-change'),
]