# ----------------------------------------------------------------------------------------- #
#                                 RECURSOS GLOBALES                                         #
# ----------------------------------------------------------------------------------------- #
import datetime
from datetime import timedelta
from apps.gestion.models import AuthCliente, AuthUser, Equipo, LogDeModificaciones, EquiDetalle
from django.db.models import Q
import numpy as np
from django.shortcuts import render




# Validar si el usuario logueado está asignado al Cliente.
def ValidaCliente(usr_id,cli_id):
	# Traer INICIO y FIN del MES
	(dia_i,dia_f) = ObtUltDiaDelMes(str(datetime.datetime.now().year),str(datetime.datetime.now().month))

	# Validar
	if AuthCliente.objects.filter( 
		Q(idauth=int(usr_id)) & Q(idcliente=int(cli_id)) & ( 
			( Q(fecha_baja__gte=dia_i) & Q(fecha_baja__lte=dia_f) ) 
			| ( Q(fecha_alta__gte=dia_i) & Q(fecha_alta__lte=dia_f) ) 
			| ( Q(fecha_alta__lte=dia_i) & Q(fecha_baja__gte=dia_i) ) 
			)
		).exists():
		rpta = True
	else:
		rpta = False	
	return rpta




# Obtenemos el cliente para el filtro personalizado
# Solo si la consulta no viene desde el listado
# y si el usuario está asignado a algún cliente.
def	MiCliente(userpk):
	hoy = datetime.datetime.now()
	clie = None
	if AuthCliente.objects.filter( Q(idauth = userpk) & Q(fecha_alta__lte=hoy) & Q(fecha_baja__gte=hoy) & Q(prioridad="on") ).exists():
		asig01 = AuthCliente.objects.filter( Q(idauth = userpk) & Q(fecha_alta__lte=hoy) & Q(fecha_baja__gte=hoy) & Q(prioridad="on") ).last()
		clie = asig01.idcliente.pk
	else:
		if AuthCliente.objects.filter( Q(idauth = userpk) & Q(fecha_alta__lte=hoy) & Q(fecha_baja__gte=hoy)).exists():
			asig01 = AuthCliente.objects.filter( Q(idauth = userpk) & Q(fecha_alta__lte=hoy) & Q(fecha_baja__gte=hoy)).last()
			clie = asig01.idcliente.pk
		clie = '0'
	return clie

# Obtenemos el equipo asignado
def	MiEquipo(clie,usr):
	equ = '0'
	if equ == None or equ == '' or equ == '0':
		if AuthCliente.objects.filter(idauth=usr, idcliente=clie, prioridad='on').exists():
			acl = AuthCliente.objects.filter(idauth=usr, idcliente=clie, prioridad='on').last()
			equi_det = EquiDetalle.objects.filter(idcliente=acl.idcliente).last()# Tenemos el id del cliente favorito jajaja
			equi = Equipo.objects.get(idequipo=equi_det.idequipo.pk)
		else: 
			# Validamos si tine asignación sin Cliente Prioridad
			if AuthCliente.objects.filter(idauth=usr, idcliente=clie).exists():
				acl = AuthCliente.objects.filter(idauth=usr, idcliente=clie).last()
				equi_det = EquiDetalle.objects.filter(idcliente=acl.idcliente).last()# Tenemos el id del cliente favorito jajaja
				equi = Equipo.objects.get(idequipo=equi_det.idequipo.pk)
			else:
				equi = Equipo.objects.get(idequipo=1) # Toma valor inicial será uno
	else:
		equi = Equipo.objects.get(idequipo=equ)
	return equi




#	Obtenemos los días laborables de esa semana y mes
#	Devuelve [ fecha dada | primer día lab | último día lab. | cant ]
def DiasLabPorSem(ArrID):
	ArrF = ['','','','']
	fe_sem 	= "20"+ArrID[3]+'-'+ArrID[4]+'-'+ArrID[6]

	fecha = datetime.datetime.strptime(fe_sem, '%Y-%m-%d')
	start = fecha - timedelta(days=fecha.weekday())
	end = start + timedelta(days=4) 

	if start.month != fecha.month:
		n_fecha = str(fecha.year)+'-'+str(fecha.month)+'-01'
		start = datetime.datetime.strptime(n_fecha, '%Y-%m-%d')
	elif end.month != fecha.month:
		fech_s = ""+str(end.year)+"-"+str(end.month)+"-01"
		fech_d = datetime.datetime.strptime(fech_s, '%Y-%m-%d')
		end = fech_d - timedelta(days = 1)

	ArrF[0] =  datetime.datetime.strptime(fe_sem, '%Y-%m-%d')
	ArrF[1] =  start
	ArrF[2] =  end
	ArrF[3] =  1 + np.busday_count(start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
	return ArrF





# Obtener asignaciones del cliente en las fechas indicadas
# MEJOR USE LA SGTE FUNCIÓN
def ObtLstAsg(cli0,dia_i,dia_f):
	if dia_i == '':
		(dia_i,dia_f) = ObtUltDiaDelMes(str(datetime.datetime.now().year),str(datetime.datetime.now().month))
	lst_asg = []
	lst_asg  = AuthCliente.objects.filter( Q(idcliente=cli0) & Q(fecha_baja__gte=dia_i) & Q(fecha_baja__lte=dia_f) | Q(idcliente=cli0) & Q(fecha_alta__gte=dia_i) & Q(fecha_alta__lte=dia_f) | Q(idcliente=cli0) & Q(fecha_alta__lte=dia_i) & Q(fecha_baja__gte=dia_i) )
	return lst_asg




# Obtener colaboradores asignados del cliente en las fechas indicadas
def ObtLstCol(cli0,dia_i,dia_f):
	if dia_i == '':
		(dia_i,dia_f) = ObtUltDiaDelMes(str(datetime.datetime.now().year),str(datetime.datetime.now().month))
	lst_col = []
	lst_col  = AuthUser.objects.filter( Q(authcliente__idcliente=cli0) & Q(authcliente__fecha_baja__gte=dia_i) & Q(authcliente__fecha_baja__lte=dia_f) | Q(authcliente__idcliente=cli0) & Q(authcliente__fecha_alta__gte=dia_i) & Q(authcliente__fecha_alta__lte=dia_f) | Q(authcliente__idcliente=cli0) & Q(authcliente__fecha_alta__lte=dia_i) & Q(authcliente__fecha_baja__gte=dia_i) )
	return lst_col



#  Validamos si el string contiene una fecha real
def is_date(fec_s):
    try: 
        datetime.datetime.strptime(fec_s,'%Y-%m-%d')
        return True
    except ValueError:
        return False




# Calculamos el primer y último día del mes
def ObtUltDiaDelMes(anio,mes):
	dia_p = 32
	dia_i = ""+anio+'-'+mes+'-01'
	while dia_p > 5:
		dia_p = dia_p - 1
		dia_f = ""+anio+'-'+mes+'-'+str(dia_p)
		if is_date(dia_f):break
	return (dia_i,dia_f)



# ------SET LOG-------# 
def LogDeAccion(usu, clie, tab, camp, tm, pk_ent, log):
	#print("  >> log > tab:"+tab+"  camp:"+camp+"  tm:"+str(tm)+"  usu:"+str(usu))
	hora = datetime.datetime.now()
	fecha=datetime.datetime(year=hora.year,month=hora.month,day=hora.day)
	nlog = LogDeModificaciones(usuario = AuthUser.objects.get(pk=int(usu)), cliente = clie, fecha=fecha, hora=hora,
		tipo_modificacion = str(tm) , tabla = tab , campo = camp , id_entidad = pk_ent, log=log)
	nlog.save()
"""
TM (Tipo de modificación) Create:0		Read:1		Update:2		Delete:3
"""


def LogDeAccion1(request):
	LogDeAccion(184443,'peticion', 'estado',1, '2', 1, 'Log add++')
	return render(request,'inicio.html')