from django.forms import *
from core.base.models import Categoria, Eventos, Productos, Beneficiario, Reserva, Suministro, Libro, Autor
from django.core.exceptions import ValidationError
from datetime import datetime


class ReservaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['libro'].widget.attrs['autofocus'] = True

    class Meta:
        model = Reserva
        fields = ('libro','beneficiario','fecha')
        widgets = {
            'libro': Select(
                attrs={
                    'placeholder': 'Ingrese el titulo del Libro',
                }
            ),
            'beneficiario': Select(
                attrs={
                    'placeholder': 'Ingrese el nombre del Evento',
                }
            ),
            'fecha': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha',
                    'data-target': '#fecha',
                    'data-toggle': 'datetimepicker',
                }
            ),
        }
    def clean_libro(self):
        libro = self.cleaned_data['libro']
        if libro.cantidad < 1:
            raise ValidationError('No se puede reservar este libro, deben existir unidades disponibles.')

        return libro

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
    
class EventosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Eventos
        fields ='__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del Evento',
                }
            ),
            'tipoEvento': TextInput(
                attrs={
                    'placeholder': 'Ingrese el tipo de Evento',
                }
            ),
             'fecha': DateTimeInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha',
                    'data-target': '#fecha',
                    'data-toggle': 'datetimepicker',
                }
             ),
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese la ubicación del Evento',
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


class LibroForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].widget.attrs['autofocus'] = True

    class Meta:
        model = Libro
        fields =('titulo','autor','f_publicacion','genero','descripcion','imagen','cantidad')
        widgets = {
            'titulo': TextInput(
                attrs={
                    'placeholder': 'Ingrese el titulo del Libro',
                }
            ),
            'autor': Select(
                attrs={
                    'class': 'select2', 
                    'style': 'width: 100%'
                }
            ),
            'f_publicacion': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'f_publicacion',
                    'data-target': '#f_publicacion',
                    'data-toggle': 'datetimepicker',
                }
            ),
            'genero': TextInput(
                attrs={
                    'placeholder': 'Ingrese el Genero del Libro',
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
        fields = ('nombres', 'nacionalidad', 'descripcion')
        widgets = {
            'nombres': TextInput(
                attrs={
                    'placeholder': 'Ingrese los nombres y apellidos',
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
             'cumpleaños': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'cumpleaños',
                    'data-target': '#cumpleaños',
                    'data-toggle': 'datetimepicker',
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
        self.fields['beneficiario'].queryset = Beneficiario.objects.none()
        
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
    