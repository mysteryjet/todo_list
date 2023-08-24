from django import forms
from django.contrib.auth.forms import AuthenticationForm

'''
Se crea una clase de formulario que herede de AuthenticationForm, se establece la label
del campo de nombre de usuario y se asigna al LoginView sore el atributo authentication_form
'''
# class CustomAuthenticationForm(AuthenticationForm):
