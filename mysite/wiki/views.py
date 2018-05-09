from django.shortcuts import render, redirect
from django.views import generic

from wiki.models import Page


class EditView(generic.DetailView):
    model = Page
    template_name = 'wiki/edit.html'
    context_object_name = 'page'

    def get(self, request, *args, **kwargs):
        return render(request, 'wiki/edit.html', {'page': get_page(self.kwargs['title'])})

    def post(self, request, **kwargs):
        title = kwargs['title']

        if 'save' in request.POST:
            page = Page.objects.get_or_create(page_title=title)[0]
            page.page_contents = request.POST['content']
            page.save()

        return redirect('wiki:detail', title)


def index(request):
    return render(request, 'wiki/index.html', {'pages': Page.objects.all()})


def view(request, title):
    return render(request, 'wiki/detail.html', {'page': get_page(title)})


def get_page(input):
    ret_page = None

    # Attempt to find the page from the provided string "title",
    # either matching its id or title.
    for page in Page.objects.all():
        if page.page_title == input or page.id == safe_parse(input):
            ret_page = page

    return ret_page


def safe_parse(str_num):
    """
    Attempts to parse a string into an integer, otherwise returns 0.

    :param str_num: string to parse.
    :return:        parsed int, or 0 if it couldn't be parsed.
    """

    try:
        return int(str_num)
    except (ValueError, TypeError):
        return 0
