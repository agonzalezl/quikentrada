"""quikentrada URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from eventos import views
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),

	# "index" URL
    url(r'^$', views.index, name='index'),

    # "login" URL
    url(r'^login/', views.login_user, name='login'),

    # "advanced search" URL
    url(r'^advanced_search/', views.advanced_search, name="advanced_search"),

    # "event" URL
    url(r'^event', views.event, name="event"),

    # "buy_ticket" URL
    url(r'^buy_ticket', views.buy_ticket, name="buy_ticket"),

    # "purchase" URL
    url(r'^purchase', views.purchase, name="purchase"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

