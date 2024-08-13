from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Producto
from .models import UserProfile
from django import forms

from .models import UserProfile

from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class CreateAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,label='Contraseña',)
    birthday = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}),label='Edad',)
    is_staff = forms.BooleanField(required=False, initial=True,label='Empleado',)  # Campo para indicar si es staff
    is_superuser = forms.BooleanField(required=False, initial=False,label='Administrador',)  # Campo para indicar si es superusuario

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'is_staff', 'is_superuser']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_staff = self.cleaned_data['is_staff']
        user.is_superuser = self.cleaned_data['is_superuser']
        if commit:
            user.save()
            UserProfile.objects.create(user=user, birthday=self.cleaned_data['birthday'])
        return user
        # ----------------------------------------------------------------------

class AltaProductoModelForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        labels = {
            'imagen_url': 'imagen',
            
            # Añade otras etiquetas según los campos de tu modelo
        }

    def clean_nombre(self):
        if not self.cleaned_data["nombre"]:
            raise ValidationError("el nombre solo puede poseer letras")
        return self.cleaned_data["nombre"]

    def clean_descripcion(self):
        if not self.cleaned_data["descripcion"]:
            raise ValidationError("la descripcion solo puede poseer letras")
        return self.cleaned_data["descripcion"]

# -------------------------------------------
class ActualizarPreciosForm(forms.Form):
    proveedor = forms.CharField(max_length=100, label='Proveedor')
    porcentaje_incremento = forms.DecimalField(max_digits=5, decimal_places=2, label='Porcentaje de Incremento')

# class AltaProductoForm(forms.Form):
#     nombre = forms.CharField(label='nombre del articulo', required=True,widget=forms.TextInput(attrs={'class' : 'campo-nombre'}))
#     descripcion= forms.CharField(label='descripcion', required=True)
#     precio=forms.IntegerField(label='precio ', required=True)
#     ean=forms.IntegerField(label='ean', required=True)
#     imagen_url = forms.URLField(label="Imagen del Producto")

#     def clean_nombre(self):
#         if not self.cleaned_data["nombre"].isalpha():
#             raise ValidationError("el nombre solo puede poseer letras")
#         return self.cleaned_data["nombre"]

#     def clean_descripcion(self):
#         if not self.cleaned_data["descripcion"].isalpha():
#             raise ValidationError("la descripcion solo puede poseer letras")
#         return self.cleaned_data["descripcion"]
# # validacion multiple
#     def clean(self):
#         cleaned_data = super().clean()
#         nombre = cleaned_data.get("nombre")
#         if nombre == "pelota":
#             raise ValidationError("el articulo ya existe")
            
#         if self.cleaned_data['ean'] < 1000000:
#             raise ValidationError("ean incorrecto")

#         return self.cleaned_data





