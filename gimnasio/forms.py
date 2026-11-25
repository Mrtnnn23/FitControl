from uuid import uuid4
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Socio, Entrenador, Membresia, Pago, Clase

class EstiloForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        etiquetas = {
            'rut': 'RUT',
            'telefono': 'Teléfono',
            'tipo_plan': 'Plan',
            'fecha_inicio': 'Fecha de inicio',
            'fecha_fin': 'Fecha de vencimiento',
            'fecha_pago': 'Fecha de pago',
            'metodo_pago': 'Método de pago',
            'descripcion': 'Descripción',
            'cupo_maximo': 'Cupos máximos',
        }
        opciones_vacias = {
            'socio': 'Selecciona un socio',
            'entrenador': 'Selecciona un entrenador',
            'membresia': 'Selecciona una membresía',
            'tipo_plan': 'Selecciona un plan',
            'metodo_pago': 'Selecciona un método de pago',
        }
        for nombre, field in self.fields.items():
            if nombre in etiquetas:
                field.label = etiquetas[nombre]
            if isinstance(field, forms.ModelChoiceField):
                field.empty_label = opciones_vacias.get(nombre, 'Selecciona una opción')
            elif isinstance(field, forms.ChoiceField):
                field.choices = [
                    (valor, opciones_vacias.get(nombre, 'Selecciona una opción') if valor == '' else etiqueta)
                    for valor, etiqueta in field.choices
                ]
            if isinstance(field, forms.DateField):
                field.widget = forms.DateInput(format='%Y-%m-%d', attrs={'type':'date'})
            elif isinstance(field, forms.TimeField):
                field.widget = forms.TimeInput(format='%H:%M', attrs={'type':'time'})

class PersonaForm(EstiloForm):
    clave = forms.CharField(label='Contraseña de acceso', required=False, widget=forms.PasswordInput,
        help_text='Obligatoria al crear la cuenta. Al editar, déjala vacía para conservarla.')
    def clean_clave(self):
        clave = self.cleaned_data.get('clave')
        if not clave and not self.instance.usuario_id:
            raise ValidationError('Ingresa una contraseña para la cuenta.')
        if clave:
            validate_password(clave, self.instance.usuario if self.instance.usuario_id else None)
        return clave
    @transaction.atomic
    def save(self, commit=True):
        persona = super().save(commit=False)
        user = persona.usuario if persona.usuario_id else User(username='fc_' + uuid4().hex[:20])
        user.email = persona.correo
        user.first_name = persona.nombre
        if self.cleaned_data.get('clave'):
            user.set_password(self.cleaned_data['clave'])
        user.save()
        persona.usuario = user
        if commit:
            persona.save()
        return persona

class SocioForm(PersonaForm):
    class Meta:
        model = Socio
        fields = ['nombre','rut','correo','telefono']

class EntrenadorForm(PersonaForm):
    class Meta:
        model = Entrenador
        fields = ['nombre','rut','correo','telefono','especialidad']

class MembresiaForm(EstiloForm):
    class Meta:
        model = Membresia
        fields = ['socio','tipo_plan','precio','fecha_inicio','fecha_fin','estado']

class PagoForm(EstiloForm):
    class Meta:
        model = Pago
        fields = ['membresia','monto','fecha_pago','metodo_pago','estado']

class ClaseForm(EstiloForm):
    class Meta:
        model = Clase
        fields = ['nombre','descripcion','entrenador','fecha','hora','cupo_maximo','estado']

def perfil_form(model):
    class PerfilForm(EstiloForm):
        class Meta:
            fields = ['nombre','correo','telefono']
        @transaction.atomic
        def save(self, commit=True):
            persona = super().save(commit=commit)
            user = persona.usuario
            user.email, user.first_name = persona.correo, persona.nombre
            user.save(update_fields=['email','first_name'])
            return persona
    PerfilForm._meta.model = model
    PerfilForm.base_fields = forms.models.fields_for_model(model, fields=['nombre','correo','telefono'])
    return PerfilForm
