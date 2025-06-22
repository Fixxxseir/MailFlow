from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import RecipientForm
from .models import Recipient
from .services import RecipientsService


@method_decorator(vary_on_cookie, name="dispatch")
class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "recipients/recipients_list.html"
    context_object_name = "recipients"
    paginate_by = 8

    def get_queryset(self):
        return RecipientsService.get_recipients_from_cache(self.request.user)


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipients/recipients_form.html"
    success_url = reverse_lazy("recipients:recipients_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Добавление получателя"
        context["submit_button_text"] = "Добавить"
        return context


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = "recipients/recipients_detail.html"
    context_object_name = "recipient"

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        recipient = get_object_or_404(queryset, pk=self.kwargs.get("pk"))
        owner = self.request.user

        if recipient.owner == owner or owner.has_perm("recipients.can_view_all_recipients"):
            return recipient
        raise PermissionDenied("У вас нет прав на просмотр")


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipients/recipients_form.html"

    def get_success_url(self):
        return reverse_lazy("recipients:recipient_detail", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        recipient = super().get_object(queryset)
        owner = self.request.user
        if recipient.owner == owner:
            return recipient
        raise PermissionDenied("У вас нет прав на изменение или удаление 'получателя'!")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Редактирование получателя"
        context["submit_button_text"] = "Сохранить"
        return context


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = "recipients/recipients_confirm_delete.html"
    success_url = reverse_lazy("recipients:recipients_list")

    def get_object(self, queryset=None):
        recipient = super().get_object(queryset)
        owner = self.request.user

        if recipient.owner == owner:
            return recipient
        raise PermissionDenied("У вас нет прав на удаление 'получателя'!")
