from django.forms import *
from core.base.models import Categoria, Productos, Beneficiario, Suministro
from datetime import datetime

class CategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True 

    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre de la categoria',
                }
            ),
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus descripción',
                }
            ),
            
        }
        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class ProductosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Productos
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'categoria': Select(
                attrs={
                    'class': 'select2', 
                    'style': 'width: 100%'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class BeneficiarioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombres'].widget.attrs['autofocus'] = True 

    class Meta:
        model = Beneficiario
        fields = '__all__'
        widgets = {
            'nombres': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'apellidos': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'cedula': TextInput(
                attrs={
                    'placeholder': 'Ingrese su cédula',
                }
            ),
            'cumpleaños': DateInput(format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                }
            ), 
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'sexo': Select()
        }
        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data



class SuministroForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Suministro
        fields = '__all__'
        widgets = {
            'beneficiario': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'fecha_registro': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_registro',
                    'data-target': '#fecha_registro',
                    'data-toggle': 'datetimepicker',
                }
            ),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
        }
    