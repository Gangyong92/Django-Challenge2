from django.urls import path
from books.views import BooksView, BookDetail, CreateBook, UpdateBook

app_name = "books"

urlpatterns = [
    path("", BooksView.as_view(), name="books"),
    path("<int:pk>/", BookDetail.as_view(), name="book"),
    path("<int:pk>/update/", UpdateBook.as_view(), name="update"),
    path("create/", CreateBook.as_view(), name="create"),
]