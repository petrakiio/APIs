import random
import string

alfabeto_minusculo = list(string.ascii_lowercase)
alfabeto_maiusculo = list(string.ascii_uppercase)
alfabeto_misturado = alfabeto_minusculo + alfabeto_maiusculo
alfabeto = "".join(alfabeto_misturado)
tratado = alfabeto+'1234567890'
# O segredo: sample pega todos os caracteres (len) de forma aleatória
embaralhado = "".join(random.sample(tratado, len(tratado)))
codi = embaralhado[6]
print(embaralhado)
print(codi)