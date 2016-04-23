from django.shortcuts import render, render_to_response, redirect
from django.http import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from eventos.models import *
from django.db.models import Q # for advanced search

# Create your views here.
def index(request):
    tipo_eventos = TipoEventos.objects.all()
    return render(request, 'index.html', {'tipo_eventos':tipo_eventos})

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

def event(request):
    id_event = request.GET.get('id_event')
    evento = Eventos.objects.get(pk=id_event)
    sesiones = Sesiones.objects.filter(id_evento=id_event) #event sessions
    
    #available of each session
    for sesion in sesiones:
        sesion.disponible = sesion.capacidad - sesion.entradas_vendidas
    
    request.session["id_evento"] = evento.id_evento
    
    return render(request, 'event.html', {
        'evento': evento, 
        'sesiones':sesiones, 
        })

def advanced_search(request):
    tipo_eventos = TipoEventos.objects.all()
    queryset = Q()

    name = request.GET.get('name')
    date_start = request.GET.get('date_start')
    location = request.GET.get('location')
    type_event = request.GET.get('type')

    if name:
        queryset.add(Q(nombre__icontains=name), Q.AND)

    if type_event:
         queryset.add(Q(tipo_evento=type_event), Q.AND)

    if date_start:
        queryset.add(Q(sesiones__sesion__date=date_start), Q.AND)

    if location:
        queryset.add(Q(sesiones__ciudad__icontains=location), Q.AND)

    eventList = Eventos.objects.filter(queryset)

    return render(request, 'advanced_search.html', 
        {'eventos':eventList, 
        'tipo_eventos':tipo_eventos, 
        'search':  { 'name': name, 'date_start':date_start, 'location':location } })

def buy_ticket(request):
    id_session = request.GET.get('id_session')
    request.session["id_sesion"] = id_session
    return render(request, 'buy_ticket.html')

def purchase(request):
    # id_sesion = request.sesion.get["id_sesion"]
    sesion = Sesiones.objects.get(pk=1)

    entrada = Entradas(
        nombre=request.GET.get('name'), 
        apellido=request.GET.get('surname'), 
        dni=request.GET.get('dni'), 
        telefono=request.GET.get('telephone'), 
        edad=request.GET.get('age'), 
        email=request.GET.get('email'), 
        id_sesion=sesion
        )
    
    entrada.save()

    return render(request, 'purchase.html', {'entrada':entrada})


