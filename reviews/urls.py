from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("add/<int:pk>/", views.add_review, name="add"),
    path("delete/<int:review_pk>/", views.delete_review, name="delete"),
]