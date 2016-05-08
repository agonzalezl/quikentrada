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