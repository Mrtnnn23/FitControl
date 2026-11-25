from datetime import time, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from gimnasio.models import Clase, Entrenador


class Command(BaseCommand):
    help = 'Agrega tres clases futuras y distribuye las nuevas sesiones entre entrenadores activos.'

    @transaction.atomic
    def handle(self, *args, **options):
        entrenadores = list(Entrenador.objects.filter(
            usuario__is_active=True
        ).order_by('pk'))
        if not entrenadores:
            raise CommandError('No hay entrenadores con una cuenta activa. No se crearon clases.')

        hoy = timezone.localdate()
        sesiones = [
            ('Fuerza funcional', 1, 18, 'Sesión de fuerza y acondicionamiento.'),
            ('Movilidad y equilibrio', 2, 19, 'Sesión de movilidad y equilibrio.'),
            ('Entrenamiento integral', 3, 18, 'Sesión de entrenamiento de cuerpo completo.'),
        ]
        creadas = 0
        for indice, (nombre, dias, hora, descripcion) in enumerate(sesiones):
            clase, creada = Clase.objects.get_or_create(
                nombre=nombre,
                fecha=hoy + timedelta(days=dias),
                hora=time(hora),
                defaults={
                    'entrenador': entrenadores[indice % len(entrenadores)],
                    'descripcion': descripcion,
                    'cupo_maximo': 12,
                    'estado': 'Programada',
                },
            )
            creadas += int(creada)
            self.stdout.write(f'{clase.nombre}: {clase.fecha:%d/%m/%Y} {clase.hora:%H:%M}')

        self.stdout.write(self.style.SUCCESS(
            f'{creadas} clases creadas. Las clases, reservas y cuentas anteriores se conservaron.'
        ))
