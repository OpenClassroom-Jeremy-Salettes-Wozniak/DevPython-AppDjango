from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserLoginForm, UserRegistrationForm, DemandeCritiqueForm, ProposerCritiqueForm, ProposerReviewForm, UserSearchForm
from .models import Ticket, Review, UserFollows
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
        # ETAPE 1 : On récupère les personnes qui qui l'utilisateur en cours
        user_follows = UserFollows.objects.filter(user=request.user)
        # On récupère les noms
        user_follows = [user_follow.followed_user for user_follow in user_follows]
        user_follows = [user_follow.username for user_follow in user_follows]
        # On rajoute l'user en cours dans la liste
        user_follows.append(request.user.username)
        # ETAPE 1 BIS : On rajoute l'user en cours dans la liste
        # La liste doit avoir des valeurs
        # ETAPE 2 : On récupère tout les ticket et review de tout le monde 
        tickets = Ticket.objects.all()
        reviews = Review.objects.all()
        # ETAPE 3 : J'affiche dans la template les ticket et review des personnes que je suis et moi même
        return render(request, 'LITReview/flux.html', {'followers': user_follows, 'tickets': tickets, 'reviews': reviews})

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

class Post(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        # On recupere les demandes de critiques
        demandes_critiques = Ticket.objects.filter(user=request.user)
        demandes_reviews = Review.objects.filter(user=request.user)
        
        return render(request, 'LITReview/posts.html', {'demandes_critiques': demandes_critiques, 'demandes_reviews': demandes_reviews})
    
    def post(self, request):
        pass

class Abonnements(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        # CREATE : Champ formulaire de recherche d'utilisateur
        recherche_form = UserSearchForm()
        # GET : On recupere les user_follows dans lesquels l'utilisateur est le follower
        user_follows = UserFollows.objects.filter(user=request.user)
        # GET : On vérifie les autres table et si la personne m'a dans ces abonnées on l'affiche
        all_user_follows = UserFollows.objects.all()
        followers = []
        for user_follow in all_user_follows:
            if user_follow.followed_user == request.user:
                followers.append(user_follow)

        return render(request, 'LITReview/abonnements.html', {'recherche_form': recherche_form, 'user_follows': user_follows, 'followers': followers})
    
        
    def post(self, request):
        action = request.POST.get('action')

        if action == 'recherche':
            recherche_form = UserSearchForm(request.POST)
            if recherche_form.is_valid():
                valeur_recherche = recherche_form.cleaned_data['followed_user']
                # On verifie si un utilisateur existe dans la db
                user_followed = User.objects.filter(username=valeur_recherche)
                # Si il existe un utilisateur
                if user_followed:
                    # On recupére l'utilisateur
                    user_followed = user_followed[0]
                    # On verifie si l'utilisateur est deja suivi
                    user_follows = UserFollows.objects.filter(user=request.user, followed_user=user_followed)
                    # Si il est deja suivi on ne fait rien
                    if user_follows:
                        return render(request, 'LITReview/abonnements.html', {'recherche_form': recherche_form})
                    # Sinon on le suit et on le redirige vers la page abonnements
                    else:
                        user_follow = UserFollows(user=request.user, followed_user=user_followed)
                        user_follow.save()
                        return redirect('abonnements')
        
        elif action == 'desabonner':
            user_follow_id = request.POST.get('user_follow_id')
            user_follow = UserFollows.objects.get(id=user_follow_id)
            print(user_follow)
            user_follow.delete()
            return redirect('abonnements')