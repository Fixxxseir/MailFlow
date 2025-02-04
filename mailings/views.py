from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from recipients.models import Recipient

from .forms import MailingForm
from .models import Mailing, MailingAttempt
from .services import MailingsService


class HomeView(TemplateView):
    template_name = "mailings/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_mailings"] = Mailing.objects.count()
        context["active_mailings"] = Mailing.objects.filter(mailing_status="launched").count()
        context["unique_recipients"] = Recipient.objects.distinct().count()
        return context


@method_decorator(vary_on_cookie, name="dispatch")
class MailingListView(ListView):
    model = Mailing
    template_name = "mailings/mailings_list.html"
    context_object_name = "mailings"
    paginate_by = 8

    def get_queryset(self):
        return MailingsService.get_mailings_from_cache(self.request.user)


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailings_form.html"
    success_url = reverse_lazy("mailings:mailings_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Добавление отправления"
        context["submit_button_text"] = "Добавить"
        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailings/mailings_detail.html"
    context_object_name = "mailing"

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        mailing = get_object_or_404(queryset, pk=self.kwargs.get("pk"))
        owner = self.request.user

        if mailing.owner == owner or owner.has_perm("mailings.can_view_all_mailings"):
            return mailing
        raise PermissionDenied("У вас нет прав на просмотр")


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailings_form.html"
    success_url = reverse_lazy("mailings:mailings_list")

    def get_success_url(self):
        return reverse_lazy("mailings:mailing_detail", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        mailing = super().get_object(queryset)
        owner = self.request.user

        if mailing.owner == owner:
            return mailing
        raise PermissionDenied("У вас нет прав на изменение или удаление 'отправления'!")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Редактирование получателя"
        context["submit_button_text"] = "Сохранить"
        return context


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailings/mailings_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailings_list")

    def get_object(self, queryset=None):
        mailing = super().get_object(queryset)
        owner = self.request.user

        if mailing.owner == owner:
            return mailing
        raise PermissionDenied("У вас нет прав на удаление 'отправления'!")


class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = "mailings/mailing_attempts.html"
    context_object_name = "attempts"
    paginate_by = 8

    def get_object(self, queryset=None):
        attempt = super().get_object(queryset)
        owner = self.request.user

        if attempt.owner == owner:
            return attempt
        raise PermissionDenied("У вас нет прав на изменение или удаление 'отправления'!")
