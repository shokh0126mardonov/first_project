from django.urls import path

from .views import ProductViewSets

urlpatterns = [
    path("api/products/", ProductViewSets.as_view({"get": "list", "post": "create"})),
    path(
        "api/products/<int:pk>/",
        ProductViewSets.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
]
