from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError 
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required


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

@login_required
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

@login_required
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

@login_required  
def project_details(request, project_id):
    if request.method == 'GET':
        project = get_object_or_404(Project, pk=project_id)
        form = ProjectForm(instance=project)
        return render(request, 'project_details.html', {
            'project' : project,
            'form' : form
        })
    else:
        try:
            project = get_object_or_404(Project, pk=project_id)
            form = ProjectForm(request.POST,instance=project)
            form.save()
            return redirect('home') 
        except ValueError:
            return render(request, 'project_details.html', {
            'project' : project,
            'form' : form,
            'error' : 'Error al Actualizar los Datos'
        })


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('home')