# P12_EpicEvents
## Développement d'une architecture back-end sécurisée en utilisant Django ORM  
Les objectifs étant la création d'un CRM (Customer Relationship Manager) sécurisé intern à l'entreprise EpicEvents.

#### Ce projet utilise les technologies suivantes:  
- Python v3.x+
- Django v4.x+
- Docker
- PostgreSQL v13.x+
- virtual environnement  

#### La configuration par défaut nécessite une base de données PostgreSQL, vous devez l'installer ou modifier la configuration dans `setting.py`.
#### Dans le cadre de mon évaluation sur ce projet avec OpenClassRooms, vous trouverez dans le dépot de code les fichiers de configurations et d'accès pour la base de données actuelle qui ne devraient pas être en libre accès :  `.env` pour les secrets keys et `docker-compose.yml` configuration du docker.


## Installation

1. Cloner le depot de code à l'aide de la commande `https://github.com/B-asile/P12_EpicEvents.git` vous pouvez également télécharger le code ent tant qu'archive zip.
2. Créer un environnement virtuel : se rendre à la racine du projet puis effectuer les commandes `python -m venv env` sous windows ou `python3 -m venv env` sous mac ou linux.
3. Activer l'environnement virtuel avec `env\Scripts\activate` sous windows ou `source env/bin/activate` sous mac ou linux.
4. Installer les dépendances du projet avec la commande `pip install -r requirement.txt`.

- #### Si vous souhaitez utiliser la Database du depot :
5. Installez Docker sur la machine host via la page [Docker](https://www.docker.com/).  
6. Vous pouvez à présent Démarrer les conteneurs Docker contenant la DataBase et PGAdmin avec la commande ` docker-compose up` et lancer le server dans un second terminal avec la commande `python manage.py runserver`.
7. & éventuellement vous connecter sur le compte admin avec les identifiants suivants : email address = admin@epicevents.com / Password = Secret  

- #### Si vous ne souhaitez utiliser la Database existante :
5. Configurez `DATABASE`dans `setting.py` en fonction de vos choix.  
6. Effectuez les migrations avec les commandes `python manage.py makemigrations ` puis `python manage.py migrate`.
7. Les permissions de l'API ont besoins de groupes, vous devez accéder au repertoire `management` via la commande `python manage.py shell`. Une fois que dans l'interpréteur python, éxecutez le script `create_groups.py` via la commande `exec(open("core/management/create_groups.py").read())`, CTRL+d pour quitter.  
8. Créer un admin avec la commande `python manage.py createsuperuser`.  
9. vous pouvez démarrer le server `python manage.py runserver`.

## Documentation Postman de l'API:  

Une documentation Postman contenant les détails sur chaque point de terminaisons est disponible via [EpicEvents_documentation_Postman](https://www.postman.com/lively-trinity-225265/workspace/epicevents/api/eacc5abd-c537-466c-95d1-b15ebc28cd92?version=a9f00911-352a-4355-9999-b5304cddb663)