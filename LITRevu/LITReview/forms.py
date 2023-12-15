from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms import ModelForm
from LITReview.models import Ticket, Review, UserFollows

# Creation du formulaire semi-autonome de creation de compte
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            # password1 et password2 sont des mots de passe, on utilise donc le widget PasswordInput
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class UserLoginForm(forms.Form):
    username = forms.CharField(
        label="Nom d'utilisateur", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label="Mot de passe"
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Identifiants incorrects")

        return cleaned_data
    
# Creation du formulaire autonome de création de ticket
class DemandeCritiqueForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ProposerCritiqueForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            # Critique
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }   

class ProposerReviewForm(ModelForm):
    # Définir les choix de notes
    NOTE_CHOICES = [
        (1, '1 Étoile'),
        (2, '2 Étoiles'),
        (3, '3 Étoiles'),
        (4, '4 Étoiles'),
        (5, '5 Étoiles'),
    ]

    # Ajouter le champ de notes avec des boutons radio
    rating = forms.ChoiceField(
        choices=NOTE_CHOICES, 
        widget=forms.RadioSelect,
        label="Votre Note",
    )

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {
            'headline': 'Titre',
            'body': 'Commentaire',
            }
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

class UserSearchForm(forms.Form):
    followed_user = forms.CharField(
        label="",
        widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rechercher un utilisateur'})
    )
