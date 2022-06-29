# Compte-rendu

Dans le cadre de la performance de haut-niveau, le CREPS des Pays de la Loire accompagne des structures sportives (Pôles Espoir, Pôles France), en mettant à leur disposition des outils de mesure et des compétences pour suivre les performances des sportifs au cours de leur entraînement. Le projet proposé ci-dessous concerne ce cadre et permettrait d’élargir les possibilités d’acquisition et d’analyse de données offertes aux structures.

Parmi les paramètres de performance mesurés, l’utilisation de cellules photoélectriques disposées « en portes » à différentes portions d’une piste permettent d’obtenir le temps réalisé par les pilotes sur les différents secteurs de course au cours d’un tour de piste complet. Si un tel dispositif permet de réaliser l’analyse de variables temporelles des pilotes par secteur de course, il ne permet pas d’obtenir les variations de ces variables à tous les instants de la course. De plus, le fonctionnement « en porte » des cellules photoélectriques contraint de réaliser les tours de piste de manière individuelle puisque les cellules ne distinguent pas quel pilote passe chacune des portes. D’autre part, les trajectoires empruntées et la distance parcourue par les pilotes sur la piste constituent des paramètres spatiaux, non mesurés par les cellules photo-électriques, important à mesurer pour témoigner d’une performance au cours d’une course de BMX.

Ainsi, le projet propose de réaliser un outil permettant de recueillir, précisément, les temps et les trajectoires des pilotes au cours d’une course de BMX et ce, de manière à ce que plusieurs pilotes puissent réaliser la course en simultané

Une phase d’investigation préalable à permis de décerner les différentes possibilités d’acquisition des données de position et des temps de course.

# Investigations

Il a été déterminer plusieurs solutions possibles : calcul avec un IMU et/ou un GPS.

## IMU

Un IMU est l’association des plusieurs capteurs: Accéléromètre, Gyroscope et Magnétomètre.

L’idée avec l’IMU est de compiler les données des capteurs pour tracer une trajectoire. La première difficulté est de traité les données récupérées en ajoutant un filtre afin d’avoir des données exploitables.

## GPS

Une acquisition GPS permet de facilement récupérer les coordonnées des sportifs et de determiner le franchissement de la ligne d’arrivée. Cependant les données GPS sont soumise à une erreur dû à l’acquisition satellites et aux différentes régulations gouvernementales. Afin de compenser cette erreur intrinsèque plusieurs pistes ont été explorées.

# Solution d’arrivée

## Transpondeur

L’utilisation de transpondeur permet la détection simultanée de plusieurs arrivées grâce à son indentifiant unique de la balise. 

## RFID

La puce RFID porté par le coureur lors du passage sur une zone d’acquisition permet de détecter son arrivée.

## RSSI

Captage de l’arrivée grâce à des ondes radios. Les vélos émettent à une certaine fréquence permettant de définir quel est le vélo qui passage la ligne d’arrivée. Les fréquences émises sont captées par les récepteur placé à l’arrivé. On considère alors qu’un vélo est arrivé lorsque l’intensité de réception est à son maximum. 

# Solution de départ

## Détection grâce à l’impulsion électrique

La grille de départ possède une prise qui émet une impulsion électrique afin d’avertir du départ de la course. Il suffit alors de détecter cette impulsion électrique et de communiquer le départ.

## Détection grâce au son

La grille de départ émet un son. La grille se baisse lors du 3ème BIP. On peut alors détecter le début de la course avec un micro.

# Applications

## Capteurs

Des smartphones sont utilisés comme capteur GPS, Gyroscope, Accéléromètre et Magnétomètre.

## Acquisition capteurs

Une application mobile développée en react-native communique avec le serveur web socket les données acquises sur les smartphones.

## Serveur web socket

Coordonne l’interface web, les applications d’acquisition et l’API. Les canaux sont les suivants :

- Connection des capteurs
- Déconnection des capteurs
- Départ de la course
- Arrivée de la course

## Interface web

Une application web pensée pour l’utilisation sur smartphone permet d’enregistrer une piste en définissant une ligne de départ et d’arrivé en plaçant des balises sur une intégration de google Maps. Une salle d’attente est créée lors de la sélection d’une piste, les capteurs actifs sont affichés sur l’écran. Un bouton permet de débuter la course et de la terminée

## API

La base de données communique avec le serveur web socket pour l’enregistrement des données. L’application d’acquisition se base également sur l’API pour acquérir la liste des capteurs disponibles.

## Base de données

La base de données contient les capteurs, les pistes et les enregistrements. 

# Traitement des données

## Correction des erreurs GPS

L’utilisation de borne GPS fixe à position exacte connues permettent de compenser l’erreur qui est une constante dans une zone géographique données.

## Visualisation des données

Une visualisation affichée sur la piste en vue satellite permet de suivre la trajectoire du coureur.