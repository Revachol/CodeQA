import copy

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator


QUESTIONS = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'This is text for question # {i}',
        'tags': ['django', 'python']
    } for i in range(30)
]

ANSWERS = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'This is text for question # {i}'
    } for i in range(10)
]

TAGS = ['django', 'python', 'bootstrap', 'css', 'html', 'с++']

# Create your views here.
def index(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_num)
    return render(request, 'index.html', context={'questions': page.object_list, 'page_obj': page, 'tags': TAGS})

def hot(request):
    q = list(reversed(copy.deepcopy(QUESTIONS)))
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(q, 5)
    page = paginator.page(page_num)
    return render(request, 'hot.html', context={'questions': page.object_list, 'page_obj': page, 'tags': TAGS})
    
def question(request, question_id):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(ANSWERS, 5)
    page = paginator.page(page_num)
    return render(request, 'single_question.html', context={'question': QUESTIONS[question_id], 'answers': page.object_list, 'page_obj': page, 'tags': TAGS})

def tag(request, tag_name):
    filtered_questions = [q for q in QUESTIONS if tag_name in q['tags']]
    return render(request, 'tag.html', context={'questions': filtered_questions, 'tag': tag_name, 'tags': TAGS})

def login(request):
    return render(request, 'login.html', context={'tags': TAGS})

def register(request):
    return render(request, "register.html", context={'tags': TAGS})

def settings(request):
    return render(request, "settings.html", context={'tags': TAGS})

def ask(request):
    return render(request, "ask.html", context={'tags': TAGS})