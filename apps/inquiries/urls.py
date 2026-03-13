from django.urls import path

from .views import InquiriesViewSets


urlpatterns = [
    path(
        "api/inquiries/", InquiriesViewSets.as_view({"get": "list", "post": "create"})
    ),
    path(
        "api/inquiries/<int:pk>/",
        InquiriesViewSets.as_view({"patch": "partial_update"}),
    ),
]
