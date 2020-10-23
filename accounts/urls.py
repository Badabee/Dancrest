from django.urls import path
from . import views
from drf_yasg2.utils import swagger_auto_schema
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordChangeView,
)

RESPONSES = {
	200: 'HTTP request successful',
	400: 'Malformed request syntax',
	500: 'An internal server error occured' 
}

PasswordResetView = swagger_auto_schema(
								method='post',
								operation_description="Accepts the POST parameter: email\
								\nReturns the success/fail message.",
								operation_summary="Password Reset View",
								tags = ["Authentication"],
								responses=RESPONSES
								)(PasswordResetView.as_view())

PasswordResetConfirmview = swagger_auto_schema(
								method='post',
								operation_description="Accepts the following POST parameters: old_password, new_password1, new_password2\
								\nReturns the success/fail message.",
								operation_summary="Password Reset Confirm View",
								tags = ["Authentication"],
								responses=RESPONSES
								)(PasswordResetConfirmView.as_view())

PasswordChangeView = swagger_auto_schema(
								method='post',
								operation_description="Accepts the following POST parameters: new_password1, new_password2,\
								uid, token\nReturns the success/fail message.",
								operation_summary="Password Change View",
								tags = ["Authentication"],
								responses=RESPONSES
								)(PasswordChangeView.as_view())

LoginView = swagger_auto_schema(
								method='post',
								operation_description="Sign in users",
								operation_summary="Login View",
								tags = ["Authentication"],
								responses=RESPONSES
								)(LoginView.as_view())

Logoutview = swagger_auto_schema(
								method='post',
								operation_description="Sign out users",
								operation_summary="Logout View",
								tags = ["Authentication"],
								responses=RESPONSES[200]
								)(LogoutView.as_view())

urlpatterns = [
	path('activate/<str:uidb64>/<str:token>', views.AccountActivationView.as_view(), name='activate'),
	path('register', views.RegistrationView.as_view(), name='register'),
	path('login', LoginView, name='login'),
	path('logout', LogoutView, name='logout'),
	path('password/reset', password_reset_view, name='password-reset'),
	path('password/reset/confirm', password_reset_confirm_view, name='password-reset-confirm'),
	path('password/change', password_change_view, name='password-change'),
]