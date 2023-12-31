"""psy_nlp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from note_psy import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.index ),
    path('', views.login_page, name='login'),
    path('signup', views.signup_page, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('patients/', views.patient_page, name='patients'),
    path('texte_patient/', views.texte_patient, name='texte_patient'),
    path('recherche_patient/', views.recherche_patient, name='recherche_patient'),
    path('recherche_text/', views.recherche_text, name='recherche_text'),
    path('creation_patient/', views.creation_patient, name='creation_patient'),
]
