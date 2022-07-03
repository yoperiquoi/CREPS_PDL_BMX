## A propos du projet

Cette application permet à l'entraîneur  de choisir, de créer des pistes de BMX.
Quand une piste est sélectionnée il peut lancer une course, ce qui va permettre de centraliser la gestion des capteurs (vélos,relais...)

## Dépendances

- Angular 14 (https://angular.io/docs)
- @angular/google-maps (https://www.npmjs.com/package/@angular/google-maps)
- @angular/material (https://material.angular.io/)

## Lancer le projet

Rentrer sa clé API google map dans le fichier index.html

```html
 <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_KEY"></script>
````

Installer les dépendances : 
```sh
cd CREPS_BMX_CLIENT
npm install
````

Lancer le serveur de développement
```sh
ng serve --open
````

# Architecture

```sh
├───.vscode
└───src
    ├───app 
    │   ├───components
    │   │   └───navbar 
    │   ├───pages
    │   │   ├───course
    │   │   ├───courses-list
    │   │   ├───create
    │   │   └───start
    │   ├───services
    │   └───types
    ├───assets
    └───environments
````
components : où se situe les composants qui font partie d'une page
***
--- *navbar* : composant qui contient les balises qui permettent de gérer la navigation entre les différentes pages.

***
pages : où se situent les composants qui forment une page (page start associé au composant start etc)
***
--- *course* : composant pour une course qui a déjà été créée par l'entraîneur, il contient une vue aérienne de la course avec l'emplacement des balises.


--- *courses-list* : composant qui regroupe sous forme de liste l'ensemble des courses déjà créé par l'entraîneur et qui sont en BDD. En cliquant sur une course de la liste l'utilisateur est redirigé vers le composant *course* 

--- *create* : composant qui permet de à l'entraîneur de créer une piste, l'utilisateur se déplace sur une vue satellite et peut placer 4 balises : 2 arrivées et 2 départs. Une fois les balises positionnées l'entraîneur peut sauvegarder la piste en lui donnant un nom et lancer une course sur cette piste.

--- *start* : composant qui gère les capteurs, via des websockets on récupère les relais qui se connectent, l'entraîneur peut ainsi voir en direct quels relais sont fonctionnels. Une fois que les relais sont tous connecté il peut lancer la course.

***

service : le service *course.service* nous permet d'interagir avec notre API, c'est ici que les requêtes CRUD sont effectuées
- https://fr.wikipedia.org/wiki/CRUD
- https://angular.io/tutorial/toh-pt4

***

types : contient les définitions des types de données qui sont utilisées dans l'application.

*** 

assets : dossier regroupant les images/icon qui sont utilisées dans l'application

## Axe d'amélioration

- ajout de la possibilité de taper un lieu lors de la création d'une piste pour ne pas avoir à naviguer sur la map jusqu'à arriver au lieu

- ajout de l'image en vue satellite de la piste dans la liste des pistes (*course-lsit*)

- ajout d'autres types de capteur (différent de arrivée/départ) pour augmenter la précision du gps différentiel

- ajout de la possibilité de modifier une course existante quand on clique dessus dans le component *course* (pouvoir modifier la disposition des capteurs)

- utilisation d'un store NGRX pour gérer l'état de notre application (+ facile à maintenir ) 
    - https://ngrx.io/

