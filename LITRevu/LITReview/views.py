from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserLoginForm, UserRegistrationForm, DemandeCritiqueForm
from django.views import View

# Create your views here.
class Disconnect(View):
    def get(self, request):
        logout(request)
        return redirect('index')

class Index(View):
    def get(self, request):
        login_form = UserLoginForm()
        return render(request, 'LITReview/index.html', {'login_form': login_form})

    def post(self, request):
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('flux')  # Rediriger vers une page appropriée après la connexion
            else:
                # Gérer l'échec de connexion
                return render(request, 'LITReview/index.html', {'login_form': login_form})

class Register(View):
    def get(self, request):
        registration_form = UserRegistrationForm()
        return render(request, 'LITReview/register.html', {'registration_form': registration_form})
    
    def post(self, request):
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            return redirect('index')
        else:
            return render(request, 'LITReview/register.html', {'registration_form': registration_form})

class Flux(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        return render(request, 'LITReview/flux.html')
    
    def post(self, request):
        pass

class DemandeCritique(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        demande_critique_form = DemandeCritiqueForm()
        return render(request, 'LITReview/demande_critique.html', {'demande_critique_form': demande_critique_form})
    
    def post(self, request):
        pass

class ProposerCritique(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        return render(request, 'LITReview/proposer_critique.html')
    
    def post(self, request):
        pass

