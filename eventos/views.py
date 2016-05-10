from django.shortcuts import render, render_to_response, redirect
from django.http import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from eventos.models import *
from django.db.models import Q, Count # for advanced
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import time #for sleep

# "index" function
def index(request):
    tipo_eventos = TipoEventos.objects.all()
    return render(request, 'index.html', {'tipo_eventos':tipo_eventos})

# "login" function
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

# "event" function
def event(request):
    id_event = request.GET.get('id_event')
    evento = Eventos.objects.get(pk=id_event)
    sesiones = Sesiones.objects.filter(id_evento=id_event) #event sessions
    
    #available of each session
    for sesion in sesiones:
        sesion.disponible = sesion.capacidad - sesion.entradas_vendidas
    
    request.session["id_evento"] = evento.id_evento

    #increasing number of event views
    evento.consultas += 1
    evento.save() 
    
    return render(request, 'event.html', {
        'evento': evento, 
        'sesiones':sesiones, 
        })

# "advanced_search" function
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

# "buy_ticket" function
def buy_ticket(request):
    id_session = request.GET.get('id_session')
    request.session["id_sesion"] = id_session
    return render(request, 'buy_ticket.html')

# "purchase" function
def purchase(request):
    #customer input values
    number = request.GET.get('number')
    expire_date = request.GET.get('expire_date')
    cvc = request.GET.get('cvc')

    #event
    id_evento = request.session.get("id_evento")
    evento = Eventos.objects.get(pk=id_evento)

    try:
        cuenta = GestionPago.objects.get(numero_tarjeta=number, fecha_caducidad=expire_date, cvc=cvc)
    except GestionPago.DoesNotExist:
        cuenta = None

    cantidad_entradas = int(request.GET.get('amount'))
    importe = float(evento.precio) * float(cantidad_entradas)
    
    if cuenta is not None:
        if cuenta.saldo >= importe:
            
            id_sesion = request.session.get("id_sesion")
            sesion = Sesiones.objects.get(pk=id_sesion)

            entrada = Entradas(
                nombre=request.GET.get('name'), 
                apellido=request.GET.get('surname'), 
                dni=request.GET.get('dni'), 
                telefono=request.GET.get('telephone'), 
                edad=request.GET.get('age'), 
                email=request.GET.get('email'),
                cantidad_entradas=request.GET.get('amount'),
                id_sesion=sesion
                )
            
            entrada.save()

            # Balance substraction
            cuenta.saldo = float(cuenta.saldo) - importe 
            cuenta.save()

            # Event capacity substraction
            sesion.entradas_vendidas = sesion.entradas_vendidas + cantidad_entradas
            sesion.save()
            time.sleep(4)
            return render(request, 'purchase.html', {'entrada':entrada, 'importe':importe})
        else:
            mensaje = "No autorizacion de pago!"
            return render(request, 'purchase.html', {'mensaje':mensaje})
    else:
        mensaje = "Error de pago!"
        return render(request, 'purchase.html', {'mensaje':mensaje})


@csrf_exempt
def age_stats(request):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')

        data = []


        for i in range(5):
            gt = i*20
            lt = gt+19
            others =  Entradas.objects.filter( edad__range=(gt, lt) ).count()
            c = Entradas.objects.filter( edad__range=(gt, lt) , id_sesion__id_evento__tipo_evento__nombre_tipoevento__icontains="Cultural").count()
            d = Entradas.objects.filter( edad__range=(gt, lt) , id_sesion__id_evento__tipo_evento__nombre_tipoevento__icontains="Deportivo").count()

            others = others - d - c

            data.append({"Cultural": c, "Deportivo": d, "Otros": others})

        # just return a JsonResponse
        return JsonResponse(data, safe=False)
