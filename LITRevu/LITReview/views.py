from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserLoginForm, UserRegistrationForm, DemandeCritiqueForm, ProposerCritiqueForm, ProposerReviewForm
from .models import Ticket, Review
from django.views import View
# Create your views here.
class Disconnect(View):
    def get(self, request):
        logout(request)
        return redirect('index')

class Index(View):
    user = User

    def get(self, request):
        login_form = UserLoginForm()
        return render(request, 'LITReview/index.html', {'login_form': login_form})

    def post(self, request):
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data['username'],
                password=login_form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('flux')
            else:
                return render(request, 'LITReview/index.html', {'login_form': login_form})
        else:
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
        # On recupere les demandes de critiques
        demandes_critiques = Ticket.objects.filter(user=request.user)
        demandes_reviews = Review.objects.filter(user=request.user)
        return render(request, 'LITReview/flux.html', {'demandes_critiques': demandes_critiques, 'demandes_reviews': demandes_reviews})
    
    def post(self, request):
        pass

class DemandeCritique(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        demande_critique_form = DemandeCritiqueForm()

        return render(request, 'LITReview/demande_critique.html', {'demande_critique_form': demande_critique_form})
    
    def post(self, request):
        post_demande_critique_form = DemandeCritiqueForm(request.POST)
        if post_demande_critique_form.is_valid():
            demande_critique = post_demande_critique_form.save(commit=False)
            demande_critique.user = request.user
            demande_critique.save()
            return redirect('flux')

class ProposerCritique(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        proposer_critique_form = ProposerCritiqueForm()
        proposer_review_form = ProposerReviewForm()
        # Rating créer 5 bountons radio de notes pour les ratings

        return render(request, 'LITReview/proposer_critique.html', {'proposer_critique_form': proposer_critique_form, 'proposer_review_form': proposer_review_form})
    
    def post(self, request):
        post_proposer_critique_form = ProposerCritiqueForm(request.POST)
        post_proposer_review_form = ProposerReviewForm(request.POST)
        if post_proposer_critique_form.is_valid() and post_proposer_review_form.is_valid():
            proposer_critique = post_proposer_critique_form.save(commit=False)
            proposer_critique.user = request.user
            proposer_critique.save()
            proposer_review = post_proposer_review_form.save(commit=False)
            proposer_review.user = request.user
            proposer_review.ticket = proposer_critique
            proposer_review.save()
            return redirect('flux')

