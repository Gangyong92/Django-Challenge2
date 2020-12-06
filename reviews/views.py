from django.shortcuts import redirect, reverse
from reviews.forms import CreateReviewForm
from movies import models as movie_models
from books import models as book_models
from . import models


def add_review(request, pk):
    if request.method == "POST":
        content_type = request.GET.get("content_type")
        form = CreateReviewForm(request.POST)
        print(form)
        if content_type == "movie":
            movie = movie_models.Movie.objects.get(pk=pk)
            # 없으면 홈으로
            if not movie:
                return redirect(reverse("core:home"))
            if form.is_valid():
                review = form.save()
                review.movie = movie
                review.created_by = request.user
                review.save()
                return redirect(reverse("movies:movie", kwargs={"pk": movie.pk}))
        elif content_type == "book":
            book = book_models.Book.objects.get(pk=pk)
            # 없으면 홈으로
            if not book:
                return redirect(reverse("core:home"))
            if form.is_valid():
                review = form.save()
                review.book = book
                review.created_by = request.user
                review.save()
                return redirect(reverse("books:book", kwargs={"pk": book.pk}))


def delete_review(request, review_pk):
    content_type = request.GET.get("content_type")

    try:
        if content_type == "book":
            review = models.Review.objects.get(pk=review_pk)
            book = review.book
            review.delete()
            return redirect(reverse("books:book", kwargs={"pk": book.pk}))
        elif content_type == "movie":
            review = models.Review.objects.get(pk=review_pk)
            movie = review.movie
            review.delete()
            return redirect(reverse("movies:movie", kwargs={"pk": movie.pk}))
    except models.Review.DoesNotExist:
        return redirect(reverse("core:home"))