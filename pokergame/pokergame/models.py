from django.db import models

class joueur(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class fonctionnalite(models.Model):
    id = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self):
        return self.titre

class vote(models.Model):
    joueur = models.ForeignKey(joueur, on_delete=models.CASCADE)
    fonctionnalite = models.ForeignKey(fonctionnalite, on_delete=models.CASCADE)
    valeur = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.joueur.nom}, {self.valeur}, {self.fonctionnalite.titre}"
