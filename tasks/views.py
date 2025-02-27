from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html',{
            'form':UserCreationForm()
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #registra un user
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('tasks')
            except:
                return render(request,'signup.html',{
                    'form':UserCreationForm(),
                    'error':'Username already exists'
                })
        return render(request,'signup.html',{
            'form':UserCreationForm(),
            'error':'Passwords do not match'
        })

@login_required    
def tasks(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request,'tasks.html',{'tasks':tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request,'tasks_completed.html',{'tasks':tasks})

@login_required
def task_detail(request,task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task ,pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request,'task_detail.html',{
            'task':task,
            'form':form
            })
    else:
        try:
            task = get_object_or_404(Task ,pk=task_id, user=request.user)
            form = TaskForm(request.POST,instance=task)
            if form.is_valid():
                form.save()
                return redirect('tasks')
        except ValueError:
            return render(request,'task_detail.html',{
            'task':task,
            'form':form,
            'error':'Error updating task'
            })

@login_required
def complete_task(request,task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task ,pk=task_id, user=request.user)
        task.date_completed = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request,task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task ,pk=task_id, user=request.user)
        task.delete()
        return redirect('tasks')
    
    
@login_required
def create_task(request):
    try:
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                new_task =form.save(commit=False)
                new_task.user = request.user
                new_task.save()
                return redirect('tasks')
    except:
         return render(request,'create_task.html',{
            'form': TaskForm(),
            'error':'Error creating task'
            })
    else:
        # Create a new task
        return render(request,'create_task.html',{
            'form': TaskForm()
            })


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request,'signin.html',{
            'form':AuthenticationForm()
        })
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            login(request,user)
            return redirect('tasks')
        return render(request,'signin.html',{
            'form':AuthenticationForm(),
            'error':'Invalid username or password'
            })
    