from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import generic

from wiki.models import Page


class EditView(generic.DetailView):
    model = Page
    template_name = 'wiki/edit.html'
    context_object_name = 'page'

    def get(self, request, *args, **kwargs):
        return render(request, 'wiki/edit.html', {'page': get_page_or_create(self.kwargs['title'])})

    def post(self, request, **kwargs):
        title = kwargs['title']

        if 'save' in request.POST:
            page = Page.objects.get_or_create(page_title=title, pub_date=timezone.now())[0]
            page.page_contents = request.POST['content']
            page.save()

        return redirect('wiki:detail', title)


def index(request):
    return render(request, 'wiki/index.html', {'pages': Page.objects.all()})


def view(request, title):
    return render(request, 'wiki/detail.html', {'page': get_page(title)})


def get_page(title):
    """
    Attempts to retrieve a page from its id.

    :param title: id of the page.
    :return: page matching provided id or None.
    """

    page = None

    try:
        page = Page.objects.get(page_title=title)
    except Page.DoesNotExist:
        pass

    return page


def get_page_or_create(title):
    """
    Attempts to retrieve a page from the provided id, otherwise returns
    a new page with using the provided id as its title.

    :param title: id of the page.
    :return: page matching provided id or temporary blank page.
    """
    page = get_page(title)

    if page is None:
        page = Page(page_title=title)

    return page
