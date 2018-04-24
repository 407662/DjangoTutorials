from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Question


def index(request):
    return render(request, 'polls/index.html', {'latest_question_list': Question.objects.order_by('-pub_date')[:5]})


def detail(request, question_id):
    return render(request, 'polls/detail.html', {'question': get_object_or_404(Question, pk=question_id)})


def results(request, question_id):
    return HttpResponse("You're looking at the results of question %s." % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
