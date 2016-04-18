from django.shortcuts import render, render_to_response, redirect
from django.http import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from eventos.models import *

# Create your views here.
def index(request):
    eventos = Evento.objects.all()
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
    eventList =  Evento.objects.filter(nombre__icontains=searched)
    return render(request, 'search.html', {'eventos':eventList, 'searched': searched})

def event(request):
    id_event = request.GET.get('id')
    evento = Evento.objects.get(pk=id_event) 
    return render(request, 'event.html', {'evento': evento})
