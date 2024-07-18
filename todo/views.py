from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task

# Create your views here.
def index(request):
    context = {}
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        due_at_str = request.POST.get('due_at', '').strip()

        if not title or not due_at_str:
            context['error'] = 'タイトルと期限を入力してください'
        else:
            due_at = parse_datetime(due_at_str)
            if due_at is not None:
                due_at = make_aware(due_at)
            else:
                context['error'] = '不正なフォーマットです'

            if 'error' not in context:
                task = Task(title=title, due_at=due_at)
                task.save()
                return redirect('index')

    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')

    context['tasks'] = tasks
    return render(request, 'todo/index.html', context)

def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    context = {
        'task': task,
    }
    return render(request, 'todo/detail.html', context)

def update(request, task_id):
    context = {}
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        due_at_str = request.POST.get('due_at', '').strip()

        if not title or not due_at_str:
            context['error'] = 'タイトルと期限を入力してください'
        else:
            due_at = parse_datetime(due_at_str)
            if due_at is not None:
                due_at = make_aware(due_at)
            else:
                context['error'] = '不正なフォーマットです'

            if 'error' not in context:
                task.title = title
                task.due_at = due_at
                task.save()
                return redirect('detail', task_id)

    context['task'] = task
    return render(request, "todo/edit.html", context)

def close(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.completed = True
    task.save()
    return redirect('index')

def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.delete()
    return redirect('index')
