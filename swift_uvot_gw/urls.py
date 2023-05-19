"""django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', include('tom_common.urls')),
    path('nonlocalizedevents/', include('tom_nonlocalizedevents.urls', namespace='nonlocalizedevents')),
    path('todolist/', TemplateView.as_view(template_name='todolist.html'),name='todolist'),
    path('draftdetectiongcn/', TemplateView.as_view(template_name='draftgcn.html'),name='draftdetectiongcn'),
    path('draftsummarygcn/', TemplateView.as_view(template_name='draftsummarygcn.html'),name='draftsummarygcn'),

]
