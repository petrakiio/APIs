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
    img = models.ImageField(
        upload_to='perfil/',
        default='perfil/icon.jpeg',
        blank=True,
        null=True
    )
    codigo_id = models.CharField(max_length=25,unique=True)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.nome

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

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


class FriendshipRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_DECLINED = 'declined'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendente'),
        (STATUS_ACCEPTED, 'Aceito'),
        (STATUS_DECLINED, 'Negado'),
    ]

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_friend_requests'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_friend_requests'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')
