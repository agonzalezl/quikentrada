from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Entradas(models.Model):
    id_entrada = models.AutoField(primary_key=True)
    fecha_compra = models.DateTimeField()
    nombre = models.CharField(max_length=25)
    apellido = models.CharField(max_length=25)
    dni = models.CharField(max_length=10)
    telefono = models.CharField(max_length=25)
    edad = models.IntegerField()
    email = models.CharField(max_length=50)
    id_evento = models.ForeignKey('Eventos', models.DO_NOTHING, db_column='id_evento')

    class Meta:
        managed = False
        db_table = 'entradas'


class Eventos(models.Model):
    id_evento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    imagen = models.FileField(max_length=75, blank=True, null=True)
    lugar = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=250)
    precio = models.DecimalField(max_digits=10, decimal_places=1)
    capacidad = models.IntegerField()
    entradas_vendidas = models.IntegerField(editable=False, default=0)
    consultas = models.IntegerField(editable=False, default=0)
    estado = models.CharField(max_length=25)
    tipo_evento = models.ForeignKey('TipoEventos', models.DO_NOTHING, db_column='tipo_evento')

    class Meta:
        managed = False
        db_table = 'eventos'
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return self.nombre


class Horarios(models.Model):
    id_horario = models.AutoField(primary_key=True)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    id_evento = models.ForeignKey(Eventos, models.DO_NOTHING, db_column='id_evento')

    class Meta:
        managed = False
        db_table = 'horarios'
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'


class TipoEventos(models.Model):
    id_tipoevento = models.AutoField(primary_key=True)
    nombre_tipoevento = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'tipo_eventos'
        verbose_name = 'Tipo de Evento'
        verbose_name_plural = 'Tipo de Eventos'

    def __str__(self):
        return self.nombre_tipoevento

class Sesiones(models.Model):
    id_sesion = models.AutoField(primary_key=True)
    sesion = models.DateTimeField()
    id_evento = models.ForeignKey(Eventos, models.DO_NOTHING, db_column='id_evento')

    class Meta:
        managed = False
        db_table = 'sesiones'
        verbose_name = 'Sesion'
        verbose_name_plural = 'Sesiones'

    def __str__(self):
        return "%s - %s"%(self.id_evento, self.sesion)

admin.site.register(Eventos)
admin.site.register(TipoEventos)
admin.site.register(Horarios)
admin.site.register(Sesiones)
