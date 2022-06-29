# Compte-rendu

Dans le cadre de la performance de haut-niveau, le CREPS des Pays de la Loire accompagne des structures sportives (Pôles Espoir, Pôles France), en mettant à leur disposition des outils de mesure et des compétences pour suivre les performances des sportifs au cours de leur entraînement. Le projet proposé ci-dessous concerne ce cadre et permettrait d’élargir les possibilités d’acquisition et d’analyse de données offertes aux structures.

Parmi les paramètres de performance mesurés, l’utilisation de cellules photoélectriques disposées « en portes » à différentes portions d’une piste permettent d’obtenir le temps réalisé par les pilotes sur les différents secteurs de course au cours d’un tour de piste complet. Si un tel dispositif permet de réaliser l’analyse de variables temporelles des pilotes par secteur de course, il ne permet pas d’obtenir les variations de ces variables à tous les instants de la course. De plus, le fonctionnement « en porte » des cellules photoélectriques contraint de réaliser les tours de piste de manière individuelle puisque les cellules ne distinguent pas quel pilote passe chacune des portes. D’autre part, les trajectoires empruntées et la distance parcourue par les pilotes sur la piste constituent des paramètres spatiaux, non mesurés par les cellules photo-électriques, importants à mesurer pour témoigner d’une performance au cours d’une course de BMX.

Ainsi, le projet propose de réaliser un outil permettant de recueillir, précisément, les temps et les trajectoires des pilotes au cours d’une course de BMX, et ce, de manière à ce que plusieurs pilotes puissent réaliser la course en simultané.

Une phase d’investigation préalable à permis de décerner les différentes possibilités d’acquisition des données de position et des temps de course.

# Investigations

Il a été déterminé plusieurs solutions possibles : calcul avec un IMU (centrale à inertie) et/ou un GPS.

La solution finale qui semble être la meilleure est l'implémentation avec l'intégration des données en provenance de l'IMU et du GPS. La compilation des deux capteurs peut permettre d'obtenir un résultat très précis et chacun d'entre eux corrigera l'erreur de l'autre.

## IMU

Un IMU est l’association de plusieurs capteurs : Accéléromètre, Gyroscope et Magnétomètre.

L’idée de la solution avec l’IMU est de compiler les données des capteurs pour tracer une trajectoire. La première difficulté est de traiter les données récupérées en ajoutant un filtre afin d’avoir des données exploitables.

## GPS

Une acquisition GPS permet de facilement récupérer les coordonnées des sportifs et de déterminer le franchissement de la ligne d’arrivée. Cependant, les données GPS sont soumises à une erreur due à l’acquisition satellites et aux différentes régulations gouvernementales. Afin de compenser cette erreur intrinsèque, plusieurs pistes ont été explorées.

# Solution d’arrivée

## Transpondeur et capteur RFID

L’utilisation de transpondeur permet la détection simultanée de plusieurs arrivées grâce à son identifiant unique de la balise. Le capteur est alors un tapis permettant de faire une détection différentiel plutôt que dans un rayon assurant une arrivé précise. Cette solution est plutôt onéreuse, mais permet une détection précise et simple d'implémentation.

## RFID

La puce RFID portée par le coureur lors du passage sur une zone d’acquisition permet de détecter son arrivée. Elle est peu onéreuse et on peut embarquer les informations que l'on veut dessus.

## RSSI

Captage de l’arrivée grâce à des ondes radios. Les vélos émettent à une certaine fréquence permettant de définir quel est le vélo qui passe la ligne d’arrivée. Les fréquences émises sont captées par les récepteurs placés à l’arrivée. On considère alors qu’un vélo est arrivé lorsque l’intensité de réception est à son maximum pour les deux récepteurs. Cette solution a déjà prouvé son efficacité sur les courses de drones et est peu onéreuse. Il peut cependant y avoir des interférences liées aux ondes radios.

# Solution de départ

## Détection grâce à l’impulsion électrique

La grille de départ possède une prise qui émet une impulsion électrique afin d’avertir du départ de la course. Il suffit alors de détecter cette impulsion électrique et de communiquer le départ. Cette solution est précise et peu onéreuse. Sachant qu'il n'existe que très peu de modèle de grille proposé par un seul vendeur, il n'y aura pas de problème de compatibilité. Cette solution demande cependant une manipulation supplémentaire aux entraîneurs qui doivent alors relier le boîtier au câble émettant l'impulsion électrique.

## Détection grâce au son

La grille de départ émet un son. La grille se baisse lors du 3ème BIP. On peut alors détecter le début de la course avec un micro. Il suffit de faire une analyse du son pour déterminer le départ. Cette solution à l'avantage de ne pas avoir besoin de se raccorder au câble de l'impulsion électrique et donc de limiter les interactions avec l'entraîneur. Solution également peu onéreuse, mais peut avoir des failles (départ détecté à cause d'un son étrangé ou bien départ non détecté à cause de bruit extérieur...)

# Applications

## Capteurs

Nous avons choisi des smartphones pour utiliser les capteurs GPS, Gyroscope, Accéléromètre et Magnétomètre.

## Acquisition capteurs

Une application mobile développée en react-native communique avec le serveur web socket les données acquises sur les smartphones.

## Serveur web socket

Coordonne l’interface web, les applications d’acquisition et l’API. Les canaux sont les suivants :

- Connexion des capteurs
- Déconnexion des capteurs
- Départ de la course
- Arrivée de la course

## Interface web

Une application web pensé pour l’utilisation sur smartphone permet d’enregistrer une piste en définissant une ligne de départ et d’arrivé en plaçant des balises sur une intégration de Google Maps. Une salle d’attente est créée lors de la sélection d’une piste, les capteurs actifs sont affichés sur l’écran. Un bouton permet de débuter la course et de la terminer.

## API

La mission de l'API est de permettre l'interaction avec la base de données MySQL.
Elle peut être implémentée en n'importe quelle technologie, elle permet seulement d'accéder à la base de données.

## Base de données

La base de données contient toutes les informations nécessaires au fonctionnement de l'application. Dans notre cas, elle enregistre les pistes, les courses, les capteurs, les enregistrements et elle fait les liens avec tout cela. Celle-ci peut être remplacée par n'importe quelle autre base de données. Cependant le côté relationnel nous simple intéressant, car il permet de lier les données et donc de les récupérer plus facilement. 

# Traitement des données

## Correction des erreurs GPS / GPS différentiel

L’utilisation de borne GPS fixe à position exacte connues permettent de compenser l’erreur qui est une constante dans une zone géographique données.

## Visualisation des données

Une visualisation affichée sur la piste en vue satellite permet de suivre la trajectoire du coureur.
Ayant les données brutes dans la base de données. La visualisation et le traitement des données peuvent se faire au choix.