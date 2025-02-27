from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate

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
    
def tasks(request):
    return render(request,'tasks.html')

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
    