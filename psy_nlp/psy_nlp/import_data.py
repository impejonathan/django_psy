from elasticsearch import Elasticsearch
from django.db import models

# Définition du modèle Patient
class Patient(models.Model):
    patient_lastname = models.CharField(max_length=100)
    patient_firstname = models.CharField(max_length=100)
    date = models.DateField()
    patient_left = models.BooleanField()
    text = models.TextField()
    emotion = models.CharField(max_length=100)

# Connexion à Elasticsearch
es = Elasticsearch(hosts=['http://localhost:9200'])

# Requête de recherche pour récupérer tous les documents
query = {
    "query": {
        "match_all": {}
    }
}

# Exécution de la requête de recherche
res = es.search(index='notes', body=query, size=10000)

# Récupération des résultats
hits = res['hits']['hits']

# Insertion des données dans la table patients
for hit in hits:
    doc = hit['_source']
    patient_lastname = doc['patient_lastname']
    patient_firstname = doc['patient_firstname']
    date = doc['date']
    patient_left = doc['patient_left']
    text = doc['text']
    emotion = doc['emotion']
    
    patient = Patient(
        patient_lastname=patient_lastname,
        patient_firstname=patient_firstname,
        date=date,
        patient_left=patient_left,
        text=text,
        emotion=emotion
    )
    patient.save()
