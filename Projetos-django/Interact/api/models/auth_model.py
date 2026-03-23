from django.db import models
from django.contrib.auth.hashers import make_password,check_password
from django.core.exceptions import ValidationError
import secrets
import string

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

    @staticmethod
    def criptografia(senha):
        return make_password(senha)

    @staticmethod
    def create_code(tamanho=25):
        caracter = string.ascii_letters + string.digits
        return ''.join(secrets.choice(caracter) for _ in range(tamanho))        

    def Signup(self):
        try:
            self.full_clean()
            self.save()
            return True
        except ValidationError as e:
            print('erro:',e)
            return False
    
    def login(email,senha):
        try:
            user = User.objects.filter(email=email).first()
            if not user:
                return (False, 'Verifique seus dados')
            if not check_password(senha, user.senha):
                return (False, 'Verifique seus dados')
            return (True, user)
        except Exception as e:
            print('erro:', e)
            return (False, 'Erro inesperado')
