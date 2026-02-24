from django.db import models

# Create your models here.
class tarefaModel(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(null=True, blank=True)
    concluido = models.BooleanField(default=False)
    data_criacao = models.DateTimeField()

