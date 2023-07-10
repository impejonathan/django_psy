# models.py
from django.db import models

class Patient(models.Model):
    # Remplacez 'nom_de_la_colonne' par le nom réel de votre clé primaire
    ma_cle_primaire = models.IntegerField(primary_key=True)
    patient_lastname = models.CharField(max_length=100)
    patient_firstname = models.CharField(max_length=100)
    date = models.DateField()
    patient_left = models.BooleanField()

    class Meta:
        db_table = 'patients'
