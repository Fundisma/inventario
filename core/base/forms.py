from django.forms import *
from core.base.models import Categoria, Productos, Beneficiario, Suministro, Autor, Libro
from datetime import datetime

class LibroForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #for form in self.visible_fields():
         #   form.field.widget.attrs['class'] = 'form-control'
          #  form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['titulo'].widget.attrs['autofocus'] = True


    class Meta:
        model=Libro
        fields = '__all__'
        widgets = {
            'titulo': TextInput(
                attrs={
                    'placeholder': 'Ingrese el Titulo',
                }
            ),
            'autor': Select(
                attrs={
                    'class': 'select2', 
                    'style': 'width: 100%'
                }
            ),
            'f_publicacion': SelectDateWidget(
                attrs={
                    'placeholder': '',
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


class AutorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #for form in self.visible_fields():
         #   form.field.widget.attrs['class'] = 'form-control'
          #  form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombres'].widget.attrs['autofocus'] = True


    class Meta:
        model=Autor
        fields = '__all__'
        widgets = {
            'nombres': TextInput(
                attrs={
                    'placeholder': 'Ingrese los nombres',
                }
            ),
            'apellidos': TextInput(
                attrs={
                    'placeholder': 'Ingrese los apellidos',
                }
            ),
            'nacionalidad': TextInput(
                attrs={
                    'placeholder': 'Ingrese la nacionalidad',
                }
            ),
            'descripcion': Textarea(
                attrs={
                    'placeholder': 'Ingrese una breve descripción.',
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

    #def clean(self):
     #   cleaned = super().clean()
      #  if len(cleaned['nombre']) <= 50:
       #     raise forms.ValidationError('Validación mm')
        #    #self.add_error('nombre', 'le faltan caracteres')
       # return cleaned


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
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'descripcion': Textarea(
                attrs={
                    'placeholder': 'Ingrese su descripción',
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

    #def clean(self):
     #   cleaned = super().clean()
      #  if len(cleaned['nombre']) <= 50:
       #     raise forms.ValidationError('Validación mm')
        #    #self.add_error('nombre', 'le faltan caracteres')
       # return cleaned

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
            'tipoDocumento': Select(
                attrs={
                    'placeholder': '',
                }
            ),
            'documento': NumberInput(
                attrs={
                    'placeholder': 'Ingrese su numero de documento',
                }
            ),
            'cumpleaños': DateInput(format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                }
            ), 
            'telefono': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el número de teléfono',
                }
            ),
            'zona': Select(
                attrs={
                    'placeholder': 'Ingrese la zona',
                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'barrio': TextInput(
                attrs={
                    'placeholder': 'barrio',
                }
            ),
            
            'gender': Select(
            attrs={
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
    