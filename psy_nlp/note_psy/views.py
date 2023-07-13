# views.py
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate , logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from . import forms
import pandas as pd

from .models import Patient
from datetime import date, timedelta

from transformers import pipeline


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
                return redirect('patients')
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



@login_required(login_url='login')
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


@login_required(login_url='login')
def texte_patient(request):
    emotion = ""
    if request.method == 'POST':
        text = request.POST.get('text')
        classifier = pipeline("sentiment-analysis", model="michellejieli/emotion_text_classifier")
        result = classifier(text)
        emotion = result[0]['label']
    return render(request, 'note_psy/texte_patient.html', {'emotion': emotion})


@login_required(login_url='login')
def recherche_patient(request):
    emotions = {}
    patient_found = False
    lastname = ""
    firstname = ""
    if request.method == 'POST':
        lastname = request.POST.get('lastname')
        firstname = request.POST.get('firstname')
        patient = Patient.objects.filter(patient_lastname=lastname, patient_firstname=firstname).first()
        if patient:
            patient_found = True
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
            emotions = df['emotion'].value_counts(normalize=True).to_dict()
    return render(request, 'note_psy/recherche_patient.html', {'emotions': emotions, 'patient_found': patient_found, 'lastname': lastname, 'firstname': firstname})


@login_required(login_url='login')
def recherche_text(request):
    results = []
    no_results = False
    if request.method == 'POST':
        expression = request.POST.get('expression')
        emotion = request.POST.get('emotion')
        lastname = request.POST.get('lastname')
        firstname = request.POST.get('firstname')
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match_phrase": {"text": expression}}
                    ]
                }
            }
        }
        if emotion:
            query['query']['bool']['must'].append({"match": {"emotion": emotion}})
        if lastname and firstname:
            query['query']['bool']['must'].extend([
                {"match": {"patient_lastname": lastname}},
                {"match": {"patient_firstname": firstname}}
            ])
        res = es.search(index='notes', body=query)
        hits = res['hits']['hits']
        results = [hit['_source'] for hit in hits]
        if not results:
            no_results = True
    return render(request, 'note_psy/recherche_text.html', {'results': results, 'no_results': no_results})


@login_required(login_url='login')
def creation_patient(request):
    if request.method == 'POST':
        lastname = request.POST['lastname']
        firstname = request.POST['firstname']
        patient = Patient(patient_lastname=lastname, patient_firstname=firstname, patient_left=True)
        patient.save()
        message = f"Patient {lastname} {firstname} créé avec succès!"
        return render(request, 'note_psy/creation_patient.html', {'message': message})
    else:
        return render(request, 'note_psy/creation_patient.html')
