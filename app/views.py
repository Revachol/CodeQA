# app/views.py
from django.shortcuts import render, get_object_or_404
from .models import Question, Tag, Answer
from django.core.paginator import Paginator
from django.http import Http404

def index(request):
    questions = Question.objects.newest()
    page = paginate(request, questions)
    tags = Tag.objects.all()[:20]
    return render(request, 'index.html', {
        'questions': page.object_list,
        'page_obj': page,
        'tags': tags
    })

def hot(request):
    questions = Question.objects.best()
    page = paginate(request, questions)
    tags = Tag.objects.all()[:20]
    return render(request, 'hot.html', {
        'questions': page.object_list,
        'page_obj': page,
        'tags': tags
    })

def question(request, question_id):
    q = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=q).order_by('-created_at')
    page = paginate(request, answers)
    tags = Tag.objects.all()[:20]
    return render(request, 'single_question.html', {
        'question': q,
        'answers': page.object_list,
        'page_obj': page,
        'tags': tags
    })

def paginate(request, queryset, per_page=5):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(queryset, per_page)
    try:
        page = paginator.page(page_num)
    except:
        raise Http404("Page not found")
    return page

def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    questions = Question.objects.by_tag(tag.name)
    page = paginate(request, questions)
    tags = Tag.objects.all()[:20]
    return render(request, 'tag.html', {
        'questions': page.object_list,
        'tag': tag.name,
        'page_obj': page,
        'tags': tags
    })

def login(request):
    return render(request, 'login.html', context={'tags': Tag.objects.all()[:20]})

def register(request):
    return render(request, "register.html", context={'tags': Tag.objects.all()[:20]})

def settings(request):
    return render(request, "settings.html", context={'tags': Tag.objects.all()[:20]})

def ask(request):
    return render(request, "ask.html", context={'tags': Tag.objects.all()[:20]})
