from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import *
from django.urls import reverse_lazy
from .mixins import *
from itertools import chain

# Create your views here.

def home(request):
    events = []
    events = chain(events, Event.objects.order_by('when').all())
    # events = Event.objects.all().sort_by('when')
    return render(request, 'home.html', {'events': events, 'teams': Team.objects.all()})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
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

class TeamList(LoginRequiredMixin, ListView, TeamMixin):
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

class TeamDetail(LoginRequiredMixin, DetailView, TeamMixin):
    model = Team
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super(TeamDetail, self).get_context_data(**kwargs)
        context['events'] = Event.objects.filter(motherteam_id=self.kwargs['pk']).order_by('-when')
        return context

class TeamCreate(LoginRequiredMixin, CreateView, TeamMixin):
    model = Team
    fields = ['title', 'description']
    success_url = reverse_lazy('teams')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TeamCreate, self).form_valid(form)

class TeamDelete(LoginRequiredMixin, DeleteView, TeamMixin):
    model = Team
    context_object_name = 'team'
    success_url = reverse_lazy('teams')

class TeamUpdate(LoginRequiredMixin, UpdateView, TeamMixin):
    model = Team
    fields = ['title', 'description']
    success_url = reverse_lazy('teams')

class EventDetail(LoginRequiredMixin, DetailView, EventMixin):
    model = Event
    context_object_name = 'event'

class EventCreate(LoginRequiredMixin, CreateView, EventMixin):
    model = Event
    fields = ['motherteam', 'title', 'description', 'place', 'when']
    success_url = reverse_lazy('teams')

    def get_form(self, *args, **kwargs):
        form_class = super().get_form(form_class=None)

        form_class.fields['motherteam'].choices =\
            [(motherteam.pk, motherteam) for motherteam in Team.objects.filter(user=self.request.user)]
        
        return form_class

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EventCreate, self).form_valid(form)

class EventDelete(LoginRequiredMixin, DeleteView, EventMixin):
    model = Event
    context_object_name = 'event'
    success_url = reverse_lazy('teams')
