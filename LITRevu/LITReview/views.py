from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserLoginForm, UserRegistrationForm, ProposerCritiqueForm, DemandeTicketForm, UserSearchForm
from .models import Ticket, Review, UserFollows
from django.views import View
# Explication : Q permet de faire des requetes complexes de type OR
from django.db.models import Q, Exists, OuterRef
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
        user_follows = UserFollows.objects.filter(user=request.user)

        # Récupérer les tickets et les reviews de l'utilisateur et de ses abonnés
        user_tickets = Ticket.objects.filter(Q(user=request.user) | Q(user__followed_by__user=request.user))
        user_reviews = Review.objects.filter(Q(user=request.user) | Q(user__followed_by__user=request.user))
        # Initialiser les listes
        ticket_critique = []
        ticket_only = []

        Ticket.objects.all().annotate(
            is_associated=Exists(Review.objects.filter(ticket=OuterRef('pk')))
        )
        # Parcourir les tickets et verifie si il y a un review et si il correspond à l'id d'un user_review
        for ticket in user_tickets:
            # Pour chaque ticket on verifie si il y a un review associé si il n'y en a pas on l'ajoute à la liste des tickets seuls
            if not Review.objects.filter(ticket=ticket):
                ticket_only.append(ticket)
            else:
                # Sinon on ajoute la review qui à pour ticket id le ticket
                ticket_critique.append(Review.objects.get(ticket=ticket))


        # Ajoute une valeur a chaque liste pour les differentier dans la template 
        for ticket in ticket_only:
            ticket.type = "ticket"
        for review in ticket_critique:
            review.type = "ticket_critique"

        # Créer une liste combinée pour le flux
        flux = list(ticket_only) + list(ticket_critique)
        flux.sort(key=lambda x: x.time_created, reverse=True)

        return render(request, 'LITReview/flux.html', {'flux': flux})

            
    def post(self, request):
        # Recupere le formulaire post de la page ticket_id
        action = request.POST.get('action')
        ticket = request.POST.get('ticket')
        
        if action == 'create':
            return render(request, 'LITReview/demande_ticket.html', {'ticket': ticket})
        else:
            return redirect('flux')
        
class CreerTicket(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        demande_ticket_form = DemandeTicketForm()
        demande_critique_form = ProposerCritiqueForm()

        return render(request, 'LITReview/demande_ticket.html', {
            'demande_ticket_form': demande_ticket_form,
            'demande_critique_form': demande_critique_form
            })
    
    def post(self, request):
        post_demande_ticket_form = DemandeTicketForm(request.POST, request.FILES)
        post_demande_critique_form = ProposerCritiqueForm(request.POST)
        if post_demande_ticket_form.is_valid() and post_demande_critique_form.is_valid():
            # On recupere le ticket de la demande de critique
            demande_ticket = post_demande_ticket_form.save(commit=False)
            # On recupere l'utilisateur
            demande_ticket.user = request.user
            # On sauvegarde le ticket
            demande_ticket.save()
            # On recupere la critique de la demande de critique
            demande_critique = post_demande_critique_form.save(commit=False)
            # On recupere l'utilisateur
            demande_critique.user = request.user
            # On sauvegarde la critique
            demande_critique.ticket = demande_ticket
            demande_critique.save()

        return redirect('flux')
class DemandeCritique(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        demande_critique_form = DemandeTicketForm()
        return render(request, 'LITReview/demande_critique.html', {'demande_critique_form': demande_critique_form})
    
    def post(self, request):
        post_demande_critique_form = DemandeTicketForm(request.POST)

        if post_demande_critique_form.is_valid():
            demande_critique = post_demande_critique_form.save(commit=False)
            demande_critique.user = request.user
            demande_critique.save()
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
        
    