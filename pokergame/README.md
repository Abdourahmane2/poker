# PokerGame

## Description
L'objectif de l'application est de permettre à des joueurs de faire une partie de planning poker
Avec cette application les membres de l'application peuvent :
 -  Participer à une session  
 -  Estimer  la complexité des fonctionnalités 
  - Importer un backlog sous forme de fichier JSON pour le traiter directement dans l'application.
 -  Exporter les résultats des votes sous format JSON pour une analyse ou une documentation ultérieure.


## Technologies utilisées 
 - Backend : Django (Framework Python)
 - Frontend : HTML/CSS (intégré dans les templates Django)
 - Base de données : SQLite 
 - JSON : Pour l'import/export de données de backlog et de résultats.


## Installation
Pour installer ce projet, suivez les étapes ci-dessous :

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/Abdourahmane2/poker.git
    ```
2. Accédez au répertoire du projet :
    ```bash
    cd pokergame
    ```

## Utilisation
Pour lancer le jeu, exécutez la commande suivante :
```bash
python manage.py runserver
```

## Fonctionnalités
- remplir le formulaire (choix du nombre de joueurs, choix des noms , mode de jeu et mettre un fichier format json avec la liste des fonctionnlites)
- chaque joueur choisi à tour de rôle la carte qu'il veut associer à une fonctionnalité, en fonction du mode de jeu choisi, on passe (ou pas) à la fonctionnalité suivante 
- si le jeu est terminé un fichier sera téléchargé 

## Contribuer
Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité 
3. Commitez vos modifications 
4. Poussez votre branche 
5. Ouvrez une Pull Request

## Licence
Ce projet est sous licence 

## Auteurs
 *Abdourahmane timera* - [https://github.com/Abdourahmane2]
 *Esin-Karsilayan* - [https://github.com/Esin-Karsilayan]



## Remerciements
- Merci à tous ceux qui ont contribué à ce projet.
