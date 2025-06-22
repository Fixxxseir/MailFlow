from django.urls import path

from MessageManagement.apps import MessagesConfig

from .views import MessageCreateView, MessageDeleteView, MessageDetailView, MessageListView, MessageUpdateView

app_name = MessagesConfig.name

urlpatterns = [
    path("", MessageListView.as_view(), name="messages_list"),
    path("add_message/", MessageCreateView.as_view(), name="add_message"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"),
    path("delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"),
]
