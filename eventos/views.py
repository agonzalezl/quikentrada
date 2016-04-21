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

def search(request):
    searched = request.GET['search']
    eventList =  Eventos.objects.filter(nombre__icontains=searched)
    return render(request, 'search.html', {'eventos':eventList, 'searched': searched})

def event(request):
    id_event = request.GET.get('id')
    evento = Eventos.objects.get(pk=id_event)
    sesiones = Sesiones.objects.filter(id_evento=id_event) #event sessions
    disponibilidad = evento.capacidad - evento.entradas_vendidas
    request.session["id_evento"] = evento.id_evento
    return render(request, 'event.html', {'evento': evento, 'sesiones':sesiones, 'disponibilidad':disponibilidad})

def advanced_search(request):
    tipo_eventos = TipoEventos.objects.all()
    queryset = Q()

    name = request.GET.get('name')
    date_start = request.GET.get('date_start')
    date_end = request.GET.get('date_end')
    location = request.GET.get('location')
    type_event = request.GET.get('type')

    if name:
        queryset.add(Q(nombre__icontains=name), Q.OR)

    if date_start and date_end:
        queryset.add(Q(fecha__range=(date_start, date_end)), Q.OR)

    if location:
        queryset.add(Q(lugar__icontains=location), Q.OR)

    if type_event:
         queryset.add(Q(tipo_evento=type_event), Q.OR)

    eventList = Eventos.objects.filter(queryset)
    return render(request, 'advanced_search.html', {'eventos':eventList, 'tipo_eventos':tipo_eventos, 'search':  { 'name': name, 'date_start':date_start, 'location':location } })

def buy_ticket(request):
    id_event = request.GET.get('id')
    evento = Eventos.objects.get(pk=id_event)   
    sesiones = Sesiones.objects.filter(id_evento=id_event)
    evento_id = request.session.get("id_evento")
    return render(request, 'buy_ticket.html', {'evento':evento, 'evento_id':evento_id, 'sesiones':sesiones})

def personal_information(request):
    request.session["session"] = request.GET.get('session')
    return render(request, 'personal_information.html')

def account_data(request):
    request.session["name"] = request.GET.get('name')
    request.session["last_name"] = request.GET.get('last_name')
    request.session["dni"] = request.GET.get('dni')
    request.session["phone"] = request.GET.get('phone')
    request.session["age"] = request.GET.get('age')
    request.session["email"] = request.GET.get('email')
    return render(request, 'account_data.html')

def purchase(request):
    # Customer Information
    name = request.session.get("name")
    last_name = request.session.get("last_name")
    dni = request.session.get("dni")
    phone = request.session.get("phone")
    age = request.session.get("age")
    email = request.session.get("email")

    # Event Information
    id_sesion = request.session.get("session")
    sesion = Sesiones.objects.get(pk=id_sesion)
    id_evento = request.session.get("id_evento")
    evento = Eventos.objects.get(pk=id_evento)
    return render(request, 'purchase.html', {
        'name':name, 
        'last_name':last_name, 
        'dni':dni,
        'phone':phone,
        'age':age,
        'email':email,
        'sesion': sesion,
        'evento': evento,
        })


