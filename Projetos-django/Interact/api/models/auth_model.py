from django.db import models

class User(models.Model):
    nome = models.CharField(max_length=150)
    senha = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)
    descricao = models.CharField(max_length=300)
    codigo_id = models.CharField(max_length=25,unique=True)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.nome
