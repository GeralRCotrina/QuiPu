# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.translation import ugettext as _



class AuthCliente(models.Model):
    idauth_cliente = models.AutoField(primary_key=True)
    idauth = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='idauth')
    idcliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='idcliente')
    asignacion = models.FloatField()
    fecha_alta = models.DateField()
    fecha_baja = models.DateField()
    descripcion = models.CharField(max_length=120)
    activo = models.CharField(max_length=2,null=True,blank=True)

    class Meta:
        managed = False
        db_table = 'auth_cliente'

    def __str__(self):
        cadena="[{0}] {1} -{2}"
        return cadena.format(self.idcliente.codigo,self.idauth.alias,self.asignacion)

 
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

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


class ColCategoria(models.Model):
    idcolaborador_categoria = models.AutoField(primary_key=True)
    variable = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'col_categoria'

    def __str__(self):
        cadena="{0} - {1}."
        return cadena.format(self.variable,self.descripcion)


class AuthUser(models.Model):
    SEXO = (
        ('M', 'MASCULINO'),
        ('F', 'FEMENINO'),
    )
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField(default=0)
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField(default=0)
    is_active = models.IntegerField(default=1)
    date_joined = models.DateTimeField(blank=True, null=True)
    categoria = models.ForeignKey(ColCategoria, models.DO_NOTHING, db_column='categoria',default=1)
    pais = models.ForeignKey('Pais', models.DO_NOTHING, db_column='pais', blank=True, null=True, default=1) 
    codigo = models.CharField(max_length=9)
    alias = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    dni = models.CharField(max_length=8,blank=True, null=True)
    celular = models.CharField(max_length=12,blank=True, null=True)
    telefono = models.CharField(max_length=12,blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO)
    foto_perfil = models.ImageField(upload_to='photos',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'

        permissions = (
            ('es_manager',_('MANAGER')),
            ('es_leader',_('LEADER')),
        )

    def __str__(self):
        cadena="{0} - {1}, {2}"
        return cadena.format(self.username,self.first_name,self.last_name)
        



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


class Cliente(models.Model):
    idcliente = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=11)
    equipo = models.ForeignKey('Equipo', models.DO_NOTHING, db_column='equipo')
    cliente = models.CharField(max_length=35)
    idpais = models.ForeignKey('Pais', models.DO_NOTHING, db_column='idpais', blank=True, null=True)
    descripcion = models.CharField(max_length=75, blank=True, null=True)
    correlativo = models.CharField(max_length=3)
    ftes = models.CharField(max_length=10)
    zultima_modificacion = models.DateField(blank=True, null=True)
    zestado = models.CharField(max_length=1, blank=True, null=True,default='1')
    wi_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cliente'

    def __str__(self):
        cadena="{0} - {1}"
        return cadena.format(self.codigo,self.cliente)


###Colaborador 

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
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



class Dominio(models.Model):
    iddominio = models.AutoField(primary_key=True)
    responsable = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='responsable')
    codigo = models.CharField(max_length=15)
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'dominio'
        
    def __str__(self):
        cadena="{0}"
        return cadena.format(self.codigo)
 



class Dudas(models.Model):    
    ESTADO = (
        ('1', 'Solucionada'),
        ('2', 'Abierta'),
        ('3', 'Respondida'),
        ('4', 'Cancelada'),
    )
    AMBITO = (
        ('1', 'Externo'),
        ('2', 'Interno'),
    )
    CRITICIDAD = (
        ('1', 'Baja'),
        ('2', 'Media'),
        ('3', 'Alta'),
        ('4', 'Bloqueante'),
    )
    DOC_ENT_INC = (
        ('1', 'Si'),
        ('2', 'No'),
    )
    iddudas = models.AutoField(primary_key=True)
    task = models.ForeignKey('Task', models.DO_NOTHING, db_column='task')
    estado = models.CharField(max_length=1,choices=ESTADO,default=1)
    acc = models.CharField(max_length=8, blank=True, null=True)
    descripcion = models.CharField(max_length=150)
    respuesta = models.CharField(max_length=150)
    rep_repuesta_proy = models.CharField(max_length=20)
    rep_respuesta_cli = models.CharField(max_length=20)
    rep_consulta = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='rep_consulta')
    fecha_prev_rep = models.DateField()
    agrupacion = models.CharField(max_length=4,null=True,blank=True)
    id_realicionada = models.CharField(max_length=4,null=True,blank=True)
    ambito = models.CharField(max_length=1,choices=AMBITO,default=1)
    criticidad = models.CharField(max_length=1,choices=CRITICIDAD,default=2)
    fase_localizada = models.ForeignKey('DudasFaseLoc', models.DO_NOTHING, db_column='fase_localizada',default=1)
    realativa_a = models.ForeignKey('DudasRelalivaA', models.DO_NOTHING, db_column='realativa_a',default=1)
    doc_entrada_incompleta = models.CharField(max_length=1,choices=DOC_ENT_INC,default=1)
    subida_a_fenix = models.CharField(max_length=1, blank=True, null=True,default='0')

    class Meta:
        managed = False
        db_table = 'dudas'



class DudasFaseLoc(models.Model):
    iddudas_fase_loc = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'dudas_fase_loc'

    def __str__(self):
        cadena="{0}"
        return cadena.format(self.descripcion)

class DudasRelalivaA(models.Model):
    iddudas_relaliva_a = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'dudas_relaliva_a'

    def __str__(self):
        cadena="{0}"
        return cadena.format(self.descripcion)

 

class EquiDetalle(models.Model):
    idequi_detalle = models.AutoField(primary_key=True)
    idequipo = models.ForeignKey('Equipo', models.DO_NOTHING, db_column='idequipo')
    idcliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='idcliente')
    creador = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='creador')
    creado_el = models.DateField()
    valido_desde = models.DateField(blank=True, null=True)
    valido_hasta = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True, default='1')

    class Meta:
        managed = False
        db_table = 'equi_detalle'

 

class Equipo(models.Model):
    idequipo = models.AutoField(primary_key=True)
    dominio = models.ForeignKey(Dominio, models.DO_NOTHING, db_column='dominio')
    responsable = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='responsable')
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'equipo'

    def __str__(self):
        cadena="{0}"
        return cadena.format(self.codigo)


class EstDetalle(models.Model):
    id_est_det = models.AutoField(primary_key=True)
    requerimiento = models.ForeignKey('Requerimientos', models.DO_NOTHING, db_column='requerimiento')
    tipo = models.ForeignKey('PeticionTipo', models.DO_NOTHING, db_column='tipo')
    suptipo = models.ForeignKey('TaskFaseActividad', models.DO_NOTHING, db_column='suptipo')
    dificultad = models.ForeignKey('Zdificultad', models.DO_NOTHING, db_column='dificultad')
    peso = models.FloatField()
    esfuerzo = models.FloatField()
    peso = models.FloatField()
    creador = models.CharField(max_length=30, blank=True, null=True)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    ajus_cantidad = models.FloatField(blank=True, null=True)
    ajus_descripcion = models.CharField(max_length=100, blank=True, null=True)
    ajus_por = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='ajus_por', blank=True, null=True)
    ajus_fecha = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'est_detalle'


class EstimPeso(models.Model):
    tarea_tipo = models.ForeignKey('PeticionTipo', models.DO_NOTHING, db_column='tarea_tipo')
    tarea_subtipo = models.ForeignKey('TaskFaseActividad', models.DO_NOTHING, db_column='tarea_subtipo')
    dificultad = models.ForeignKey('Zdificultad', models.DO_NOTHING, db_column='dificultad')
    peso = models.FloatField()
    peso_hist = models.FloatField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    alta = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estim_peso'
        

class Gant(models.Model):
    idgant = models.AutoField(primary_key=True)
    idcliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='idcliente', blank=True, null=True)
    idauth = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='idauth', blank=True, null=True)
    idcol_edit = models.ForeignKey(AuthUser, models.DO_NOTHING,related_name='idcol_edit', db_column='idcol_edit', blank=True, null=True) # + 21.08
    anio = models.CharField(max_length=4, blank=True, null=True)
    mes = models.CharField(max_length=2, blank=True, null=True)
    sem = models.CharField(max_length=2, blank=True, null=True)
    dia = models.CharField(max_length=2, blank=True, null=True)
    idrequerimiento = models.ForeignKey('Requerimientos', models.DO_NOTHING, db_column='idrequerimiento',blank=True, null=True)
    llave = models.CharField(max_length=28)
    posicion = models.CharField(max_length=2, blank=True, null=True)
    fecha_modif = models.DateField()
    fecha_clave = models.DateField()
    imputacion = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gant'


class Hardcode(models.Model):
    app = models.CharField(max_length=5)
    asp = models.CharField(max_length=5)
    typcon = models.CharField(max_length=5)
    consum = models.CharField(max_length=5)
    item = models.CharField(max_length=10, blank=True, null=True)
    val01 = models.CharField(max_length=100)
    val02 = models.CharField(max_length=100, blank=True, null=True)
    val03 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hardcode'


class IncLocalizadaEn(models.Model):
    idinc_localizada_en = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'inc_localizada_en'

    def __str__(self):
        cadena="{0}"
        return cadena.format(self.descripcion)


class IncTipo(models.Model):
    idinc_tipo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'inc_tipo'
        
    def __str__(self):
        cadena="{0}"
        return cadena.format(self.descripcion)


class Incidencia(models.Model):
    CATG = (
        ('1', 'Funcional'),
        ('2', 'No funcional'),
    )
    CATG_INC = (
        ('1', 'INTERNA'),
        ('2', 'EXTERNA'),
    )
    EST_INC_CAR = (
        ('1', 'Pendiente'),
        ('2', 'No aplica'),
        ('3', 'Resuelto'),
        ('4', 'Siguiente Versión'),
    )
    CRIT = (
        ('1', 'Baja'),
        ('2', 'Media'),
        ('3', 'Alta'),
    )
    idincidencia = models.AutoField(primary_key=True)
    num_bug = models.CharField(max_length=15)
    requerimiento = models.ForeignKey('Requerimientos', models.DO_NOTHING, db_column='requerimiento')
    idetificador = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='idetificador')
    descripcion = models.CharField(max_length=150)
    categoria = models.CharField(max_length=1, choices=CATG,default='1')
    localizada_en = models.ForeignKey(IncLocalizadaEn, models.DO_NOTHING, db_column='localizada_en',default='1')
    tipo_incidencia = models.ForeignKey(IncTipo, models.DO_NOTHING, db_column='tipo_incidencia',default='1')
    criticidad = models.CharField(max_length=1, choices=CRIT,default='2')
    fecha_ident = models.DateField()
    categoria_inc = models.CharField(max_length=1, choices=CATG_INC, default='1')
    fecha_ini = models.DateField()
    fecha_fin = models.DateField()
    estado_inc_car = models.CharField(max_length=1, choices=EST_INC_CAR,default='3')
    esfuerzo = models.FloatField(blank=True, null=True)
    comentario_car = models.CharField(max_length=100, blank=True, null=True)
    subida_a_fenix = models.CharField(max_length=1, blank=True, null=True,default='0')
 
    class Meta:
        managed = False
        db_table = 'incidencia'



class LogDeModificaciones(models.Model):
    idlog_de_modificaciones = models.AutoField(primary_key=True)
    #usuario = models.IntegerField()# grcl4
    usuario = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='usuario')
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='cliente', blank=True, null=True)
    fecha = models.DateField()
    hora = models.TimeField()
    tipo_modificacion = models.CharField(max_length=1)
    tabla = models.CharField(max_length=25, blank=True, null=True)
    campo = models.CharField(max_length=25, blank=True, null=True)
    id_entidad = models.IntegerField()
    log = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_de_modificaciones'


class ModulosSap(models.Model):
    idmodulos_sap = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=7)
    modulo = models.CharField(max_length=45)
    zultima_modificacion = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True, default='1')

    class Meta:
        managed = False
        db_table = 'modulos_sap'

    def __str__(self):
        cadena="{0}"
        return cadena.format(self.codigo)


class Pais(models.Model):
    idpais = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=3)
    pais = models.CharField(max_length=25)
    codigo_tel = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pais'

    def __str__(self):
        cadena="{0}-{1}"
        return cadena.format(self.codigo ,self.pais)


class PeerReview(models.Model):
    RESULTADO = (
        ('1', 'OK'),
        ('2', 'KO'),
        ('3', 'N/A'),
    )
    idperer = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=35)
    requerimiento = models.ForeignKey('Requerimientos', models.DO_NOTHING, db_column='requerimiento', blank=True, null=True)
    revisor = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='revisor', blank=True, null=True)
    resultado = models.CharField(max_length=1,choices=RESULTADO,default='1')
    version = models.IntegerField()
    nota = models.CharField(max_length=500, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'peer_review'


class Peticion(models.Model):
    CONTENEDORA = (
        ('On', 'Contenedora'),
        (' ', 'No contenedora'),
    )
    idpeticion = models.AutoField(primary_key=True)
    id_pet_fenix = models.CharField(max_length=20)
    id_ot_fenix = models.CharField(max_length=20)

    pet_ruta = models.CharField(max_length=200, blank=True, null=True)
    ot_ruta = models.CharField(max_length=200, blank=True, null=True)
    #contenedora = models.CharField(max_length=2, choices=CONTENEDORA, default=' ')
    contenedora = models.CharField(max_length=2, blank=True, null=True)

    nombre = models.CharField(max_length=45)
    tipo = models.ForeignKey('PeticionTipo', models.DO_NOTHING, db_column='tipo',default=1)
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='cliente')
    gestion = models.ForeignKey('PeticionGestion', models.DO_NOTHING, db_column='gestion',default=1)
    estado = models.ForeignKey('PeticionEstado', models.DO_NOTHING, db_column='estado',default=1)
    input_final = models.ForeignKey('PeticionInputFinal', models.DO_NOTHING, db_column='input_final',default=1)
    fecha_solicitud = models.DateField()
    fecha_fin_acuerdo = models.DateField()
    fecha_real_entrega = models.DateField(blank=True, null=True)
    horas_acuerdo = models.FloatField(blank=True, null=True)
    horas_estimadas = models.FloatField(blank=True, null=True)
    comentario = models.CharField(max_length=300, blank=True, null=True)
    creador = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='creador', blank=True, null=True)
    zultima_modificacion = models.DateField(blank=True, null=True)
    zestado = models.CharField(max_length=1, blank=True, null=True, default='1')
    color = models.CharField(max_length=10, blank=True, null=True,default='#CCF0D5')

    class Meta:
        managed = False
        db_table = 'peticion'

    def __str__(self):
        cadena="{0}-{1}"
        return cadena.format(self.id_pet_fenix ,self.nombre)


class PeticionEstado(models.Model):
    idestado_peticion = models.AutoField(primary_key=True)
    variable = models.CharField(max_length=15)
    codigo = models.CharField(max_length=6)
    descripcion = models.CharField(max_length=45)
    descripcion_fenix = models.CharField(max_length=45, blank=True, null=True)
    col_str = models.CharField(max_length=10, blank=True, null=True,default='#CCF0D5')
    col_lig = models.CharField(max_length=10, blank=True, null=True,default='#CCF0D5')

    class Meta:
        managed = False
        db_table = 'peticion_estado'

    def __str__(self):
        cadena="{0}"
        return cadena.format(self.descripcion_fenix)


class PeticionGestion(models.Model):
    idgestion_peticion = models.AutoField(primary_key=True)
    gestion = models.CharField(max_length=3)
    descripcion = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'peticion_gestion'

    def __str__(self):
        cadena="{0}"
        return cadena.format(self.gestion)


class PeticionInputFinal(models.Model):
    idpet_inp_fnl = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=1)
    input_final = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=45,blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'peticion_input_final'

    def __str__(self):
        cadena="{0}"
        return cadena.format(self.input_final)


class PeticionTipo(models.Model):
    idtipo_peticion = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=15)
    ultima_modificacion = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'peticion_tipo'
        
    def __str__(self):
        cadena="{0}"
        return cadena.format(self.tipo)


class ReqCalidadInput(models.Model): 
    idreq_calidad_input = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=1)
    calidad = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'req_calidad_input'
        
    def __str__(self):
        cadena="{0}"
        return cadena.format(self.calidad)


class ReqContacto(models.Model):
    idpeticion_contacto = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=45)
    apellidos = models.CharField(max_length=45, blank=True, null=True)
    celular = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'req_contacto'

    def __str__(self):
        cadena="{0} {1}"
        return cadena.format(self.nombres,self.apellidos)



class ReqCriticidad(models.Model):
    criticidad = models.CharField(max_length=15)
    crit = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'req_criticidad'
    
    def __str__(self):
        cadena="{0}"
        return cadena.format(self.criticidad)



class ReqEstado(models.Model):
    idreq_estado = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'req_estado'

    def __str__(self):
        cadena="{0}"
        return cadena.format(self.estado)


class ReqEstimAltoNivel(models.Model):
    idreq_estim_alto_nivel = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=1)
    nivel = models.CharField(max_length=15)
    descripcion = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'req_estim_alto_nivel'

    def __str__(self):
        cadena="{0}"
        return cadena.format(self.descripcion)


class ReqInputFinal(models.Model):#grcl4
    idreq_input_final = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=1)
    input_final = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'req_input_final'

    def __str__(self):
        cadena="{0}"
        return cadena.format(self.input_final)


class ReqPrioridad(models.Model):
    idreq_prioridad = models.AutoField(primary_key=True)
    prioridad = models.CharField(max_length=15)
    descripcion = models.CharField(max_length=45, blank=True, null=True)
    color1 = models.CharField(max_length=10, blank=True, null=True)
    color2 = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'req_prioridad'

    def __str__(self):
        cadena="{0}"
        return cadena.format(self.descripcion)


class Requerimientos(models.Model):
    idrequerimiento = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=21)
    requerimien_asociado = models.CharField(max_length=11,blank=True, null=True)
    modulo = models.ForeignKey(ModulosSap, models.DO_NOTHING, db_column='modulo',default=13)
    codigo_cliente = models.CharField(max_length=20, blank=True, null=True)
    breve_descripcion = models.CharField(max_length=200, blank=True, null=True)
    descripcion = models.CharField(max_length=1500, blank=True, null=True)  # line add 02.04.2021
    peticion = models.ForeignKey(Peticion, models.DO_NOTHING, db_column='peticion')
    responsable = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='responsable')
    contacto = models.CharField(max_length=75, blank=True, null=True)
    fecha_estimacion = models.DateField()
    fecha_inicio_planificada = models.DateField()
    fehca_inicio_real = models.DateField(null=True,blank=True)
    fecha_fin_planificada = models.DateField()
    fecha_entrega_real = models.DateField(null=True,blank=True)
    calidad_input = models.ForeignKey(ReqCalidadInput, models.DO_NOTHING, db_column='calidad_input', blank=True, null=True,default=3)
    input_final = models.ForeignKey(ReqInputFinal, models.DO_NOTHING, db_column='input_final',default=1)
    estimacion_alto_nivel = models.ForeignKey(ReqEstimAltoNivel, models.DO_NOTHING, db_column='estimacion_alto_nivel', blank=True, null=True)
    prioridad = models.ForeignKey(ReqPrioridad, models.DO_NOTHING, db_column='prioridad',blank=True,default=3)
    criticidad = models.ForeignKey(ReqCriticidad, models.DO_NOTHING, db_column='criticidad',blank=True,default=1)
    estimacion_acuerdo = models.FloatField()
    estimacion_aprobada = models.FloatField()
    estimacion_fenix_h = models.FloatField(blank=True, null=True)
    horas_adicionales = models.FloatField(blank=True, null=True)
    estado = models.ForeignKey('PeticionEstado', models.DO_NOTHING, db_column='estado', blank=True, null=True, default=1)
    horas_acuerddo_mes = models.FloatField(blank=True, null=True)
    seguimiento_diario = models.TextField(blank=True, null=True)
    ordent = models.TextField(blank=True, null=True)
    programas = models.TextField(blank=True, null=True)
    zultima_modificacion = models.DateField(blank=True, null=True)
    zestado = models.CharField(max_length=1, blank=True, null=True,default='1')
    estimacion_aprobada = models.SmallIntegerField(blank=True, null=True,default=0)
    class Meta:
        managed = False
        db_table = 'requerimientos' 

    def __str__(self):
        cadena="{0} : {1} @{2}"
        return cadena.format(self.peticion.cliente.codigo,self.codigo,self.breve_descripcion)


class Riesgo(models.Model):
    TIPO = (
        ('1', 'Riesgo'),
        ('2', 'Problema'),
    )
    ESTADO = (
        ('1', 'En Progreso'),
        ('2', 'Materializado'),
        ('3', 'Cancelado'),
        ('4', 'Cerrado'),
        ('5', 'Resuelto'),
    )
    RESOLUCION = (
        ('1', 'Proceso'),
    )
    idriesgo = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=8)
    fecha_indentificacion = models.DateField()
    requerimiento = models.ForeignKey(Requerimientos, models.DO_NOTHING, db_column='requerimiento')
    tipo = models.CharField(max_length=1,choices=TIPO,default='1')
    estado = models.CharField(max_length=1,choices=ESTADO,default='4')
    resolucion = models.CharField(max_length=1, blank=True, null=True,choices=RESOLUCION,default='1')
    responsable = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='responsable')
    categoria = models.ForeignKey('RiesgoCategoria', models.DO_NOTHING, db_column='categoria',default='1')
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    acciones = models.CharField(max_length=75, blank=True, null=True)
    zultima_modificacion = models.DateField(blank=True, null=True)
    zestado = models.CharField(max_length=1, blank=True, null=True)
    seguimiento = models.CharField(max_length=300, blank=True, null=True)
    subida_a_fenix = models.CharField(max_length=1, blank=True, null=True,default='0')

    class Meta:
        managed = False
        db_table = 'riesgo'


class RiesgoCategoria(models.Model):
    idriesgo_categoria = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=55)

    class Meta:
        managed = False
        db_table = 'riesgo_categoria'
        
    def __str__(self):
        cadena="{0}"
        return cadena.format(self.categoria)


class Task(models.Model):
    idtask = models.AutoField(primary_key=True)
    id_interno = models.CharField(max_length=20,blank=True)
    requerimiento = models.ForeignKey(Requerimientos, models.DO_NOTHING, db_column='requerimiento')
    responsable = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='responsable')
    subtarea = models.CharField(max_length=150)
    fase_actividad = models.ForeignKey('TaskFaseActividad', models.DO_NOTHING, db_column='fase_actividad',default=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    esfuerzo_total_estandar = models.FloatField()
    esfuerzo_ejecutado = models.FloatField(blank=True, null=True)
    estado = models.ForeignKey('TaskEstado', models.DO_NOTHING, db_column='estado', blank=True ,default='1')
    subida_a_fenix = models.CharField(max_length=1, blank=True, null=True)
    zultima_modificacion = models.DateField(blank=True, null=True)
    zestado = models.CharField(max_length=1, blank=True, null=True,default='1')

    class Meta:
        managed = False
        db_table = 'task'
        
    def __str__(self):
        cadena="{0} : {1} - {2}."
        return cadena.format(self.requerimiento.peticion.cliente.codigo,self.requerimiento.codigo,self.subtarea)
        

class TaskEstado(models.Model):
    idtask_estado = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=3)
    descripcion = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task_estado'
        
    def __str__(self):
        cadena="{0}"
        return cadena.format(self.estado)


class TaskFaseActividad(models.Model):
    idtask_fase_actividad = models.AutoField(primary_key=True)
    id_interno = models.CharField(max_length=6, blank=True, null=True)
    tipo = models.CharField(max_length=6)
    codigo = models.CharField(max_length=3)
    fase_actividad = models.CharField(max_length=25)
    esfuerzo = models.FloatField()
    parte_esfuerzo_sin_gestion = models.FloatField()
    parte_esfuerzo = models.FloatField()
    zultima_modificacion = models.DateField(blank=True, null=True)
    zestado = models.CharField(max_length=1, blank=True, null=True,default='1')

    class Meta:
        managed = False
        db_table = 'task_fase_actividad'

    def __str__(self):
        cadena="{0}"
        return cadena.format(self.fase_actividad)

 
class Zdificultad(models.Model):
    dificultad = models.CharField(max_length=15)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null=True)
    alta = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zdificultad'

    def __str__(self):
        cadena="{0}"
        return cadena.format(self.dificultad)


