POUR TOUT EXECUTER FACILEMENT:
./execute.sh

POUR TOUT FERMER SANS PRISE DE TÊTE:
./kill_all.sh

——————— Ne pas oublier de bien tout installer ————————    

Pour générer l'apidoc :
- ouvrir un terminal dans le repertoire apidoc
- apidoc -i ../python

Pour lancer le serveur REST :
- se placer dans le repertoire python
- mettre les bons identifiants de la bdd dans le fichier database.ini
- mettre l'adresse où lancer le serveur REST dans rest_server.ini (localhost par défaut)
- python REST_server.py

Pour lancer l'application web :
- se placer dans le repertoire nodejs
- npm install
- node server.js
- ouvrir un navigateur et se rendre sur localhost:8080

Pour la base de données:
- installer postgresql
- lancer un terminal en se connectant au compte par default (par exemple) : sudo -u postgres psql postgres
- ensuite exécuter le scripte distributed_create.sql : \i PATH/distributed_create.sql
- le second fichier distributed_insert.sql servait principalement pour le debug, pas utile


Python:
- nécessite Python2 (notre code) et Python3 (code prof.)
- plusieurs packages à installer dont: requests, configparser, flask, psycopg2, time, datetime 
- il y a peu de commentaires (client & les classes database, rule, ..), car souvent le nom des fonctions parlent d’eux-mêmes
- cela dit, ce qui est important: serveur REST est très bien documenté :-)
