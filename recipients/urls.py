from django.urls import path

from recipients.apps import RecipientsConfig

from .views import (RecipientCreateView, RecipientDeleteView, RecipientDetailView, RecipientListView,
                    RecipientUpdateView)

app_name = RecipientsConfig.name

urlpatterns = [
    path("recipients/", RecipientListView.as_view(), name="recipients_list"),
    path("add_recipient/", RecipientCreateView.as_view(), name="add_recipient"),
    path("recipient/<int:pk>/", RecipientDetailView.as_view(), name="recipient_detail"),
    path("update/<int:pk>/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("delete/<int:pk>/", RecipientDeleteView.as_view(), name="recipient_delete"),
]
