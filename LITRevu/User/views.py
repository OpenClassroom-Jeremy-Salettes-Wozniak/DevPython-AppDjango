from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.views import View
from django.contrib.auth import authenticate, login

# Create your views here.
class index(View):
    def get(self, request):
        registration_form = UserRegistrationForm()
        login_form = UserLoginForm()
        return render(request, 'user/index.html', {'registration_form': registration_form, 'login_form': login_form})

    def post(self, request):
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Rediriger vers une page appropriée après la connexion
            else:
                # Gérer l'échec de connexion

                return render(request, 'user/index.html', {'login_form': login_form})

class register(View):
    def get(self, request):
        registration_form = UserRegistrationForm()
        return render(request, 'user/register.html', {'registration_form': registration_form})
    
    def post(self, request):
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            return redirect('index')
        else:
            return render(request, 'user/register.html', {'registration_form': registration_form})
        