from django.test import TestCase

# Create your tests heref
from core.base.models import *
import random

data = ['arroz', 'verduras', 'coco', 'dedo']


letters =  ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 
            'ñ', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',]

for i in range(1, 6000):
    nombre = ''.join(random.choice(letters, k=5))
    while Categoria.objects.filter(nombre=nombre).exists():
        nombre = ''.join(random.choice(letters, k=5))
    Categoria(nombre=nombre).save()
    print('Guardado Registro {}'.format(i))