# authentication/views.py
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate , logout
from . import forms

from .models import Patient
from datetime import date, timedelta

# Create your views here.


def index(request):
    return render(request, 
                  'note_psy/index.html',
                  )
    
def logout_user(request):
    
    logout(request)
    return redirect('login')



def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Identifiants invalides.'
    return render(request, 'note_psy/login.html', context={'form': form, 'message': message})


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect('login')
    return render(request, 'note_psy/signup.html', context={'form': form})



# def patient_page(request):
#     patients = Patient.objects.all()
#     return render(request, 'note_psy/patient.html', context={'patients': patients})

def patient_page(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    patients = Patient.objects.filter(patient_left=True).order_by('patient_lastname', 'patient_firstname', '-date')

    if start_date and end_date:
        patients = patients.filter(date__range=(start_date, end_date))

    return render(request, 'note_psy/patient.html', context={'patients': patients})