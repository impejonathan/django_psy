# # models.py
from django.db import models

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    patient_lastname = models.CharField(max_length=100)
    patient_firstname = models.CharField(max_length=100)
    patient_left = models.BooleanField()

    class Meta:
        db_table = 'liste_patients'


# # models.py
# from django.db import models
# from django.contrib.auth.models import User

# class Patient(models.Model):
#     id = models.AutoField(primary_key=True)
#     patient_lastname = models.CharField(max_length=100)
#     patient_firstname = models.CharField(max_length=100)
#     patient_left = models.BooleanField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     class Meta:
#         db_table = 'liste_patients'
