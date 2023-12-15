"""
URL configuration for LITRevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from LITReview import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index.as_view(), name='index'),
    path('register/', views.Register.as_view(), name='register'),
    path('flux/', views.Flux.as_view(), name='flux'),
    path('logout/', views.Disconnect.as_view(), name='logout'),
    path('demande_critique/', views.DemandeCritique.as_view(), name='demande_critique'),
    path('proposer_critique/', views.ProposerCritique.as_view(), name='proposer_critique'),
    path('posts/', views.Post.as_view(), name='posts'),
    path('abonnements/', views.Abonnements.as_view(), name='abonnements'),
]
