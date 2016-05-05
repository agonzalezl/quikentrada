from django.contrib import admin
from django.shortcuts import render

@admin.site.register_view('statistics')
def statistics(request):
    return render(request, 'statistics.html')
