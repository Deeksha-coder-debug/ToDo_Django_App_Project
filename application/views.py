from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Q
from .forms import TaskForm
from .models import Task
from django.utils import timezone


@login_required
def index(request):
    # Data isolation: ONLY the current user's tasks
    pending_tasks = Task.objects.filter(
        user=request.user, 
        complete=False
    ).order_by('due_date', '-priority')
    
    completed_tasks = Task.objects.filter(
        user=request.user, 
        complete=True
    ).order_by('-completed_at')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # CRITICAL: Assign ownership
            task.save()
            messages.success(request, "Task added successfully!")
            return redirect('application:index')
    else:
        form = TaskForm()

    # Dashboard counts
    total_pending = pending_tasks.count()
    total_completed = completed_tasks.count()
    overdue_count = pending_tasks.filter(due_date__lt=timezone.now().date()).count()

    return render(request, 'application/index.html', {
        'form': form,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'total_pending': total_pending,
        'total_completed': total_completed,
        'overdue_count': overdue_count,
        'today': timezone.now().date(),  
    })


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task created!")
            return redirect('application:index')
    else:
        form = TaskForm()
    return render(request, 'application/add_task.html', {'form': form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # Object-Level Authorization: Prevent IDOR
    if task.user != request.user:
        raise PermissionDenied("You do not have permission to edit this task.")
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated!")
            return redirect('application:index')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'application/edit_task.html', {'form': form, 'task': task})


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if task.user != request.user:
        raise PermissionDenied("You do not have permission to modify this task.")
    
    task.complete = True
    task.save()
    messages.success(request, "Task marked as complete!")
    return redirect('application:index')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if task.user != request.user:
        raise PermissionDenied("You do not have permission to delete this task.")
    
    task.delete()
    messages.success(request, "Task deleted.")
    return redirect('application:index')


# from django.shortcuts import render,redirect
# from .forms import TaskForm
# from .models import Task
# # Create your views here.

# def index(request):
#     # tasks = Task.objects.all()  # Fetch all tasks from the database
#     # return render(request, 'application/index.html', {'tasks': tasks})
#     pending_tasks = Task.objects.filter(complete=False).order_by('due_date')
#     completed_tasks = Task.objects.filter(complete=True).order_by('-due_date')

#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         form = TaskForm()

#     return render(request, 'application/index.html', {
#         'form': form,
#         'pending_tasks': pending_tasks,
#         'completed_tasks': completed_tasks,
#     })

# def delete_task(request, task_id):
#     task = Task.objects.get(id=task_id)  # Get the task by its ID
#     task.delete()  # Delete the task from the database
#     return redirect('index')  # Redirect to the task list page

# def complete_task(request, task_id):
#     task = Task.objects.get(id=task_id)  # Get the task by its ID
#     task.complete = True  # Mark the task as complete
#     task.save()  # Save the task with the updated status
#     return redirect('index')  # Redirect to the task list page

# # Add task using TaskForm
# def add_task(request):
#     if request.method == 'POST':  # If the form is submitted via POST
#         form = TaskForm(request.POST)  # Create a form instance with the POST data
#         if form.is_valid():  # Check if the form is valid
#             form.save()  # Save the new task to the database
#             return redirect('index')  # Redirect to the task list page after saving the task
#     else:
#         form = TaskForm()  # Create an empty form instance if it's a GET request

#     return render(request, 'application/add_task.html', {'form': form})  # Render the form

# def edit_task(request, task_id):
#     task = Task.objects.get(id=task_id)
#     if request.method == 'POST':
#         form = TaskForm(request.POST, instance=task)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         form = TaskForm(instance=task)
#     return render(request, 'application/edit_task.html', {'form': form, 'task': task})
