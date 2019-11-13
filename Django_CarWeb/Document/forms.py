from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms



class DocumentForm(forms.ModelForm):

    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Document
        fields = '__all__'




class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nombre de Usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))



class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))


    class Meta:
        model = User
        fields = ['username', 'password', 'email']



class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña actual'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Nueva contraseña'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar nueva contraseña'}))


    def clean(self):

        if self.cleaned_data['new_password'] != self.cleaned_data['confirm_password']:
            raise forms.ValidationError('Tus contraseñas no coinciden!')
        else:
            return self.cleaned_data




class DescriptionForm(forms.ModelForm):


    class Meta:
        model = Document

        fields = ['gps_northing', 'gps_easting','layers', 'gps_lat', 'gps_long']



class clasificadorform(forms.ModelForm):



    nombre = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nombre.. '}))
    coordinatex = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Coord x.. '}))
    coordinatey = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Coord y.. '}))
    coordinatez = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Coord z.. '}))
    path = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nombre.. '}))



    class Meta:

        model = clasificador
        fields = ['objetos','nombre','path','coordinatex','coordinatey','coordinatez',]


class Apiform(forms.Form):
    url = forms.URLField()