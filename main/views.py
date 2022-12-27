from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import *
from django.urls import reverse_lazy


# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    else:
        form = SignUpForm()

    return render(request, 'authentication/signup.html', {'form': form})

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is None:
            return redirect('falselogin')
        elif user is not None:
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'authentication/login.html')

def falselogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is None:
            return redirect('falselogin')
        elif user is not None:
            login(request, user)
            return redirect('home')

    else:
        return render(request, 'authentication/falselogin.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def user(request):
    return render(request, 'user.html')

class TeamList(LoginRequiredMixin, ListView):
    model = Team
    context_object_name = 'teams'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = context['teams'].filter(user=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['teams'] = context['teams'].filter(title__icontains=search_input) # můžeme použít title__startswith místo title__contains

        context['search_input'] = search_input
        return context

class TeamDetail(LoginRequiredMixin, DetailView):
    model = Team
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super(TeamDetail, self).get_context_data(**kwargs)
        context['events'] = Event.objects.filter(motherteam_id=self.kwargs['pk'])
        return context

class TeamCreate(LoginRequiredMixin, CreateView):
    model = Team
    fields = ['title', 'description']
    success_url = reverse_lazy('teams')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TeamCreate, self).form_valid(form)

class TeamDelete(LoginRequiredMixin, DeleteView):
    model = Team
    context_object_name = 'team'
    success_url = reverse_lazy('teams')

class TeamUpdate(LoginRequiredMixin, UpdateView):
    model = Team
    fields = ['title', 'description']
    success_url = reverse_lazy('teams')

class EventDetail(LoginRequiredMixin, DetailView):
    model = Event
    context_object_name = 'event'

class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'description', 'place', 'when', 'motherteam']
    success_url = reverse_lazy('teams')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EventCreate, self).form_valid(form)