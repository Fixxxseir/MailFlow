from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import MessageForm
from .models import Message
from .services import MessagesService


@method_decorator(vary_on_cookie, name="dispatch")
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "MessageManagement/messages_list.html"
    context_object_name = "messages"
    paginate_by = 8

    def get_queryset(self):
        return MessagesService.get_messages_from_cache(self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "MessageManagement/messages_form.html"
    success_url = reverse_lazy("MessageManagement:messages_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Добавление сообщения"
        context["submit_button_text"] = "Добавить"
        return context


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "MessageManagement/messages_detail.html"
    context_object_name = "message"

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        message = get_object_or_404(queryset, pk=self.kwargs.get("pk"))
        owner = self.request.user

        if message.owner == owner or owner.has_perm("MessageManagement.can_view_all_messages"):
            return message
        raise PermissionDenied("У вас нет прав на просмотр")


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "MessageManagement/messages_form.html"

    def get_success_url(self):
        return reverse_lazy("MessageManagement:message_detail", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        message = super().get_object(queryset)
        owner = self.request.user

        if message.owner == owner:
            return message
        raise PermissionDenied("У вас нет прав на изменение или удаление 'сообщения'!")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Редактирование сообщения"
        context["submit_button_text"] = "Сохранить"
        return context


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "MessageManagement/messages_confirm_delete.html"
    success_url = reverse_lazy("MessageManagement:messages_list")

    def get_object(self, queryset=None):
        message = super().get_object(queryset)
        owner = self.request.user

        if message.owner == owner:
            return message
        raise PermissionDenied("У вас нет прав на удаление 'сообщения'!")
