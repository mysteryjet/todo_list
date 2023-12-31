from typing import Any, Dict
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

# vista para login
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        #cuando esto sea válido, se hará login al usuario
        if user is not None: # esto indica si el usuario fue creado correctamente
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get (self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


# muestra la vista de las task que se tienen
class TaskList(LoginRequiredMixin, ListView):# regresa un template con un queryset de datos
    model = Task
    context_object_name = 'tasks'

    # nos aseguramos que el usuario solo pueda ver sus propias tareas
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        
        # para buscar texto dentro de las tasks
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

# esta vista es para Crear una tarea
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = {'title', 'complete', 'description'}
    success_url = reverse_lazy('tasks') #esto sirve para redireccionar al usuario

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
# esta vista es para Actualizar una task
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = {'complete', 'description', 'title'}
    success_url = reverse_lazy('tasks')


# esta vista es para Eliminar una task
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')