from django.urls import path
from favs.views import resolve_add, FavsDetail

app_name = "favs"

urlpatterns = [
    path("", FavsDetail.as_view(), name="favs"),
    path("toggle/<int:pk>/", resolve_add, name="add"),
]