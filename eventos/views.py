from django.shortcuts import render, render_to_response, redirect
from django.http import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from eventos.models import *
from django.db.models import Q # for advanced search
from django import forms

# Create your views here.
def index(request):
    eventos = Eventos.objects.all()
    return render(request, 'index.html', {'eventos': eventos})

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/admin/')
    return render_to_response('login.html', context_instance=RequestContext(request))

def search(request):
    searched = request.GET['search']
    eventList =  Eventos.objects.filter(nombre__icontains=searched)
    return render(request, 'search.html', {'eventos':eventList, 'searched': searched})

def event(request):
    id_event = request.GET.get('id')
    evento = Eventos.objects.get(pk=id_event) 
    return render(request, 'event.html', {'evento': evento})

# It works except with date
def advanced_search(request):
    queryset = Q()

    name = request.GET.get('name')
    date = request.GET.get('date')
    location = request.GET.get('location')
    # tipo = request.GET.get('tipo')

    if name:
        queryset.add(Q(nombre__icontains=name), Q.OR)

    if date:
         queryset.add(Q(fecha=date), Q.OR)

    if location:
         queryset.add(Q(lugar__icontains=location), Q.OR)

    # if tipo is not None:
    #      queryset.add(Q(tipo=tipo), Q.AND)

    eventList = Eventos.objects.filter(queryset)
    return render(request, 'advanced_search.html', {'eventos':eventList})

