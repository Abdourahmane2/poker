from django.shortcuts import render  
from django.http import JsonResponse
from .models import joueur, fonctionnalite, vote 
import json


def index(request):
    return render(request, 'index.html')


def start_game(request):
    voter = vote.objects.all()
    voter.delete() 
    if request.method == 'POST':
        # Récupération des noms de joueurs et création d'instances de modèle
        noms = request.POST.get('player_names').split(',')
        nom_joueurs = [name.strip() for name in noms]

        # Création des objets 'joueur'
    
        joueurs = [joueur.objects.create(nom=name) for name in nom_joueurs]

        # Gestion du fichier JSON (backlog)
        fichier = request.FILES.get('backlog')
        if fichier:
            file_content = fichier.read().decode('utf-8')
            backlog_data = json.loads(file_content)

            # Création des objets 'fonctionnalité' dans la base de données
            for fonct in backlog_data:
                if not fonctionnalite.objects.filter(id=fonct['id']).exists():
                    fonctionnalite.objects.create(
                        id=fonct['id'],
                        titre=fonct['title'],
                        description=fonct['description']
                    )


        # Stocker les joueurs et les fonctionnalités dans la session
         
        request.session['joueurs'] = [j.id for j in  joueurs]
           #stocker lid des jouers

        request.session['current_joueur_index'] = 0  #stoker lindex du jouer courant
        request.session['current_fonctionnalite_index'] = 0  #stoker la fonctionnalite courante

        # Rediriger vers la page de jeu avec les joueurs et les fonctionnalités
        return render(request, 'game.html', {
            'joueurs': joueurs,
            'fonctionnalites': fonctionnalite.objects.all(),
            'current_joueur': joueurs[0],  # Afficher le premier joueur à voter
            'current_fonctionnalite': fonctionnalite.objects.first()  # Première fonctionnalité
        })
        

    return render(request, 'index.html')

def voter(request):
    request.session['cartes_bloquees'] = False
    
    if request.method == 'POST':
        joueurs_ids = request.session.get('joueurs')
        current_joueur_index = request.session.get('current_joueur_index', 0)
        current_fonctionnalite_index = request.session.get('current_fonctionnalite_index', 0)

        # Obtenir le joueur et la fonctionnalité actuels 
        current_joueur = joueur.objects.get(id=joueurs_ids[current_joueur_index])
        current_fonctionnalite = fonctionnalite.objects.all()[current_fonctionnalite_index]

        # Enregistrer le vote
        vote_valeur = request.POST.get('button_value')
        son_vote = vote.objects.create(joueur=current_joueur, fonctionnalite=current_fonctionnalite, valeur=vote_valeur)

        # Avancer au joueur suivant ou activer les votes
        if current_joueur_index < len(joueurs_ids) - 1:
            current_joueur_index += 1
        else:
            # Tous les joueurs ont voté, bloquer les cartes pour affichage des résultats
            request.session['cartes_bloquees'] = True
            current_joueur_index = 0

        request.session['current_joueur_index'] = current_joueur_index

        # Obtenez les votes pour la fonctionnalité actuelle et vérifiez l'unanimité
        votes = vote.objects.filter(fonctionnalite=current_fonctionnalite)
        valeurs = [v.valeur for v in votes]
        unanimous = len(set(valeurs)) == 1

        # Réponse JSON pour le front-end
        return JsonResponse({
            'message': f"Vote de {current_joueur.nom} enregistré.",
            'current_joueur': joueur.objects.get(id=joueurs_ids[current_joueur_index]).nom,
            'current_fonctionnalite': current_fonctionnalite.titre,
            'votes': [{'joueur': v.joueur.nom, 'valeur': v.valeur} for v in votes],
            'cartes_bloquees': request.session.get('cartes_bloquees'),
            'unanimous': unanimous  # Ajout pour indiquer l'unanimité
        })
    
    return JsonResponse({"error": "Invalid request"}, status=400)

def compare_votes(request):
    if request.method == 'GET':
        current_fonctionnalite_index = request.session.get('current_fonctionnalite_index', 0)
        current_fonctionnalite = fonctionnalite.objects.all()[current_fonctionnalite_index]

        # Récupérer tous les votes pour la fonctionnalité en cours
        votes = vote.objects.filter(fonctionnalite=current_fonctionnalite)
        valeurs = [v.valeur for v in votes]

        # Vérifier l'unanimité
        unanimous = len(set(valeurs)) == 1

        if unanimous:
            # Si les votes sont identiques, passer à la fonctionnalité suivante
            request.session['current_fonctionnalite_index'] += 1
        else:
            # Sinon, on garde la même fonctionnalité
            request.session['current_fonctionnalite_index'] = current_fonctionnalite_index

        # Renvoyer le statut d’unanimité
        return JsonResponse({
            'unanimous': unanimous,
            'message': "Les votes sont identiques, passage à la prochaine fonctionnalité." if unanimous else "Les votes diffèrent, revotez pour la même fonctionnalité."
        })
    return JsonResponse({"error": "Invalid request"}, status=400)