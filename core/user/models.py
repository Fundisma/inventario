from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict
from crum import get_current_request
from inventario.settings import MEDIA_URL, STATIC_URL


class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True,verbose_name="Imagen" )
    class TipoDocumento(models.TextChoices):
        RC='Registro Civil', ('Registro Civil')
        TI='Tarjeta de Identidad', ('Tarjeta de Identidad')
        CC='Cédula de Ciudadanía', ('Cédula de Ciudadanía')
        CE='Cédula de Extrajería', ('Cédula de Extrajería')
        CR='Contraseña Registraduría', ('Contraseña Registraduria')
    tipoDocumento=models.CharField(max_length=25, choices=TipoDocumento.choices, default=TipoDocumento.RC, verbose_name="Tipo de Documento")
    documento = models.IntegerField( unique=True, verbose_name='Documento',null=True,blank=True)
    token = models.UUIDField(primary_key=False, editable=False,null=True,blank=True )

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions', 'last_login'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['image'] = self.get_image()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        return item

    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass