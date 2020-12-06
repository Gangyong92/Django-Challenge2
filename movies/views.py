from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.core.paginator import Paginator
from movies.models import Movie
from users import mixins as user_mixins
from reviews import forms as review_forms
from reviews import models as review_models


class MoviesView(ListView):

    model = Movie
    paginate_by = 15
    paginate_orphans = 5
    ordering = "-created_at"
    context_object_name = "movies"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "All Movies"

        paginator = context["paginator"]
        page_numbers_range = 10
        max_index = len(paginator.page_range)
        page = self.request.GET.get("page")
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context["page_range"] = page_range
        return context


class MovieDetail(DetailView):
    model = Movie
    context_object_name = "movie"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review_form = review_forms.CreateReviewForm()
        context["form"] = review_form

        # book의 pk 가져옴
        movie_pk = self.kwargs.get("pk")
        page = self.request.GET.get("page")

        # 한페이지당 표시 수랑 페이지 끊는 단위를 같이 쓰고 있음
        # 굳이 같이 쓸필요 없음 현재는 같이 씀 5, 5 단위로 끊음.
        page_numbers_range = 5
        # 가져온 book_pk에 해당하는 review만 가져옴
        review_list = review_models.Review.objects.filter(movie__pk=movie_pk)
        paginator = Paginator(review_list, page_numbers_range)
        max_index = len(paginator.page_range)
        reviews = paginator.get_page(page)

        # page 끊은 단위 계산
        current_page = int(page) if page else 1
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]

        context["page_range"] = page_range
        context["reviews"] = reviews  # paginator  직접 반환
        # print(vars(reviews.paginator)) 안에 뭐 들었는지 확인용.

        return context


class CreateMovie(user_mixins.LoggedInOnlyView, CreateView):
    model = Movie
    fields = (
        "title",
        "year",
        "cover_image",
        "category",
        "director",
        "cast",
    )


class UpdateMovie(user_mixins.LoggedInOnlyView, UpdateView):
    model = Movie
    fields = (
        "title",
        "year",
        "cover_image",
        "category",
        "director",
        "cast",
    )