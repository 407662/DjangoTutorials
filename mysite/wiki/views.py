from django.shortcuts import render
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'wiki/index.html'
    context_object_name = 'page'


def index(request):
    return render(request, 'wiki/index.html')
