from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import joueur, fonctionnalite, vote
import json
from django.views.decorators.http import require_http_methods

def index(request):
    return render(request, 'index.html')

def start_game(request):
    # Nettoyer les votes et les joueurs existants pour éviter la duplication
    vote.objects.all().delete()  # Supprime tous les votes existants
    joueur.objects.all().delete()  # Supprime tous les joueurs existants pour un nouveau jeu

    if request.method == 'POST':
        mode = request.POST.get('mode')
        # Récupération et nettoyage des noms des joueurs
        noms = request.POST.get('player_names').split(',')
        nom_joueurs = [name.strip() for name in noms]

        # Création de nouveaux joueurs
        joueurs = []
        for name in nom_joueurs:
            if not joueur.objects.filter(nom=name).exists():  # Vérifie si le joueur existe déjà
                joueur_obj = joueur.objects.create(nom=name)
                joueurs.append(joueur_obj)

        # Traitement du fichier de backlog si fourni
        fichier = request.FILES.get('backlog')
        if fichier:
            file_content = fichier.read().decode('utf-8')
            backlog_data = json.loads(file_content)
            for fonct in backlog_data:
                if not fonctionnalite.objects.filter(id=fonct['id']).exists():  # Vérifie l'unicité par id
                    fonctionnalite.objects.create(
                        id=fonct['id'],
                        titre=fonct['title'],
                        description=fonct['description']
                    )
        
        # Initialisation de la session
        request.session['mode'] = mode
        request.session['joueurs'] = [j.id for j in joueurs]
        request.session['current_joueur_index'] = 0
        request.session['current_fonctionnalite_index'] = 0

        return render(request, 'game.html', {
            'joueurs': joueurs,
            'fonctionnalites': fonctionnalite.objects.all(),
            'current_joueur': joueurs[0] if joueurs else None,
            'current_fonctionnalite': fonctionnalite.objects.first() ,
            'mode' : mode
        })

    return render(request, 'index.html')


@require_http_methods(["GET", "POST"])
def voter(request):
   
    votes_data = []
    bon = False
    moyenne = 0 

    if request.method == 'POST':
        # Récupération des données nécessaires depuis la session
        joueurs_ids = request.session.get('joueurs', [])
        current_joueur_index = request.session.get('current_joueur_index', 0)
        current_fonctionnalite_index = request.session.get('current_fonctionnalite_index', 0)

        # Récupération de la valeur du vote depuis la requête POST
        vote_valeur = request.POST.get('button_value')

        # Validation des indices et récupération du joueur et de la fonctionnalité actuels
        if joueurs_ids and current_joueur_index < len(joueurs_ids):
            current_joueur = joueur.objects.get(id=joueurs_ids[current_joueur_index])
            fonctionnalites = fonctionnalite.objects.all()

            if current_fonctionnalite_index < len(fonctionnalites)  :
                request.session['fini'] = False
                current_fonctionnalite = fonctionnalites[current_fonctionnalite_index]

                # Création de l'enregistrement de vote
                vote.objects.create(
                    joueur=current_joueur,
                    fonctionnalite=current_fonctionnalite,
                    valeur=vote_valeur
                )

                # Récupération des votes pour cette fonctionnalité
                n = len(joueurs_ids)
                print(n)
                votes = vote.objects.filter(fonctionnalite=current_fonctionnalite)       
                print((votes))
                print(len(joueurs_ids))
                # Vérification si tous les joueurs ont voté pour cette fonctionnalité
                if current_joueur_index == len(joueurs_ids) - 1:
                   
                    vote_values = list(votes.values_list('valeur', flat=True))
                    request.session['cartes_bloquees'] = False
                    # Vérification si les votes sont les meme pour le mode unanime
                    if request.session.get('mode') == 'unanime':
                        print(vote_values)
                        bon = all(v == vote_values[0] for v in vote_values) if vote_values else False
                        print(bon)
                    else :
                        print(request.session.get('mode'))
                        #transformer les votes str en int pour calculer la moyenne
                        vote_values = [int(v) for v in vote_values]  
                        moyenne = sum(vote_values) / n
                    
                    
                    if not bon:
                        request.session['cartes_bloquees'] = True # Si les votes sont différents
                        #si les votes ne sont pas bon on supprime les votes pour cette fonctionnalite
                        #recuperer pour les afficher avant de les supprimer 
                        
                    else:
                        request.session['cartes_bloquees'] = True  # Bloquer les cartes si tous ont voté et c'est unanime
                    
                    # Réinitialiser l'index des joueurs
                    current_joueur_index = 0  
                    

                else:
                    # Passer au joueur suivant si ce n'est pas le dernier
                    print(current_joueur_index)
                    current_joueur_index += 1
                    request.session['cartes_bloquees'] = False 

                # Mettre à jour la session avec les nouveaux indices
                request.session['current_joueur_index'] = current_joueur_index

                # Préparer les données de votes pour l'interface
                votes_data = [{'joueur': v.joueur.nom, 'valeur': v.valeur} for v in votes]
                
                # Retour Json avec les informations nécessaires
                return JsonResponse({
                    'message': f"Vote de {current_joueur.nom} enregistré.",
                    'current_joueur': joueur.objects.get(id=joueurs_ids[current_joueur_index]).nom if joueurs_ids else "",
                    'current_fonctionnalite': current_fonctionnalite.titre,
                    'votes': votes_data,
                    'cartes_bloquees': request.session.get('cartes_bloquees', False),
                    'bon': bon  ,
                    'moyenne' : moyenne ,
                    'mode' : request.session.get('mode')
                    
                                        
                })
                
            else:
               
                return JsonResponse({"error": "Fonctionnalité non trouvée ou index incorrect", 
                                     })
        else:
            return JsonResponse({"error": "Joueur non trouvé ou index incorrect"}, status=400)

    elif request.method == 'GET':
        print(request.session.get('mode'))
        joueurs_ids = request.session.get('joueurs', [])
        n = len(joueurs_ids) 
        current_fonctionnalite_index = request.session.get('current_fonctionnalite_index', 0)
        fonctionnalites = fonctionnalite.objects.all()

        if current_fonctionnalite_index < len(fonctionnalites):
             current_fonctionnalite = fonctionnalites[current_fonctionnalite_index]
             votes_queryset = vote.objects.filter(fonctionnalite=current_fonctionnalite).order_by('-created_at')[:n]
             votes = list(reversed(votes_queryset))
             # Vérifier si tous les votes sont identiques
             vote_values = [v.valeur for v in votes]  # Extraire les valeurs des votes 
             
             #verfifier si ils ont vote cafe
            
                         
             
             if request.session.get('mode') == 'unanime':
                bon = all(v == vote_values[0] for v in vote_values) if vote_values else False  # Vérifier l'unanimité
                print(bon) 
             else :
                 #transformer les votes str en int pour calculer la moyenne
                    vote_values = [int(v) for v in vote_values]
                    moyenne = sum(vote_values) / n   
                
                  
             votes_data = [{'joueur': v.joueur.nom, 'valeur': v.valeur} for v in votes_queryset]
            # Retour Json avec les informations sur l'unanimité et les votes
             return JsonResponse({
                'votes': votes_data,
                'bon': bon,
                'current_fonctionnalite': current_fonctionnalite.titre,
                'moyenne': moyenne,
                'mode': request.session.get('mode'),
                'cafe_mode': False,  
            })
            
        else:
            
            return JsonResponse({"error": "jeu termine"
                                    })

    # Requête non valide
    return JsonResponse({"error": "Méthode non supportée"}, status=400)


@require_http_methods(["POST"])
def passer_a_la_suivante(request):
    current_fonctionnalite_index = request.session.get('current_fonctionnalite_index', 0)
    fonctionnalites = fonctionnalite.objects.all()
    
    if current_fonctionnalite_index < len(fonctionnalites)-1:
        request.session['current_fonctionnalite_index'] += 1
        current_fonctionnalite = fonctionnalites[request.session['current_fonctionnalite_index']]
        return JsonResponse({
            "success": True,
            "message": "Passage à la fonctionnalité suivante.",
            'current_fonctionnalite': current_fonctionnalite.titre,
            'suivant'  :True
        })
    else:
        #telecharger les donnees
        telecharger_donne(request)
        return JsonResponse(
            { "suivant" : False}
        ) 
@require_http_methods(["POST"])       
def revenir_menu_principal(request):
    return render(request, 'index.html')  

#telecharger les donne format json 
def telecharger_donne(request):
    votes = vote.objects.select_related('fonctionnalite', 'joueur').all()
    fonctionnalites_votes = {}
    
    # Regrouper les votes par fonctionnalité
    for v in votes:
        fonction_id = v.fonctionnalite.id
        if fonction_id not in fonctionnalites_votes:
            fonctionnalites_votes[fonction_id] = {
                "fonctionnalite": v.fonctionnalite,
                "valeurs": []
            }
        fonctionnalites_votes[fonction_id]["valeurs"].append(v.valeur)
    
    # Analyser les votes pour chaque fonctionnalité
    fichier = []
    for fonction_id, data in fonctionnalites_votes.items():
        valeurs = data["valeurs"]
        fonctionnalite = data["fonctionnalite"]
        
        # Vérifier si toutes les valeurs sont identiques
        if all(val == valeurs[0] for val in valeurs):
            fichier.append({
                "id": fonctionnalite.id,
                "title": fonctionnalite.titre,
                "description": fonctionnalite.description,
                "valeur": valeurs[0], 
            })
    # Préparer la réponse HTTP pour le téléchargement
    response = HttpResponse(json.dumps(fichier,), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="votes.json"'
    return response
    
   
   
  


