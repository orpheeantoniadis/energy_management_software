Pour générer l'apidoc :
- ouvrir un terminal dans le repertoire apidoc
- apidoc -i ../python

Pour lancer le serveur REST :
- se placer dans le repertoire python
- mettre les bon identifiants de la bdd dans le fichier database.ini
- mettre l'adresse où lancer le serveur REST dans rest_server.ini (localhost par défaut)
- python REST_server.py

Pour lancer l'application web :
- se placer dans le repertoire nodejs
- npm install
- node server.js
- ouvrir un navigateur et se rendre sur localhost:8080