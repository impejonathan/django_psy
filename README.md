# django_psy
projet NLP a partie des note 


# Application Django pour les psychologues

Cette application Django permet aux psychologues de gérer les informations de leurs patients et d'analyser les émotions des textes écrits par les patients. L'application utilise une base de données PostgreSQL pour stocker les informations sur les patients et les psychologues, et une base Elasticsearch pour stocker les textes et les évaluations des émotions. Le front-end de l'application utilise Bootstrap pour un design moderne et réactif.

## Fonctionnalités

- Espace de connexion pour les psychologues
- Visualisation de la répartition des émotions des patients actifs sur une certaine période de temps
- Recherche de patients par nom et prénom
- Recherche de textes contenant une certaine expression avec des filtres pour les émotions et les noms/prénoms des patients
- Création de nouveaux patients avec un nom et un prénom
- Évaluation automatique des émotions des textes écrits par les patients en utilisant un modèle Hugging Face

## Installation

1. Clonez ce dépôt sur votre ordinateur.
2. Installez les dépendances en exécutant `pip install -r requirements.txt` dans le répertoire du projet.
3. Configurez les paramètres de connexion à votre base de données PostgreSQL et Elasticsearch dans le fichier `settings.py`.
4. Exécutez les migrations en exécutant `python manage.py migrate` dans le répertoire du projet.
5. Démarrez l'application en exécutant `python manage.py runserver` dans le répertoire du projet.

## Utilisation

1. Accédez à l'application en ouvrant votre navigateur web et en accédant à l'URL `http://localhost:8000`.
2. Connectez-vous en utilisant vos identifiants de psychologue ou créez un nouveau compte en cliquant sur le lien "S'inscrire".
3. Une fois connecté, vous pouvez accéder aux différentes fonctionnalités de l'application en utilisant le menu de navigation.
