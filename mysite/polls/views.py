from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1 style='color: red'>Hello World</h1>")


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    return HttpResponse("You're looking at the results of question %s." % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)