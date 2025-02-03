from django.urls import path
from .views import (
    UserProfileView,
    LogoutView,
    CreateAccountView,
    UpdateProfileView,
    ForgotPasswordView,
    ResetPasswordView,
    VerifyEmailView,
    LoginView
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("create-account/", CreateAccountView.as_view(), name="create-account"),
    path("update-profile/", UpdateProfileView.as_view(), name="update-profile"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/<str:uidb64>/<str:token>/", ResetPasswordView.as_view(), name="reset-password"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
]
