from django.views.generic import ListView, DetailView, CreateView, UpdateView
from people.models import Person
from movies.models import Movie
from books.models import Book
from users import mixins as user_mixins


class PeopleView(ListView):

    model = Person
    paginate_by = 15
    paginate_orphans = 5
    ordering = "-created_at"
    context_object_name = "people"
    template_name = "people/people_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "All People"

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


class PersonDetail(DetailView):
    model = Person
    template_name = "people/person_detail.html"
    context_object_name = "person"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kind = context["object"].kind
        if kind == Person.KIND_ACTOR:
            contents = Movie.objects.filter(cast=context["object"])
            content_kind = "movie"
        elif kind == Person.KIND_DIRECTOR:
            contents = Movie.objects.filter(director=context["object"])
            content_kind = "movie"
        elif kind == Person.KIND_WRITER:
            contents = Book.objects.filter(writer=context["object"])
            content_kind = "book"

        context["contents"] = contents
        context["content_kind"] = content_kind
        return context


class CreatePerson(user_mixins.LoggedInOnlyView, CreateView):
    model = Person
    fields = (
        "name",
        "photo",
        "kind",
    )


class UpdatePerson(user_mixins.LoggedInOnlyView, UpdateView):
    model = Person
    fields = ("name", "photo", "kind")