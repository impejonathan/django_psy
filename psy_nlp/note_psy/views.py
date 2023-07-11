# authentication/views.py
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate , logout
from . import forms
import pandas as pd

from .models import Patient
from datetime import date, timedelta

from elasticsearch import Elasticsearch
es = Elasticsearch(hosts=['http://localhost:9200'])

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


# def patient_page(request):
#     patients = Patient.objects.filter(patient_left=True).order_by('patient_lastname', 'patient_firstname')

#     return render(request, 'note_psy/patient.html', context={'patients': patients})



# def patient_page(request):
#     patients = Patient.objects.filter(patient_left=True).order_by('patient_lastname', 'patient_firstname')
#     patients_emotions = []
#     for patient in patients:
#         res = es.search(index="notes", body={"query": {"match": {"text": patient.patient_lastname}}})
#         if res['hits']['hits']:
#             emotion = res['hits']['hits'][0]['_source']['emotion']
#         else:
#             emotion = 'Aucune donnée trouvée'
#         patients_emotions.append((patient, emotion))
#     return render(request, 'note_psy/patient.html', context={'patients_emotions': patients_emotions})

def patient_page(request):
    patients = Patient.objects.filter(patient_left=True).order_by('patient_lastname', 'patient_firstname')
    patients_emotions = []
    for patient in patients:
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"patient_lastname": patient.patient_lastname}},
                        {"match": {"patient_firstname": patient.patient_firstname}}
                    ]
                }
            }
        }
        res = es.search(index='notes', body=query)
        hits = res['hits']['hits']
        data = [hit['_source'] for hit in hits]
        df = pd.DataFrame(data)
        sentiment_counts = df['emotion'].value_counts(normalize=True)
        patients_emotions.append((patient, sentiment_counts))
    return render(request, 'note_psy/patient.html', context={'patients_emotions': patients_emotions})