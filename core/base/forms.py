from django.forms import *
from core.base.models import Categoria, Eventos, Lector, Productos, Beneficiario, Reserva, Suministro, Libro, Autor, categoriaLibro, inventario
from django.core.exceptions import ValidationError
from datetime import datetime


class ReservaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['libro'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Reserva
        fields = ('libro','lector','fecha9','fecha8','estado')
        widgets = {
            'libro': Select(
                attrs={
                    'readonly':'True',
                    'class': 'select2', 
                    'style': 'width: 100%',

                }
            ),
            'lector': Select(
            
                attrs={
                    'class': 'select2', 
                    'style': 'width: 100%',
                    
                    

                }
            ),
            'fecha9': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha9',
                    'data-target': '#fecha9',
                    'data-toggle': 'datetimepicker',
                    'readonly': 'True' 
                    
            

                }
            ),
             'fecha8': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha8',
                    'data-target': '#fecha8',
                    'data-toggle': 'datetimepicker',
                   

                },
            ),
            'estado': NullBooleanSelect(
               
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

class ReservaUpdate(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Reserva
        fields = ('estado',)
        widgets = {
           
            'estado': NullBooleanSelect(
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
                    'placeholder': 'Ingrese el nombre del evento',
                    'style':'text-transform: capitalize;'
                }
            ),
            'tipoEvento': TextInput(
                attrs={
                    'placeholder': 'Ingrese el tipo de evento',
                    'style':'text-transform: capitalize;'
                }
            ),
             'fecha': DateTimeInput(
                format='%Y-%m-%d %H:%M:%S',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha',
                    'data-target': '#fecha',
                    'data-toggle': 'datetimepicker',
                }
             ),
            'descripcion': Textarea(
                attrs={
                    'placeholder': 'Ingrese la descripción del evento',
                }
            ),
            'ubicacion': TextInput(
                attrs={
                    'placeholder': 'Ingrese la ubicación del evento',
                    'style':'text-transform: capitalize;'
                }
            ),
            'estado': NullBooleanSelect(
               
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
        fields =('titulo','autor','categoriaLibro','f_publicacion','genero','descripcion','imagen','cantidad',)
        widgets = {
            'titulo': TextInput(
                attrs={
                    'placeholder': 'Ingrese el titulo del libro',
                    'style':'text-transform: capitalize;'
                }
            ),
            'autor': Select(
                attrs={
                    'class': 'select2', 
                    'style': 'width: 100%',
                }
            ),
            'categoriaLibro': Select(
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
                    'placeholder': 'Ingrese el género del Libro',
                    'style':'text-transform: capitalize;'
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
        fields = ('nombres', 'nacionalidad')
        widgets = {
            'nombres': TextInput(
                attrs={
                    'placeholder': 'Ingrese los nombres y apellidos',
                'style':'text-transform: capitalize;'
                }
            ),
            'nacionalidad': TextInput(
                attrs={
                    'placeholder': 'Ingrese la nacionalidad',

                'style':'text-transform: capitalize;'
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
                    'placeholder': 'Ingrese la categoía',
                'style':'text-transform: capitalize;'

                }
            ),
            'descripcion': Textarea(
                attrs={
                    'placeholder': 'Ingrese la descripción',
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
    
class CategoriaLibroForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo'].widget.attrs['autofocus'] = True

    class Meta:
        model = categoriaLibro
        fields = '__all__'
        widgets = {
            'codigo': NumberInput(
                attrs={
                    'placeholder': '000',

                }
            ),
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese la categoría del libro',
                    'style':'text-transform: capitalize;'

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
        fields = ('nombre', 'categoria', 'imagen','stock','pvp','estado')
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un producto',
                'style':'text-transform: capitalize;'

                }
            ),
            'categoria': Select(
                attrs={
                    'class': 'select2', 
                    'style': 'width: 100%'
                }
            ),
           
            'estado': NullBooleanSelect(
               
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

class InventarioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = inventario
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un producto',
                'style':'text-transform: capitalize;'

                }
            ),
            'categoria': Select(
                attrs={
                    'class': 'select2', 
                    'style': 'width: 100%'
                }
            ),
            'estado': NullBooleanSelect(
               
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
                    'placeholder': 'Ingrese los nombres',
                'style':'text-transform: capitalize;'

                }
            ),
            'apellidos': TextInput(
                attrs={
                    'placeholder': 'Ingrese los apellidos',
                'style':'text-transform: capitalize;'

                }
            ),
            'tipoDocumento': Select(
                attrs={
                    'placeholder': '',
                'style':'text-transform: capitalize;'

                }
            ),
            'documento': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el número de documento',
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
                'style':'text-transform: capitalize;'

                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',

                }
            ),
            'barrio': TextInput(
                attrs={
                    'placeholder': 'Barrio',
                'style':'text-transform: capitalize;'

                }
            ),
            
            'gender': Select(
            attrs={
                'style':'text-transform: capitalize;'
            
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

class LectorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombres'].widget.attrs['autofocus'] = True

    class Meta:
        model = Lector
        fields = '__all__'
        widgets = {
            'nombres': TextInput(
                attrs={
                    'placeholder': 'Ingrese los nombres',
                'style':'text-transform: capitalize;'

                }
            ),
            'apellidos': TextInput(
                attrs={
                    'placeholder': 'Ingrese los apellidos',
                'style':'text-transform: capitalize;'

                }
            ),
            'tipoDocumento': Select(
                attrs={
                    'placeholder': '',
                'style':'text-transform: capitalize;'

                }
            ),
            'documento': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el número de documento',
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
                'style':'text-transform: capitalize;'

                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'barrio': TextInput(
                attrs={
                    'placeholder': 'Barrio',
                'style':'text-transform: capitalize;'

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

