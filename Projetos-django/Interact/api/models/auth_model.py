from django.db import models
from django.contrib.auth.hashers import make_password,check_password
from django.core.exceptions import ValidationError

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

    def tratamento(senha):
        return make_password(senha)

    def Singup(self):
        try:
            self.full_clean()
            self.save()
            return True
        except ValidationError as e:
            print('erro:',e)
            return False
        