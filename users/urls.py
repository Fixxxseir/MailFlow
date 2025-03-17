from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetCompleteView, PasswordResetConfirmView,
                                       PasswordResetDoneView, PasswordResetView)
from django.urls import path, reverse_lazy

from users.apps import UsersConfig
from .forms import CustomLoginForm

from .services import block_user, unblock_user
from .views import UserEditProfile, UserManagerListView, UserRegisterView, email_verification

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html", form_class=CustomLoginForm), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email_confirm"),
    path("edit_profile/", UserEditProfile.as_view(), name="edit_profile"),
    path(
        "password_reset/",
        PasswordResetView.as_view(
            template_name="users/password_reset_form.html",
            email_template_name="users/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
        name="password_reset_complete",
    ),
    # FOR MODERATION
    path("user_list/", UserManagerListView.as_view(), name="user_manager_list"),
    path("block/<int:pk>/", block_user, name="block_user"),
    path("unblock/<int:pk>/", unblock_user, name="unblock_user"),
    # path("password_reset_confirm/<str:uid64>/<str:token>/", password_reset_confirm, name="password_reset_confirm"),
    # path("password_reset_complete/", password_reset_complete, name="password_reset_complete"),
    # path("password_reset_invalid/", password_reset_invalid, name="password_reset_invalid"),
    # path("users/", UserListView.as_view(), name="user_list"),
    # path("user/<int:pk>/", UserDetailsView.as_view(), name="user"),
    # path("update/user/<int:pk>/", UserUpdateView.as_view(), name="user_update"),
    # path("block_user/<int:pk>/", BlockUserView.as_view(), name="block_user"),
]
