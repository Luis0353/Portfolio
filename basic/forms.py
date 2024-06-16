from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','sources']
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Write your Project Title'}),
            'description' : forms.Textarea(attrs={'class': 'form-control', 'placeholder' : 'Write your Project Description'}),
            'sources' : forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Write your Project Source'}),
        }