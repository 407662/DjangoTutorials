from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from wiki.forms import UserLoginForm
from wiki.models import Page


class EditView(generic.DetailView):
    model = Page
    template_name = 'wiki/edit.html'
    context_object_name = 'page'

    @method_decorator(login_required(login_url='/wiki/login'))
    def get(self, request, *args, **kwargs):
        """
        Using the login_required method decorator, the requester's user
        authentication is checked before the method is called. If not
        authenticated they will be redirected to the login page.

        Retrieves the requested page using the provided title. If the page
        does not exist, a page with no content and the title provided will
        be rendered, but not stored.

        :param request: page requester.
        :return: rendered GET HttpResponse of edit.html.
        """

        return render(request, 'wiki/edit.html', {'page': get_page_or_temp(self.kwargs['title'])})

    def post(self, request, **kwargs):
        """
        Retrieves or creates a Page object using the provided title
        and sets page_contents with the provided content. The page is
        saved whether or not the page existed or if the content had
        been changed.

        Redirects to the provided wiki's detail page.

        :param request: page requester.
        :return: rendered POST HttpResponse of edit.html.
        """

        title = kwargs['title']

        if 'save' in request.POST:
            page = Page.objects.get_or_create(page_title=title, defaults={'pub_date': timezone.now()})[0]
            page.page_contents = request.POST['content']
            page.save()

        return redirect('wiki:detail', title)


def index(request):
    """
    Renders index.html, providing a QuerySet of all Page objects alphabetically
    ordered by their page_title.

    :param request: page requester.
    :return: rendered HttpResponse of register.html.
    """

    return render(request, 'wiki/index.html', {'pages': Page.objects.order_by('page_title')})


def view(request, title):
    """
    Retrieves the requested page using the provided title. If the page does
    not exist, a page with no content and the title provided will be
    rendered, but not stored.

    :param request: page requester.
    :param title:   title of the wiki, not the title from the html head tags.
    :return: rendered HttpResponse of detail.html.
    """

    return render(request, 'wiki/detail.html', {'page': get_page_or_temp(title)})


def login_view(request):
    """
    On POST attempts to authenticate the user with the provided credentials,
    if successful the requester will be redirected to the provided next
    page. Otherwise the requester will be informed about why they could
    not be logged in. Invalid credentials, user, etc ("authentication error").

    On GET a blank UserLoginForm is created along with the next parameter
    being stored, which will later be used in the POST request. "/wiki" is
    used by default if the next parameter is provided.

    :param request: page requester.
    :return: rendered HttpResponse of login.html.
    """

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            login(request, user)
            return redirect(form.next)
        else:
            form.error = 'Failed to log you in: authentication error.'
    else:
        form = UserLoginForm
        form.next = request.GET.get('next', '/wiki')

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    """
    Logs out authenticated users and passes if the logout was
    successful when calling render.

    :param request: page requester.
    :return: rendered HttpResponse of logout.html.
    """

    success = request.user.is_authenticated

    if success:
        logout(request)

    return render(request, 'registration/logout.html', {'success': success})


def register(request):
    """
    On GET returns an empty UserCreationForm. On POST, attempts to create
    a user with create_user. Existing user, weak passwords and parsing is
    handled when calling the create_user method.

    Upon successful registration, the requester is redirected to the
    login page.

    :param request: page requester.
    :return: rendered HttpResponse of register.html.
    """

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
