from django.contrib import admin
from django.shortcuts import render
from eventos.models import *
from django.db.models import Count

@admin.site.register_view('edades')
def edades(request):
    return render(request, 'age_stats.html')


@admin.site.register_view('consultas')
def consultas(request):
	eventos = Eventos.objects.all().order_by('-consultas')[:20]
	return render(request, 'consults_stats.html', {'eventos':eventos})


@admin.site.register_view('top_ventas')
def top_ventas(request):
	entradas =  Entradas.objects.all().values('id_sesion__id_evento__nombre').annotate(total=Count('id_sesion__id_evento')).order_by('-total')[:20]
	print entradas

	return render(request, 'top_sells.html', {'sells':entradas})

@admin.site.register_view('event_customers')
def event_customers(request):
	eventos = Eventos.objects.all().order_by('id_evento')

	if request.GET.get('id_evento') is not None:
		id_evento = request.GET.get('id_evento')
		entradas =  Entradas.objects.filter(id_sesion__id_evento=id_evento).distinct('dni')
	else:
		entradas = Entradas.objects.filter(id_sesion__id_evento = 1).distinct('dni')

	return render(request, 'event_customers.html', {
		'eventos': eventos,
		'clientes':entradas
		})


cantidad = ventas_hora(13)
print cantidad

def ventas_hora(hour):
	cont = 0 #count amount of hours
	ventas = Entradas.objects.all()
	for venta in ventas:
		if venta.fecha_compra.hour == hour:
			cont += 1
	return cont


