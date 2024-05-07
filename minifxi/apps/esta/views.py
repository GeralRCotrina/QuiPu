
from django.http import HttpResponse
from django.shortcuts     import render
from django.views.generic import View
from apps.gestion.models import *


import calendar
import datetime
import numpy as np
from django.db.models import Q
from django.db import connection, transaction
from apps.gestion.gv_view import *







#  ===================== D A I L Y ================== #



#  - - - -  Actualiza los campos de la vista Daily - - -  - #
class DaiUpd(View):

	def get(self,request,*args,**kwargs):
		
		#  Get request
		json = '{'

		idr = self.request.GET.get('idr')
		val = self.request.GET.get('val')
		col = self.request.GET.get('col')
		
			
		# Logic
		#print("  >> "+str(idr)+" "+str(col)+" "+str(val)+" ")
		if Requerimientos.objects.filter(pk=idr).exists():
			req = Requerimientos.objects.filter(pk=idr).first()

			# Validar asignación actual
			if not ValidaCliente(request.user.pk,req.peticion.cliente.pk):
				json += '"0":"NUsr"'  # Usted No está asignado a ese cliente.
			else:

				#  Actualiza el estado
				if col == 'est':
					req.estado = PeticionEstado.objects.get(pk=val)

				#  Actualiza la prioridad
				elif col == 'prio':
					req.prioridad = ReqPrioridad.objects.get(pk=val)

				#  Actualiza la FECHA DE INICIO PLANIFICADA
				elif col == 'f_ini':
					req.fecha_inicio_planificada = val

				#  Actualiza EL CONTACTO FUNCIONAL
				elif col == 'cont':
					req.contacto = val

				#  Actualiza la CALIDAD DEL INPUT
				elif col == 'cld':
					req.calidad_input = ReqCalidadInput.objects.get(pk=val)

				#  Actualiza la BITÁCORA
				elif col == 'bit':
					req.seguimiento_diario = val

				#  Actualiza EL RESPONSABLE DEL REQUERIMIENTO
				elif col == 'resp':
					req.responsable = AuthUser.objects.get(pk=val)


				# Save Changes and rpta
				req.save()
				json += '"0":"ok"'

		else:
			json += '"0":"nrq"'

		json += '}'
		#print("  >> json : "+json+" ")
		return HttpResponse(json)


"""
ok  = 'Proceso finalizado correctamente'
nrq = 'No existe requerimiento'
"""





#  - - - - Carga el Daily - - -  - #
class Daily(View):
	
	def get(self,request,*args,**kwargs):
		
		# Lista de clientes para el matchcode

		equ = self.request.GET.get('equ')
		fecha_desde = self.request.GET.get('fecha_desde')
		fecha_hasta = self.request.GET.get('fecha_hasta')


		# Get TIPO ESTIM
		lst_pes = PeticionEstado.objects.all()
		for pes in lst_pes:
			pass

		# Get PRIORIDAD
		lst_prio = ReqPrioridad.objects.all()
		for prio in lst_prio:
			pass

		# Get CALIDAD DEL INPUT
		lst_cld = ReqCalidadInput.objects.all()
		for cld in lst_cld:
			pass


		# Get USUARIOD del equipo
		lst_usr = AuthUser.objects.filter()
		for usr in lst_usr:
			pass


		# Para el matcode de clientes
		lst_equs = Equipo.objects.all()
		for equs in lst_equs:
			pass			


		# Get ...
		obj_fa = TaskFaseActividad.objects.all()
		cad = ''
		for fa in obj_fa:
			cad += '-'+str(fa.pk)
		#print("  >> "+cad)


		userpk = self.request.user.pk

		# Obtenemos el equipo asignado
		#print(" >> equ : ["+str(equ)+"]")
		if equ == None or equ == '' or equ == '0':
			if AuthCliente.objects.filter(idauth=userpk).exists():
				acl = AuthCliente.objects.filter(idauth=userpk).first()
				equi = acl.idcliente.equipo
			else: 
				equi = Equipo.objects.get(idequipo=1) # Toma valor inicial será uno
		else:
			equi = Equipo.objects.get(idequipo=equ)


		#print(" >> Equi : "+str(equi))


		# Validamos fechas
		if fecha_desde == None:
			fh1 = datetime.datetime.now()
			fecha_desde = "'"+str(fh1.year)+"-"+str(fh1.month)+"-01'"
		if fecha_hasta == None:
			fh = datetime.datetime.now()
			cant_dias = calendar.monthrange(fh.year,fh.month)
			fecha_hasta = "'"+str(fh.year)+"-"+str(fh.month)+"-"+str(cant_dias[1])+"'"


		# Obtenemos los colaboradores con asignación a ese equipo
		lst_usrs = []	
		cursor = connection.cursor()
		cursor.execute("CALL sp_002_usr_x_equi ("+str(equi.pk)+","+fecha_desde+","+fecha_hasta+")")
		resultado = cursor.fetchall()
		cad = ''
		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			lst_usrs.append(dic)
			cad += '-'+str(dic['id']) 
			#print(" ------>"+str(dic))
		cursor.close()

		#print(" >> equi : "+str(equi)+"   pK "+str(equi.pk)+" - "+str(fecha_desde)+" - "+str(fecha_hasta) )
		object_list = []		
		cursor = connection.cursor()
		cursor.execute("CALL sp_dail_x_fecha_2 ("+str(equi.pk)+","+str(fecha_desde)+","+str(fecha_hasta)+")")
		cursor.execute("CALL sp_dail_x_fecha_2 (1,'2020-01-01','2020-01-01')")	# ---> CONSULTA FANTASMA NECESARIA
		resultado = cursor.fetchall()

		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)
			#print(" >> "+str(dic['etc']))
		cursor.close()

		# Bluid mensaje
		msj ="Daily desde "+fecha_desde+" hasta "+fecha_hasta+" del equipo "+str(equi.nombre)+"."

		# Build response
		dicc = { 
			'object_list':object_list,		# Contiene todos los requerimietos ( toda la consulta a la ddbb )
			'lst_equs': lst_equs,			# Los equipos a consultar
			'lst_pes': lst_pes,				# Los estado del requerimeitno/petición
			'lst_prio': lst_prio,			# Las prioridades requerimeitno 
			'lst_cld': lst_cld,				# Listado de las diferentes calidades de input 
			'lst_usrs': lst_usrs,			# Colaboradores con asignación a ese equipo. 
			'obj_fa': obj_fa,
			'msj': msj
		}

		return render(request,'dail/daily.html',dicc)



		










"""  ================================================ E S T A T U S --------------------- """
# Crea el estratus diario
class EstCrear(View): 

	def get(self,request,*args,**kwargs):

		#print("  >> sta.")
		# Lista de clientes para el matchcode
		cli_lst = Cliente.objects.all()	
		for x in cli_lst:
			pass


		# Optenemos los estado para luego excluirlos en el front
		lst_sta = PeticionEstado.objects.all()
		for p in lst_sta:
			pass


		# Traer la lista de lso estatus excluidos en el filtro  #grcl4
		lst_excl = []
		lst_sta_excl = Hardcode.objects.filter( Q(app='gest') & Q(asp='esta') & Q(typcon='clie') & Q(item='excl_sta') & Q(item='excl_sta') )
		for q in lst_sta_excl:
			lst_excl.append(q.val02)



		# Lista de clientes para el matchcode
		cli_id = self.request.GET.get('cli_id')
		fec_des = self.request.GET.get('fec_des')
		fchs = ""
		fch = ""
		clie = None


		#	Si no envían cliente, lo obtenemos
		if cli_id == None:
			cli_id = MiCliente(self.request.user.pk)
			if cli_id == '0':
				cli_id0 = Cliente.objects.filter(idcliente__gte=1).first()
				cli_id = cli_id0.pk
		
		# Cuando se consulta por cliente, es necesario buscarlo
		if clie == None:
			clie = Cliente.objects.get(pk=cli_id)


		# Traer la lista de los estatus excluidos en el filtro  #grcl4
		lst_excl = []
		lst_sta_excl = Hardcode.objects.filter( Q(app='gest') & Q(asp='esta') & Q(typcon='clie') & Q(consum=str(cli_id)) & Q(item='excl_sta') )
		for q in lst_sta_excl:
			lst_excl.append(q.val02)

		#print('   >>---|--->'+str(fec_des))
		
		# Tomamos la fecha enviada o la construímos
		if fec_des != '' and fec_des != None:
			fchs = fec_des
			fch = datetime.datetime.strptime(fchs, '%Y-%m-%d')
		else:
			fch = datetime.datetime.now() 	
			fchs = ""+str(fch.year)+"-"+str(fch.month)+"-"+str(fch.day)+""


		# Obtenemos el resumen
		hoy = ""
		if fch.day < 10:
			hoy = "0"+str(fch.day)+"."
		else:
			hoy = ""+str(fch.day)+"."
		if fch.month < 10:
			hoy = hoy + "0"+str(fch.month)+"."
		else:
			hoy = hoy + str(fch.month)+"."



		ArrF = StartEndWeek(fchs)
		semn = "desde el "+str(ArrF[1].day)+"/"+str(ArrF[1].month)
		semn = semn + " hasta "+str(ArrF[2].day)+"/"+str(ArrF[2].month)


		pet_lst = Peticion.objects.filter(cliente = clie).exclude( Q(estado=2) | Q(estado=3) | Q(estado=8) )
		for p in pet_lst:
			pass

		req_lst_hoy1 = Requerimientos.objects.filter(Q(peticion__cliente=clie) & Q(seguimiento_diario__icontains=hoy))	
		req_lst_hoy	= []
		for q in req_lst_hoy1:
			#print("  >> "+str(q.codigo)+"  : "+str(q.peticion.nombre[0:3]))
			req_lst_hoy.append({'pet':q.peticion.pk,'codigo':q.codigo,'bitacora':q.seguimiento_diario})
			#pass


		pet_lst1 = []
		req_lst_tot = []

		for y in pet_lst:
			#pet_lst1.append({'nombre':y.nombre,'pk':y.pk})
			pet_lst1.append({'nombre':y.nombre[0:3],'pk':y.pk})





		from django.db import connection, transaction
		object_list = []
		cursor = connection.cursor()	
		cursor.execute("CALL sp_status01("+str(cli_id)+")")
		resultado = cursor.fetchall()
		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			if dic['estado'] not in lst_excl:
				#print("  >-----> "+str(dic['estado']))
				object_list.append(dic)

		cursor.close()


		dicc = {  
			"req_lst_tot" : object_list,
			"pet_lst" : pet_lst1,
			"req_lst_hoy" : req_lst_hoy,
			'cli_lst': cli_lst,
			'fecha': str(fch.day)+"."+str(fch.month)+"."+str(fch.year),
			'hora': "05:00 pm",
			'semana': semn,
			"cliente": clie,
			'lst_sta' : lst_sta,
			'lst_sta_excl' : lst_sta_excl,
			'idc' : cli_id,
			'msj': " "
		}
		return render(request,'esta/status.html',dicc)







#	Obtenemos los días laborables de esa semana y mes
#	Devuelve [ fecha dada | priper día lab | último día lab. | cant ]
def StartEndWeek(fe_sem):
	ArrF = ['','','','']

	from datetime import datetime, timedelta
	fecha = datetime.strptime(fe_sem, '%Y-%m-%d')
	start = fecha - timedelta(days=fecha.weekday())
	end = start + timedelta(days=4) 

	if start.month != fecha.month:
		n_fecha = str(fecha.year)+'-'+str(fecha.month)+'-01'
		start = datetime.strptime(n_fecha, '%Y-%m-%d')
	elif end.month != fecha.month:
		fech_s = ""+str(end.year)+"-"+str(end.month)+"-01"
		fech_d = datetime.strptime(fech_s, '%Y-%m-%d')
		end = fech_d - timedelta(days = 1)

	ArrF[0] =  datetime.strptime(fe_sem, '%Y-%m-%d')
	ArrF[1] =  start
	ArrF[2] =  end
	ArrF[3] =  1 + np.busday_count(start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))

	return ArrF





