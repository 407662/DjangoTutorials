from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from wiki.models import Page


class EditView(generic.DetailView):
    model = Page
    template_name = 'wiki/edit.html'
    context_object_name = 'page'

    def get(self, request, *args, **kwargs):
        return render(request, 'wiki/edit.html', {'page': get_page_or_temp(self.kwargs['title'])})

    def post(self, request, **kwargs):
        title = kwargs['title']

        if 'save' in request.POST:
            page = Page.objects.get_or_create(page_title=title, defaults={'pub_date': timezone.now()})[0]
            page.page_contents = request.POST['content']
            page.save()

        return redirect('wiki:detail', title)


def index(request):
    return render(request, 'wiki/index.html', {'pages': Page.objects.order_by('page_title')})


def view(request, title):
    return render(request, 'wiki/detail.html', {'page': get_page(title)})


def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            login(request, user)
        # else: failed page
    else:
        return render(request, 'registration/login.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password1'])
            user.save()
            return redirect('wiki:login')
    else:
        form = UserCreationForm
    return render(request, 'registration/register.html', {'form': form})


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


def get_page_or_temp(title):
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
