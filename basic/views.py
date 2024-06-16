from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError 
from .models import Project
from .forms import ProjectForm


# Create your views here.

def home(request):
    projects = Project.objects.all()
    return render(request, 'home.html', {
        "projects" : projects
    })

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {
            'form' : UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('home')
            except IntegrityError:
               return render(request, 'register.html', {
                'form' : UserCreationForm,
                'error' : 'El usuario ya existe'
            }) 
        else:
            return render(request, 'register.html', {
            'form' : UserCreationForm,
            'error' : 'Las Contrasenas no coinciden'
        })

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'Usuario o Contrasena equivocados'
            })
        else:
            login(request, user)
            return redirect('home')

def about(request):
    return render(request, 'about.html')

def create(request):
    if request.method == 'GET':
        return render(request, 'create.html', {
            'form' : ProjectForm
        })
    else:
        form = ProjectForm(request.POST)
        new_project = form.save(commit=False)
        new_project.user = request.user
        new_project.save()
        return redirect('home')

def project_details(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'project_details.html', {
        'project' : project
    })

