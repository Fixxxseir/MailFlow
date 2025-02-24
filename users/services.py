from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from mailings.models import Mailing
from users.models import User


def block_user(request, pk):
    if not request.user.groups.filter(name="managers").exists():
        raise PermissionDenied
    user = get_object_or_404(User, pk=pk)
    user.is_active = False
    user.save()
    return redirect(reverse_lazy("users:user_manager_list"))


def unblock_user(request, pk):
    if not request.user.groups.filter(name="managers").exists():
        raise PermissionDenied
    user = get_object_or_404(User, pk=pk)
    user.is_active = True
    user.save()
    return redirect(reverse_lazy("users:user_manager_list"))


@login_required
@permission_required("mailings.can_disabling_mailings", raise_exception=True)
def disable_mailing(request, mailing_id):
    mailing = get_object_or_404(Mailing, id=mailing_id)
    mailing.status = "completed"
    mailing.save()
    return redirect("mailings:mailing_list")
