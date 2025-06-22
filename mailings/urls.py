from django.urls import path

from mailings.apps import MailingsConfig
from mailings.services import disable_mailing, start_mailing
from mailings.views import (HomeView, MailingCreateView, MailingDeleteView, MailingDetailView, MailingListView,
                            MailingUpdateView, MailingAttemptListView)

app_name = MailingsConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("mailings/", MailingListView.as_view(), name="mailings_list"),
    path("mailings/add_mailing/", MailingCreateView.as_view(), name="add_mailing"),
    path("mailings/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailings/update/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailings/delete/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("mailings/disable_malling/<int:pk>/", disable_mailing, name="disable_mailing"),
    path("mailings/start_mailing/<int:pk>/", start_mailing, name="start_mailing"),
    path("mailings/attempt/", MailingAttemptListView.as_view(), name="mailings_attempt")

]
