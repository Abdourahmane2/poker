#creer des test unitaires pour les fonctions de la classe PokerGame
import json
from django.test import TestCase
from django.urls import reverse 
from .models import  fonctionnalite, joueur, vote 
from django.core.files.uploadedfile import SimpleUploadedFile
class index(TestCase):
    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        
class PokerGameTest(TestCase):
    def debut(self):
        self.url = reverse('start_game')
        
    def joueur(self):
        data = {
            'mode': 'unanime',
            'player_names': 'Alice, Bob, Charlie',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(joueur.objects.count(), 3)    
        
    def backblog(self):
        backlog_data = json.dumps([
            {"id": 1, "title": "Fonct1", "description": "Description1"},
            {"id": 2, "title": "Fonct2", "description": "Description2"},
        ])
        backlog_file = SimpleUploadedFile("backlog.json", backlog_data.encode('utf-8'), content_type="application/json")
        data = {
            'mode': 'unanime',
            'player_names': 'Alice, Bob',
            'backlog': backlog_file,
        }
        response = self.client.get(reverse('backblog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pokergame/backblog.html')                    
        
     
   
class voter :
    def debut(self):
        self.joueur1 = joueur.objects.create(nom='Alice')
        self.joueur2 = joueur.objects.create(nom='Bob')
        self.fonctionnalite1 = fonctionnalite.objects.create(id=1, titre='Fonction 1', description='Desc 1')
        self.url = reverse('voter')
        self.client.session['joueurs'] = [self.joueur1.id, self.joueur2.id]
        self.client.session['current_joueur_index'] = 0
        self.client.session['current_fonctionnalite_index'] = 0
        self.client.session['mode'] = 'unanime'
        self.client.session.save()  
        
    def creer_vote(self) :
        data = {'button_value': '5'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(vote.objects.count(), 1)   
        
    
class passer_fonctionnalite_suivante :
    def setUp(self):
        self.fonctionnalite1 = fonctionnalite.objects.create(id=1, titre='Fonct1', description='Description1')
        self.fonctionnalite2 = fonctionnalite.objects.create(id=2, titre='Fonction2', description='Description2')
        self.url = reverse('passer_a_la_suivante')
        self.client.session['current_fonctionnalite_index'] = 0
        self.client.session.save()

    def test_pass_to_next_feature(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session['current_fonctionnalite_index'], 1)    