from django.urls import path
from messaging.views import (
    CommunicationList,
    CommunicationDetail,
    MessageList,
    MessageDetail,
)

app_name = "messaging"

urlpatterns = [
    # Communication URLs
    path("communications/", CommunicationList.as_view(), name="communication-list"),
    path(
        "communications/<int:pk>/",
        CommunicationDetail.as_view(),
        name="communication-detail",
    ),
    # Message URLs
    path("messages/", MessageList.as_view(), name="message-list"),
    path("messages/<int:pk>/", MessageDetail.as_view(), name="message-detail"),
]
