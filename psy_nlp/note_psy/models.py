# models.py
from django.db import models

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    patient_lastname = models.CharField(max_length=100)
    patient_firstname = models.CharField(max_length=100)
    date = models.DateField()
    patient_left = models.BooleanField()

    class Meta:
        db_table = 'liste_patients'
