from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
#from django.urls import reverse_lazy
from django.views.generic import View
from apps.gestion.models import *
from apps.gestion.gv_view import *

import datetime
#import calendar
#from django.contrib import messages#
from django.db.models import Q

 
 

# ==============   G A N T ================= #

#	Pantalla principal.
def GantIni(request):
	object_list = Cliente.objects.all()
	dicc = {
		"object_list":object_list
	}
	return render(request,'gant/gnt.html',dicc)





#     ======================== CREAR NUEVO GANT ( PLANIFICAR ) ===================     #
"""
	Al crear nuevo gant (planificar algo) llega del front esto  'ID_CLI_COL_AA_MM_SEM_DIA_POS'  
	que son las claves de:
		id  : ( idr o idi ) Si se condultó desde el requerimiento o desde la imputación
		cli : cliente
		col : colaborador al que se le hace la planificación
		aa  : año tipo AA 
		mm  : número de mes
		sem : número de semana
		dia : día calendario
		pos : el número de la repetición en la que se registró el nuevo gant

	" Los resumenes guardan claves en la colunma día 
	( en lugar de llegan el número del DIA, llegan 2 letras), siendo :
		RS : Resumen semanal
		IN : Incurrido semanal
		HA : Horas acuerdo semanal
		DI : Disponibilidad semanal
		RD : Resumen diario
	y por último en la POSICION indica los resumenes diarios:
		ZA : Horas acuerdo diario.
		ZI : Incurrido diario.
		ZD : Disponibilidad.
		ZJ : Ajuste para incurrido diario.
"""

#  	Validación para insertar Gant  ======================================================================
class Gnt_c1(View):

	def get(self,request,*args,**kwargs):
		rpta = "Inv"
		ide = self.request.GET.get('ide')
		val_1 = self.request.GET.get('val_1') # Código de req
		val_2 = self.request.GET.get('val_2') # Imputación
		#mes = self.request.GET.get('mes')
		#anio = self.request.GET.get('anio')

		# ide = idr_CLI_COL_AA_MM_SEM_DIA_POS   -> 	Así llega
		rpta = GntValid(self.request,ide,val_1)
		if rpta == 'Ok':
			rpta = InsertarGant(ide,val_1,val_2,self.request.user.pk)
		#print("  >> rpta : "+str(rpta))
		return HttpResponse(rpta)
"""
"NAsi" # No está asignado a ese cliente.
"NCli" # No existe el cliente.
"NAut" # No existe el AuthUser.
"NReq" # No existe el req.
"NRaC" # Req no pertenece al cliente.
"Much" # Mas de un Req. con ese código.
"""


# Validaciones para modificar Gant
#       idr_CLI_COL_AA_MM_SEM_DIA_POS   -> 	Así llega  
# ArrID[ 0   1   2  3  4   5   6   7 ]
#
def	GntValid(request,ide,req):
	
	ArrID = ide.split('_') 
	cli0 = 1
	# 1.- Valicar CLIENTE
	if not Cliente.objects.filter(pk=int(ArrID[1])).exists():
		return 'NCli' # No existe el cliente.
	else: 
		cli0 = Cliente.objects.get(pk=int(ArrID[1]))

	## 2.- Validar COLABORADOR
	#if not AuthCliente.objects.filter(Q(idauth=request.user.pk) & Q(idcliente=cli0) ).exists():
	#	return 'NUsr' # Usted No está asignado a ese cliente.
	#if not AuthCliente.objects.filter( Q(idauth=int(ArrID[2])) & Q(idcliente=cli0) ).exists():
	#	return 'NAsi' # Colaborador No está asignado a ese cliente.
	
	# Validar asignación actual
	if not ValidaCliente(request.user.pk,cli0.pk):
		return 'NUsr' # Usted No está asignado a ese cliente.

	
	# 3.- Validar REQUERIMIENTO (Para otras validaciones no es necesario)
	if	req != 'Ok':
		lst_gnt =  Requerimientos.objects.filter(codigo=req)
		if lst_gnt.count() == 0 : 
			return 'NReq' # No existe el req.
		elif lst_gnt.count() > 1 : 
			return 'Much' # Mas de un Req. con ese código.
		elif lst_gnt.count() == 1 : 
			req2 = lst_gnt.first()
			if not cli0.pk == req2.peticion.cliente.pk:	# ¿Req pertenece al cliente?
				return "NRaC" # Req no pertenece al cliente.

	return 'Ok'






#	Guarda regisro de Gant
#def Insertar Gant(ArrID,ide,cli0,col0,req,val_1,val_2,us_edi):
def InsertarGant(ide,val_1,val_2,us_edi):
	rpta2 = 'Ok'
	n_gnt = ""
	# idr_CLI_COL_AA_MM_SEM_DIA_POS   -> 	Así llega
	if Gant.objects.filter(llave=ide[4:len(ide)]).exists():
		n_gnt=Gant.objects.get(llave=ide[4:len(ide)])
		# Validamos si la imputación ha cambiado
		if n_gnt.imputacion !=  float(val_2):
			rpta2='ACT' #	Actualizó, ya existía.
		else:
			rpta2='NAC' #	No Actualizó, no hay diferencia.
	else:
		n_gnt = Gant()
		rpta2='REG'	#	Registró nuevo Gant.
	
	ArrID = ide.split('_') 
	req = Requerimientos.objects.get(codigo=val_1)
	cli0 = Cliente.objects.get(pk=int(ArrID[1]))
	col0 = AuthUser.objects.get(pk=int(ArrID[2]))

	#print(" >> rp: "+rpta2+"  ||   a:"+str(n_gnt.imputacion)+"    b:"+str(val_2))
	if rpta2 != 'NAC':
		n_gnt.idcliente = cli0
		n_gnt.llave = ide[4:len(ide)]
		n_gnt.idauth = col0
		n_gnt.idcol_edit = AuthUser.objects.get(pk=us_edi)
		n_gnt.anio 	= ArrID[3]
		n_gnt.mes 	= ArrID[4]
		n_gnt.sem 	= ArrID[5]
		n_gnt.dia 	= ArrID[6]
		n_gnt.idrequerimiento = req
		n_gnt.posicion    = ArrID[7]
		n_gnt.fecha_modif = datetime.datetime.now()
		n_gnt.fecha_clave = '20'+ArrID[3]+"-"+ArrID[4]+"-"+ArrID[6]
		n_gnt.imputacion  =  float(val_2)
		n_gnt.save()

		# Devolvemos el color
		rpta2 += "~"+n_gnt.idrequerimiento.peticion.color
		
		# Se reaclculan los acumulados
		CalcularAcumulados(ArrID,ide,cli0,col0,req,val_1)

	return rpta2









#		Lógica del NEGOCIO (acumulados Gant)
def CalcularAcumulados(ArrID,ide,cli0,col0,req,val_1):

	# Actualiza el total Incurrido por Semana por Posición
	sem_v1 = ArrID[5]
	ActTotIncSemPos(ArrID,ide,cli0,col0,req,val_1)

	# Total H.Acuerdo semanal
	ArrID[5] = sem_v1
	CalcularHAcuerdo(ArrID,cli0,col0,req)
	
	# Actualiza el total incurrido semanal
	ArrID[5] = sem_v1
	ActTotIncSemanal(ArrID,cli0,req)

	# Calcula la disponibilidad
	ArrID[5] = sem_v1
	CalcularDisponibilidad(ArrID,cli0,col0,req)

	# Calcular resumen diarios 
	ArrID[5] = sem_v1
	CalcularZdia(ArrID,cli0,col0,req)









# Calcula los acumulados diarios
def CalcularZdia(ArrID,cli0,col0,req):
	# idr_CLI_COL_AA_MM_SEM_DIA_POS   -> 	Así llega

	
	#  CALCULAMOS LAS HORAS INCURRIDAS EL DÍA  = = = = = = = = = = = = = = = = = = = = = #
	tot = 0.0
	lst_di = Gant.objects.filter( Q(idcliente =str(ArrID[1])) &  Q(anio=str(ArrID[3])) &  Q(mes=str(ArrID[4])) &  Q(dia=str(ArrID[6])) )
	lst_di = lst_di.exclude( Q(posicion='za') | Q(posicion='zi') | Q(posicion='zd') | Q(posicion='zj') )
	
	#  Sumamos todas las imputaciones de ese día
	#print("   >> ----------------------------------- ||> ")
	for di in lst_di:
		tot = tot + di.imputacion
		#print("   >>  key : "+di.llave+"    "+str(di.imputacion)+'  = '+str(tot)+'   -   '+str(di.idauth))

	# Construimos la llave
	n_llav =  ArrID[1]+"_1_"+ArrID[3]+"_"+ArrID[4]+"_"+ArrID[5]+"_"+ArrID[6]+"_zi"

	# Validamos si tenemos que crear un nuevo o modificar uno existentre
	if Gant.objects.filter(llave=n_llav).exists():
		gnt1 = Gant.objects.get(llave=n_llav)
		gnt1.imputacion = float(tot)
		gnt1.save()
	else: 
		gnt1 = Gant()
		gnt1.idcliente = cli0
		gnt1.llave 	= n_llav
		gnt1.idauth 	= col0
		gnt1.anio 	= ArrID[3]
		gnt1.mes 	= ArrID[4]
		gnt1.sem 	= ArrID[5]
		gnt1.dia 	= ArrID[6]
		gnt1.idrequerimiento = req
		gnt1.posicion = 'zi'				# ----> RESUMEN DE INCURRIDO DIARIO
		gnt1.fecha_modif = datetime.datetime.now()
		gnt1.fecha_clave = '20'+ArrID[3]+"-"+ArrID[4]+"-"+ArrID[6]
		gnt1.imputacion =  float(tot)
		gnt1.save()





	#  CALCULAMOS LAS HORAS ACUERDO DIARIAS  = = = = = = = = = = = = = = = = = = = = = #
	
	# Calculamos las horas acuerdo estándar
	ArrR = ObtUltDiaDelMes(('20'+str(ArrID[3])),ArrID[4])

	# Obtener los colaboradores asignados para ese cliente, esas fechas.
	lst_asg =  ObtLstAsg(cli0,ArrR[0],ArrR[1])
	#print(" >> CalcularZdia: "+str(len(lst_asg)))

	tot1 = 0.0
	for asg in lst_asg:
		tot1 = tot1 + asg.asignacion
		#print("  -> "+str(asg.idauth.alias)+':-:'+str(asg.asignacion)+"  _  "+str(tot1))

	# Construimos la llave
	n_llav1 =  ArrID[1]+"_1_"+ArrID[3]+"_"+ArrID[4]+"_"+ArrID[5]+"_"+ArrID[6]+"_za"


	# Verificamos si hay algún ajuste para ese días 
	# Aplicamos ajuste al cáculo de H.Acuerdo	
	n_llav2 =  ArrID[1]+"_1_"+ArrID[3]+"_"+ArrID[4]+"_"+ArrID[5]+"_"+ArrID[6]+"_zj"
	if Gant.objects.filter(llave=n_llav2).exists():
		ajt = Gant.objects.get(llave=n_llav2).imputacion
		tot1 = float(tot1) - float(ajt)



	# Validamos si tenemos que crear un nuevo o modificar uno existentre
	if Gant.objects.filter(llave=n_llav1).exists():
		gnt2 = Gant.objects.get(llave=n_llav1)
		gnt2.imputacion = float(tot1)
		gnt2.save()
	else: 
		gnt2 = Gant()
		gnt2.idcliente = cli0
		gnt2.llave 	= n_llav1
		gnt2.idauth 	= col0
		gnt2.anio 	= ArrID[3]
		gnt2.mes 	= ArrID[4]
		gnt2.sem 	= ArrID[5]
		gnt2.dia 	= ArrID[6]
		gnt2.idrequerimiento = req
		gnt2.posicion    = 'za'				# ----> HORAS ACUERDO DIARIO
		gnt2.fecha_modif = datetime.datetime.now()
		gnt2.fecha_clave = '20'+ArrID[3]+"-"+ArrID[4]+"-"+ArrID[6]
		gnt2.imputacion  = float(tot1)
		gnt2.save()



	#  CALCULAMOS LAS HORAS DE DISPONIBILIDAD AL DÍA  = = = = = = = = = = = = = = = = = = = = = #
	tot2 = 0.0
	tot2 = ( tot1 - tot )
	#print("  >> tot1 : "+str(tot1)+" - tot: "+str(tot)+"  =  tot2 = "+str(tot2))

	# Construimos la llave
	n_llav2 =  ArrID[1]+"_1_"+ArrID[3]+"_"+ArrID[4]+"_"+ArrID[5]+"_"+ArrID[6]+"_zd"
	# print( "  >> llv: "+str(n_llav2)+"   ::  "+str(tot2))

	# Validamos si tenemos que crear un nuevo o modificar uno existentre
	if Gant.objects.filter(llave=n_llav2).exists():
		gnt3 = Gant.objects.get(llave=n_llav2)
		gnt3.imputacion = float(tot2)
		gnt3.save()
	else: 
		gnt3 = Gant()
		gnt3.idcliente = cli0
		gnt3.llave 	= n_llav2
		gnt3.idauth 	= col0
		gnt3.anio 	= ArrID[3]
		gnt3.mes 	= ArrID[4]
		gnt3.sem 	= ArrID[5]
		gnt3.dia 	= ArrID[6]
		gnt3.idrequerimiento = req
		gnt3.posicion = 'zd'				# ----> DISPONIBILIDAD DIARIA
		gnt3.fecha_modif = datetime.datetime.now()
		gnt3.fecha_clave = '20'+ArrID[3]+"-"+ArrID[4]+"-"+ArrID[6]
		gnt3.imputacion =  float(tot2)
		gnt3.save()






#		========================================================================================================0
#  0.-	Actulización del total incurrido por posición  	=======================================================ok
def ActTotIncSemPos(ArrID,ide,cli0,col0,req,val_1):

	# Debe recalcular la sem en cuestión y todas las siguientes.....
	ArrID_A = ArrID
	sem_v = int(ArrID[5])
	for x in range(6 - int(ArrID[5])):
		ArrID_A[5] = str(sem_v)
		ActTotIncSemPos_old(ArrID_A,ide,cli0,col0,req,val_1)
		sem_v += 1

#	Calcula el incurrido total de la semana que se le indica....
def ActTotIncSemPos_old(ArrID,ide,cli0,col0,req,val_1):
	#	Construímos la clave del resumen y luego verificamos si ya existe.
	#	Cli_Aut_AA_MM_sem_(rs)_Pos
	n_llav = ArrID[1]+"_"+ArrID[2]+"_"+ArrID[3]+"_"+ArrID[4]+"_"+ArrID[5]+"_rs_"+ArrID[7]

	if Gant.objects.filter(llave=n_llav).exists():
		gnt_act = Gant.objects.get(llave=n_llav)
		gnt_act.imputacion = RecTotIncSemPos(ArrID,cli0,col0)
		gnt_act.save()
		
	else: 
		gnt_act = Gant()
		gnt_act.idcliente = cli0
		gnt_act.llave 	= n_llav
		gnt_act.idauth 	= col0
		gnt_act.anio 	= ArrID[3]
		gnt_act.mes 	= ArrID[4]
		gnt_act.sem 	= ArrID[5]
		gnt_act.dia 	= 'rs'
		gnt_act.idrequerimiento = req
		gnt_act.posicion = ArrID[7]
		gnt_act.fecha_modif = datetime.datetime.now()
		gnt_act.fecha_clave = '20'+ArrID[3]+"-"+ArrID[4]+"-"+ArrID[6]
		gnt_act.imputacion =  RecTotIncSemPos(ArrID,cli0,col0) #float(val_2)
		gnt_act.save()


def RecTotIncSemPos(ArrID,cli0,col0):
	#	Filtramos lo imputado esa semana exceptuando el resumen de la imputación
	lst_sem = Gant.objects.filter(idcliente=cli0,idauth=col0,anio=ArrID[3],mes=ArrID[4],sem=ArrID[5],posicion=ArrID[7]).exclude(Q(dia='ha') | Q(dia='in') | Q(dia='di') | Q(dia='rs'))
	rpta = 0.0
	for x in lst_sem:
		rpta += float(x.imputacion)
	#	Verificamos si existe la semana anterior y la sumamos.
	n_llav2 = ArrID[1]+"_"+ArrID[2]+"_"+ArrID[3]+"_"+ArrID[4]+"_"+str(int(ArrID[5])-1)+"_rs_"+ArrID[7]
	if Gant.objects.filter(llave=n_llav2).exists():
		rpta += float(Gant.objects.get(llave=n_llav2).imputacion)
	return rpta










 
#		========================================================================================================1
#  1.-	Calculamos las Horas acuerdo ==========================================================================ok
def CalcularHAcuerdo(ArrID,cli0,col0,req):

	#  ArrID['idi', '34', '1', '21', '05', '3', '20', '4']
	
	#  DE TRATARSE DEL 1° REGISTRO, CREAREMOS ACUMULADOS DIARIOS DE H.ACUERDO DE TOD.O EL MES   #
	if not Gant.objects.filter( Q(idcliente=cli0) & Q(anio=ArrID[3]) & Q(mes=ArrID[4]) & Q(posicion='za') ).exists():
		CalcularHAcuerdo001(ArrID,cli0,col0,req)# Calculamos las horas acuerdo estándar

	# Debe calcular la sem en cuestión y todas las siguientes.....
	sem_tamp = ArrID[5]
	dia_tamp = ArrID[6]

	#	Reemplazamos por el primer día de la semana. para cáculos más prácticos
	ArrF = DiasLabPorSem(ArrID)
	ArrID[6] = str(ArrF[1].day)

	# Lo realizamos para todas las sem sgts
	for x in range(5):
		# Validamos si la fecha sgte a consultar es válida
		fec_s = "20"+ArrID[3]+'-'+ArrID[4]+'-'+ArrID[6]
		if is_date(fec_s):
			CalcularHAcuerdo_old(ArrID,cli0,col0,req)
			ArrID[5] = str(int(ArrID[5]) + 1 )
			ArrID[6] = str(int(ArrID[6]) + 7 )

	# Crear las horas acuerdo apra todo el mes.
	#  Colocamos datos originales
	ArrID[5] = sem_tamp
	ArrID[6] = dia_tamp






# ----------------------------------------------------------------------------------------- #
#  DE TRATARSE DEL 1° REGISTRO, CREAREMOS ACUMULADOS DIARIOS DE H.ACUERDO DE TOD.O EL MES   #
# ----------------------------------------------------------------------------------------- #
def CalcularHAcuerdo001(ArrID,cli0,col0,req):

	#  ArrID[   0  ,   1   ,   2   ,  3  ,   4  ,  5  ,  6  ,  7  ]
	#  ArrID[ 'idi', idCli , idCol , año ,  mes , sem , día , pos ]
	#  ArrID[ 'idi', '34'  ,  '1'  , '21', '05' , '3' , '20', '4' ]

	# Calculamos las horas acuerdo estándar
	ArrR = ObtUltDiaDelMes(('20'+str(ArrID[3])),ArrID[4])
	#print(' >> CalcularHAcuerdo001: dia_i:'+str(ArrR[0])+'  dia_f:'+str(ArrR[1]))

	# Obtener los colaboradores asignados para ese cliente, esas fechas.
	lst_asg =  ObtLstAsg(cli0,ArrR[0],ArrR[1])
	#print(" >> CalcularHAcuerdo001: "+str(len(lst_asg))+'  dia_i:'+str(ArrR[0])+'  dia_f:'+str(ArrR[1])) 

	h_acu = 0.0
	h_ac2 = 0.0
	for asg in lst_asg:
		h_acu = h_acu + asg.asignacion
		#print("  '°->"+str(h_acu)+'   -| '+str(asg.idauth.alias))
	h_ac2 = h_acu


	# Validamos los días festivos
	llv_fest = '20'+str(ArrID[3])+'_'+str(ArrID[4])+'_'+str(ArrID[1])+''
	lst_fest = []
	if Hardcode.objects.filter( Q(app='gest') & Q(asp='gnt') & Q(typcon='clie') & Q(consum='HA-aj') & Q(item=llv_fest) ).exists():
		hrd = Hardcode.objects.filter( Q(app='gest') & Q(asp='gnt') & Q(typcon='clie') & Q(consum='HA-aj') & Q(item=llv_fest) ).first()
		lst_fest = hrd.val01.split('~')

	# validamos por semana
	dia_6 = ArrID[6]
	ArrID[6] = '3'
	ArrG = DiasLabPorSem(ArrID)		#	Devuelve [ fecha dada | primer día lab | último día lab. | cant ]
	find = int(ArrG[2].day)			# 	Calculamos lo viernes
	ArrID[6] = str(ArrG[1].day)		# 	Establesclo el inicio en el 1° día laborables


	# Recorremos el mes completo
	diaa = int(ArrG[1].day) - 1
	sem = 1
	while diaa <= 31:
		h_acu = h_ac2
		diaa += 1

		# los días festivos mapeados no los creamos
		if str(diaa) in lst_fest:
			pass
		else:
			
			dat = "20"+ArrID[3]+'-'+ArrID[4]+'-'+str(diaa)
			if is_date(dat):

				# -ini----------- CREAMOS EL REGISTRO ----------------------# 
				# Construimos la llave de las H.Acuerdo
				n_llav1 =  ArrID[1]+"_1_"+ArrID[3]+"_"+ArrID[4]+"_"+str(sem)+"_"+str(diaa)+"_za"

				# Construimos la llave del AJUSTE de las H.Acuerdo y ajustamos
				n_llav2 =  ArrID[1]+"_1_"+ArrID[3]+"_"+ArrID[4]+"_"+str(sem)+"_"+str(diaa)+"_zj"
				if Gant.objects.filter(llave=n_llav2).exists():
					ajt = Gant.objects.get(llave=n_llav2).imputacion
					h_acu = float(h_acu) - float(ajt)
				#print(" >>"+str(dat)+' : '+str(find)+"  :: "+n_llav1+"    :->  "+str(h_acu))

				# Validamos si tenemos que crear un nuevo o modificar uno existentre
				if Gant.objects.filter(llave=n_llav1).exists():
					gnt2 = Gant.objects.get(llave=n_llav1)
					gnt2.imputacion = float(h_acu)
					gnt2.save()
				else: 
					gnt2 = Gant()
					gnt2.idcliente = cli0
					gnt2.llave 	= n_llav1
					gnt2.idauth 	= col0
					gnt2.anio 	= ArrID[3]
					gnt2.mes 	= ArrID[4]
					gnt2.sem 	= str(sem)
					gnt2.dia 	= str(diaa)
					gnt2.idrequerimiento = req
					gnt2.posicion    = 'za'				# ----> HORAS ACUERDO DIARIO
					gnt2.fecha_modif = datetime.datetime.now()
					gnt2.fecha_clave = '20'+ArrID[3]+"-"+ArrID[4]+"-"+ArrID[6]
					gnt2.imputacion  = float(h_acu)
					gnt2.save()
				# -end----------- CREAMOS EL REGISTRO ----------------------#
		
		if diaa == find:
			sem += 1   		# Aumentamos la semana
			diaa += 2		# Nos saltamos los fines de semana
			find = find + 7 # calculamos el sgte viernes

	# Devolvemos su valor original
	ArrID[6] = dia_6











def CalcularHAcuerdo_old(ArrID,cli0,col0,req):
	#	CLI_(au)_AA_MM_SEM_(ha)_SEM
	n_llav 	= ArrID[1]+"_au_"+ArrID[3]+"_"+ArrID[4]+"_"+ArrID[5]+"_ha_"+ArrID[5]
	n_gnt = ""

	# Calculamos las H.Acuerdao de la semana en iteración
	lst_ha = Gant.objects.filter( Q(idcliente=ArrID[1]) & Q(anio=ArrID[3]) & Q(mes=ArrID[4]) & Q(sem=ArrID[5]) & Q(posicion='za') )
	#lst_ha.delete() #  ::: bug de Hrs.Acuerdo

	n_imp = 0.0
	for za in lst_ha:
		n_imp = n_imp + float(za.imputacion)
		#print("     _ __>2> "+str(za.llave)+"  +  "+str(za.imputacion)+"   = "+str(n_imp))

	
	#	Verificamos si existe la semana anterior y la sumamos.
	n_llav2 = ArrID[1]+"_au_"+ArrID[3]+"_"+ArrID[4]+"_"+str(int(ArrID[5])-1)+"_ha_"+str(int(ArrID[5])-1)
	if Gant.objects.filter(llave=n_llav2).exists():
		n_imp += float(Gant.objects.get(llave=n_llav2).imputacion)


	#	Procedemos con la creación o midificación del gant  HA
	if Gant.objects.filter(llave=n_llav).exists():
		n_gnt=Gant.objects.get(llave=n_llav)
		n_gnt.imputacion = n_imp
		n_gnt.save()
	else:
		n_gnt=Gant()
		n_gnt.idcliente = cli0
		n_gnt.llave 	= n_llav
		n_gnt.idauth 	= col0
		n_gnt.anio 		= ArrID[3]
		n_gnt.mes 		= ArrID[4]
		n_gnt.sem 		= ArrID[5]
		n_gnt.dia 		= 'ha'
		n_gnt.idrequerimiento = req
		n_gnt.posicion 	= ArrID[7]
		n_gnt.fecha_modif	= datetime.datetime.now()
		n_gnt.fecha_clave	= '20'+ArrID[3]+'-'+ArrID[4]+'-'+ArrID[6]
		n_gnt.imputacion = n_imp
		n_gnt.save() 














#		========================================================================================================2
# 	2.-	Actualizamos total incurrido por semana ===============================================================ok

def ActTotIncSemanal(ArrID,cli0,req):

	# Debe recalcular la sem en cuestión y todas las siguientes.....
	ArrID_A = ArrID
	sem_v = int(ArrID[5])
	for x in range(6 - int(ArrID[5])):
		ArrID_A[5] = str(sem_v)
		ActTotIncSemanal_old(ArrID,cli0,req)
		sem_v += 1

#	Se calcula el incurrido de la semana que se le indica....
def ActTotIncSemanal_old(ArrIDx,cli0,req):
	# 	Construímos el resumen de ha por semana.
	#  	Cli_(au)_AA_MM_Sem_(in)_(1)
	n_llav = ArrIDx[1]+"_au_"+ArrIDx[3]+"_"+ArrIDx[4]+"_"+ArrIDx[5]+"_in_"+ArrIDx[5]
	if Gant.objects.filter(llave=n_llav).exists():
		gnt_act = Gant.objects.get(llave=n_llav)
		gnt_act.imputacion = RecTotIncSemanal(ArrIDx,cli0)
		gnt_act.save()
	else: 
		gnt_act = Gant()
		gnt_act.idcliente = cli0
		gnt_act.llave 	= n_llav
		gnt_act.idauth 	= AuthUser.objects.get(pk=4) #grcl4
		gnt_act.anio 	= ArrIDx[3]
		gnt_act.mes 	= ArrIDx[4]
		gnt_act.sem 	= ArrIDx[5]
		gnt_act.dia 	= 'in'
		gnt_act.idrequerimiento = req
		gnt_act.posicion = ArrIDx[7]
		gnt_act.fecha_modif	= datetime.datetime.now()
		gnt_act.fecha_clave	= '20'+ArrIDx[3]+'-'+ArrIDx[4]+'-'+ArrIDx[6]
		gnt_act.imputacion =  RecTotIncSemanal(ArrIDx,cli0)
		gnt_act.save()

def RecTotIncSemanal(ArrIDx,cli0):	
	lst_rs = Gant.objects.filter(idcliente=cli0,anio=ArrIDx[3],mes=ArrIDx[4],sem=ArrIDx[5],dia='rs')
	rpta = 0.0
	for x in lst_rs:
		rpta = rpta + float(x.imputacion)
	return rpta









#		========================================================================================================3
#	3.-	Calculamos la Disponibiidad ===========================================================================ok
def CalcularDisponibilidad(ArrID,cli0,col0,req):
	# Debe recalcular la sem en cuestión y todas las siguientes.....
	ArrID_A = ArrID
	sem_v = int(ArrID[5])

	for x in range(6 - int(ArrID[5])):
		ArrID_A[5] = str(sem_v)
		CalcularDispoOld(ArrID,cli0,col0,req)
		sem_v += 1







def CalcularDispoOld(ArrID,cli0,col0,req):
	#	0	1	2  3  4  5  6   7
	# idr_CLI_COL_AA_MM_SEM_DIA_POS   -> 	Así llega
	#Creamos Id Ha  -> CLI_(au)_AA_MM_SEM_(ha)_SEM
	#Creamos Id Inc -> CLI_(au)_AA_MM_SEM_(in)_SEM 
	#Creamos Id dis -> CLI_(au)_AA_MM_SEM_(di)_SEM

	id_ha=ArrID[1]+'_au_'+ArrID[3]+'_'+ArrID[4]+'_'+ArrID[5]+'_ha_'+ArrID[5]
	id_in=ArrID[1]+'_au_'+ArrID[3]+'_'+ArrID[4]+'_'+ArrID[5]+'_in_'+ArrID[5]
	n_llv=ArrID[1]+'_au_'+ArrID[3]+'_'+ArrID[4]+'_'+ArrID[5]+'_di_'+ArrID[5]
	n_gnt = ""
	in_t = 0.0
	ha_t = 0.0

	if Gant.objects.filter(llave=id_in).exists():
		in_t = Gant.objects.get(llave=id_in).imputacion

	if Gant.objects.filter(llave=id_ha).exists():
		ha_t = Gant.objects.get(llave=id_ha).imputacion


	imp = ha_t - in_t
	if imp < 0:
		imp = imp * -1

	if Gant.objects.filter(llave=n_llv).exists():#	Verificamos si hay que crear o solo actualizar.
		n_gnt=Gant.objects.get(llave=n_llv)
		n_gnt.imputacion =  imp
		n_gnt.save()
		rpta2='ACT' #	Actualizó, ya existía.
	else:
		n_gnt = Gant()
		n_gnt.idcliente = cli0
		n_gnt.llave 	= n_llv
		n_gnt.idauth 	= col0
		n_gnt.anio 		= ArrID[3]
		n_gnt.mes 		= ArrID[4]
		n_gnt.sem 		= ArrID[5]
		n_gnt.dia 		= 'di'
		n_gnt.idrequerimiento = req
		n_gnt.posicion 	= ArrID[7]
		n_gnt.fecha_modif	= datetime.datetime.now()
		n_gnt.fecha_clave	= '20'+ArrID[3]+'-'+ArrID[4]+'-'+ArrID[6]
		n_gnt.imputacion =  imp
		n_gnt.save()
		rpta2='REG'	#	Registró nuevo Gant.












 

# 	Validación para eliminar registro de Gant ===================================================================
class Gnt_vd1(View):

	def get(self,request,*args,**kwargs):

		rpta = "Nex" #	No existe nada que boorar
		ide = self.request.GET.get('ide')
		usr = self.request.user.pk

		rpta = GntValid(self.request,ide,'Ok')
		if rpta != 'Ok':
			return HttpResponse(rpta)

		if Gant.objects.filter(llave = ide[4:len(ide)]).exists():
			gnt1 = Gant.objects.get(llave = ide[4:len(ide)])
			if gnt1.idauth.pk == usr:
				rpta = 'Exi' #	Si existe nada que boorar
			else:
				rpta = 'Npe' #	No permisos para borrar
		else:
			rpta = 'Nex' #	No existe nada que boorar

		return HttpResponse(rpta)
"""
"Nex" #	No existe nada que boorar
'Exi' #	Si existe nada que boorar
'Npe' #	No permisos para borrar
"""


#		Borrar regitro de Gant 	
class Gnt_d1(View):

	# idr_CLI_COL_AA_MM_SEM_DIA_POS   -> 	Así llega

	def get(self,request,*args,**kwargs):

		rpta = "Err" #	No existe nada que boorar
		ide = self.request.GET.get('ide')
		usr = self.request.user.pk
		#print("  >> ide : "+str(ide))

		if Gant.objects.filter(llave = ide[4:len(ide)]).exists():
			gnt1 = Gant.objects.get(llave = ide[4:len(ide)])
			if gnt1.idauth.pk == usr:
				# Guardo el req
				req = gnt1.idrequerimiento
				gnt1.delete()
				rpta 	= 'Ok' 				#	Borrado exitoso.
				ArrID 	= ide.split('_')	# 	idr_CLI_COL_AA_MM_SEM_DIA_POS   -> 	Así llega
				# Relizar nuevos calculos
				#print("  >>-:>  ArrID[1] = "+str(ArrID[1])+"    ArrID[2] = "+str(ArrID[2])+" cod = "+str(req.codigo))
				CalcularAcumulados(ArrID,ide,ArrID[1],ArrID[2],req,req.codigo)

			else:
				rpta = 'Npe' #	No permisos para borrar

		return HttpResponse(rpta)
"""
"Nex" #	No existe nada que boorar
'Exi' #	Si existe nada que boorar
'Npe' #	No permisos para borrar
"""






#		Consulta detalle de Gant    
class Gnt_d2(View):
	#	0	1	2  3  4  5  6   7
	# idr_CLI_COL_AA_MM_SEM_DIA_POS   -> 	Así llega

	def get(self,request,*args,**kwargs):
		ide = self.request.GET.get('ide')
		rpta = "Nex"

		if Gant.objects.filter(llave=ide[4:len(ide)]).exists():
			gnt0 = Gant.objects.get(llave=ide[4:len(ide)])

			#	Horas Acuerdo
			req_hac = gnt0.idrequerimiento.estimacion_acuerdo

			#	Total incurrido ese día por el usuario.
			LstGntUsu = Gant.objects.filter(Q(idauth = gnt0.idauth) & Q(anio=gnt0.anio) & Q(mes=gnt0.mes) & Q(dia=gnt0.dia))
			LstGntUsu = LstGntUsu.exclude(Q(dia='ha') | Q(dia='in') | Q(dia='di') | Q(dia='rs') | Q(posicion='za') | Q(posicion='zi') | Q(posicion='zd') | Q(posicion='zj'))
			inc_hoy_usu = 0.0
			for x in LstGntUsu:
				inc_hoy_usu = inc_hoy_usu + x.imputacion
				#print("  -> key: "+x.llave+' val: '+str(x.imputacion)+'   cli: '+str(x.idcliente))


			#  Total incurrido en el requerimiento
			LstGntReq = Gant.objects.filter(idrequerimiento = gnt0.idrequerimiento)
			LstGntReq = LstGntReq.exclude(Q(dia='ha') | Q(dia='in') | Q(dia='di') | Q(dia='rs') | Q(posicion='za') | Q(posicion='zi') | Q(posicion='zd')  | Q(posicion='zj'))
			req_inc = 0.0
			gnt_cnt = 0
			for y in LstGntReq:
				req_inc += y.imputacion
				gnt_cnt += 1
				#print("  -> key "+x.llave)


			#  Calcular acumulado en TASK del reque 
			tsk_cnt = 0
			tsk_pla = 0.0
			tsk_inc = 0.0

			LstTsk = Task.objects.filter(requerimiento=gnt0.idrequerimiento)
			for z in LstTsk:
				tsk_cnt += 1
				tsk_pla += z.esfuerzo_total_estandar
				tsk_inc += z.esfuerzo_ejecutado


			# Estimación     -- se retiró el 23.11.2022
			est_sum = 0.0
			est_cnt = 0
			#LstEstim = EstDetalle.objects.filter(requerimiento=gnt0.idrequerimiento)
			#for p in LstEstim:
			#	est_sum += p.esfuerzo
			#	est_cnt += 1



			#  Creamos el JSON.
			desc = str(gnt0.idrequerimiento.breve_descripcion).replace('"', "'")

			rpta = '{"pet_nom":"'+gnt0.idrequerimiento.peticion.id_pet_fenix+' ['+ gnt0.idrequerimiento.peticion.id_ot_fenix +'] : '+gnt0.idrequerimiento.peticion.nombre+'."'

			rpta += ',"pet_col":"'+str(gnt0.idrequerimiento.peticion.color)+'"'

			rpta += ',"req_nom":"'+str(gnt0.idrequerimiento.modulo.codigo)+' : '+gnt0.idrequerimiento.codigo+'  @ '+desc+'."'
			rpta += ',"req_hac":"'+str(req_hac)+'"'			#	Horas acuerdo req

			rpta += ',"est_sum":"'+str(est_sum)+'"'				#	Estimación acumulado
			rpta += ',"est_cnt":"'+str(est_cnt)+'"'				#	Estimación cantidad

			rpta += ',"usu":"'+gnt0.idauth.alias+'"'				#	Colaborador
			rpta += ',"usu_inc":"'+str(inc_hoy_usu)+'"'				#	Colaborador incurrió hoy
			rpta += ',"usu_mod":"'+gnt0.idcol_edit.username+'"' 	# 	Última edición por

			rpta += ',"tsk_cnt":"'+str(tsk_cnt)+'"'			# Cantidad de tareas en task
			rpta += ',"tsk_pla":"'+str(tsk_pla)+'"'			# Cantidad de h planificadas en task
			rpta += ',"tsk_inc":"'+str(tsk_inc)+'"'			# Cantidad de h incurridas en task

			rpta += ',"gnt_pla":"'+str(req_inc)+'"'			#	Planificado en gant 
			rpta += ',"gnt_cnt":"'+str(gnt_cnt)+'"'			#	Cantidad de tareas en gant 

			rpta += ',"etc":"'+str( req_hac - tsk_inc )+'"'
			#print(" >> "+str(req_hac)+"  - "+str(tsk_inc))

			rpta += '}'
			
		else:
			rpta = "Nex"		
		#print("  >>> "+rpta)

		return HttpResponse(rpta)
"""
"Nex" #	No existe gant
"""





#		Obtiene los colaboradores asignados al cliente. ftes
class ObtAsignaciones(View):

	def get(self,request,*args,**kwargs):
		idc = self.request.GET.get('idc')
		anio = self.request.GET.get('anio')
		mes = self.request.GET.get('mes')
		fecha_desde = self.request.GET.get('fecha_desde')
		fecha_hasta = self.request.GET.get('fecha_hasta')
		#print(" >> idc:"+str(idc)+"  anio:"+str(anio)+"  mes:"+str(mes)+"  fd:"+str(fecha_desde)+"  fh:"+str(fecha_hasta))

		v1 =''
		jsn = '{'

		# Obtener los colaboradores asignados para ese cliente, esas fechas.
		asgns =  ObtLstAsg(idc,fecha_desde,fecha_hasta)
		#print(" >> ObtAsignaciones: "+str(len(asgns)))
		
		if len(asgns) > 0:
			client = Cliente.objects.get(idcliente=idc)

			# Obetenemos días no lavorables
			llv = ''+str(anio)+'_'+str(mes)+'_'+str(idc)
			if Hardcode.objects.filter( Q(app='gest') & Q(asp='gnt') & Q(typcon='clie') & Q(consum='HA-aj') & Q(item=llv) ).exists():
				hrd = Hardcode.objects.filter( Q(app='gest') & Q(asp='gnt') & Q(typcon='clie') & Q(consum='HA-aj') & Q(item=llv) ).first()
				v1 = hrd.val01
				if v1 == None:
					v1 = ''

			# Creamos el JSON				
			Cli = '"Cli":"'+str(client.cliente)+'",'
			Pai = '"Pai":"'+str(client.idpais.pais)+'",'
			lsC = '"lstCOL":"'
			lsI = '"lstIDs":"'
			Nlb = '"lstNlb":"'+str(v1)+'",'


			ftes = 0
			ftes_peso = 0.0
			prim = True
			for x in asgns:
				#print(" >> "+str(x.idauth.alias))
				if prim == True:
					prim = False					
					lsC += str(x.idauth.alias)
					lsI += str(x.idauth.pk)
				else:
					lsC += ','+ str(x.idauth.alias)
					lsI += ','+ str(x.idauth.pk)

				ftes_peso = ftes_peso + x.asignacion
				ftes = ftes + 1
			
			#Fte = '"Fte":" <b>'+str(client.codigo)+'<br><br><br>'+str(ftes)+'</b> FTEs <br><br><br> Con <b>'+str(ftes_peso)+'</b>  h/d",'
			Fte = '"Fte":" <b>'+str(ftes)+'</b> FTEs  _  <b>'+str(ftes_peso)+'</b>  h",'

			lsC += '",'
			jsn += '"msj":"Ok",'+Cli+Nlb+Pai+Fte+lsC+lsI+'"'
			jsn += ',"StrJsn":"'+GntLst(idc,fecha_desde,fecha_hasta)+'"}'

		else:
			jsn +='"msj":"Err"}'  
		
		#print("  >>"+str(jsn))
		return HttpResponse(jsn) 




# Función que trae todo el cuerpo del gant (el incurrido + resumenes)
def GntLst(idc,fecha_desde,fecha_hasta):

	#print("  >>> : "+str(idc) +" --- "+str(fecha_desde)+"','"+str(fecha_hasta))
	from django.db import connection, transaction
	cursor = connection.cursor()
	cursor.execute("CALL sp_gnt_x_fecha_y_cli ('"+str(fecha_desde)+"','"+str(fecha_hasta)+"',"+idc+")")
	resultado = cursor.fetchall()

	rpta = "{"
	cont = True

	#print(" >> ln : "+str(len(resultado)))
	for row in resultado:

		dic = dict(zip([col[0] for col in cursor.description], row))
		if cont:
			cont = False
			rpta += ""+dic['lst']+""
		else:
			rpta += ","+dic['lst']+""
	cursor.close()
	rpta += "}"
	#print("   ->"+rpta)
	return rpta







#  ================ HORAS ACUERDO AJUSTE ===============  #
# Consulta los ajustes H.Acuerdo 
class GntHajLst(View):

	def get(self,request,*args,**kwargs):
		llv = self.request.GET.get('llv')
		jsn = '{ "0":'

		if llv == '' or llv == None :
			jsn += '"Nll"}'
		else:
			jsn += ''

			ln =len(llv) - 1
			llv2 = ''+str(llv[0:ln]) + 'j'
			#print(" -->"+str(llv2))

			if Gant.objects.filter(llave=llv2).exists():
				gnt = Gant.objects.get(llave=llv2)
				jsn += '"ok","val":"'+str(gnt.imputacion)+'",'
				jsn += '"llv":"'+str(llv)+'"}'
			else:
				jsn += '"ok","val":"0","llv":"'+str(llv)+'"}'

		#print("  >> "+str(jsn))
		return HttpResponse(jsn)
"""
	'Nll' : No llegó
"""



 
# Actualizar ajuste de H.Acuerdo diario
class GntHajMdf(View):

	def get(self,request,*args,**kwargs):
		llv = self.request.GET.get('llv')
		val = self.request.GET.get('val')
		jsn = '{ "0":'
		#print("  >> "+str(llv))

		if llv == '' or val == '' :
			jsn += '"Nll"}'
		else:


			ln =len(llv) - 1
			llv2 = ''+str(llv[0:ln]) + 'j'
			ArrID = llv.split('_') # CLI_COL_AA_MM_SEM_DIA_POS   -> 	Así llega  
			

			# Lanzamos las validaciones
			# ide = idr_CLI_COL_AA_MM_SEM_DIA_POS   -> 	Así debería estar
			# ide =     CLI_COL_AA_MM_SEM_DIA_POS   -> 	Así llega  
			rpta = 'idr_'+str(ArrID[0])+'_'+str(self.request.user.pk)+'_'+str(ArrID[2])+'_'+str(ArrID[3])+'_'+str(ArrID[4])+'_'+str(ArrID[5])+'_1'
			rpta = GntValid(self.request,rpta,'Ok')
			if not rpta == 'Ok':
				jsn += '"'+rpta+'"}'
				return HttpResponse(jsn)


			# Calculamos las horas acuerdo estándar
			ArrR = ObtUltDiaDelMes(('20'+str(ArrID[2])),ArrID[3])
			
			# Obtener los colaboradores asignados para ese cliente, esas fechas.
			lst_asg =  ObtLstAsg(ArrID[0],ArrR[0],ArrR[1])
			#print(" >> GntHajMdf: "+str(len(lst_asg)))
			
			tot1 = 0.0
			for asg in lst_asg:
				tot1 = tot1 + asg.asignacion
				#print(" .,>> "+str(asg.idauth.alias)+" : "+str(asg.asignacion))

			# Ajustamos las horas acuerdo.
			if Gant.objects.filter(llave=llv).exists():
				gnt = Gant.objects.get(llave=llv)
				gnt.imputacion =  float(tot1) - float(val)
				gnt.save()

			# variables
			cli0 = Cliente.objects.get(pk=ArrID[0])
			col0 = AuthUser.objects.get(pk=self.request.user.pk)
			req  = Requerimientos.objects.filter().first()

			# Creamos/modificamos el ajuste
			if Gant.objects.filter(llave=llv2).exists():
				n_gnt = Gant.objects.get(llave=llv2)

				# Eliminamos si el valor del ajuste es 0
				if val == '0' or val == '0.0':
					n_gnt.delete()
				else:
					n_gnt.imputacion =  float(val)
					n_gnt.save()
				jsn += '"ok"}'

			else:
				n_gnt = Gant()
				n_gnt.idcliente = cli0
				n_gnt.llave 	= llv2
				n_gnt.idauth 	= col0
				n_gnt.anio 		= ArrID[2]
				n_gnt.mes 		= ArrID[3]
				n_gnt.sem 		= ArrID[4]
				n_gnt.dia 		= ArrID[5]
				n_gnt.idrequerimiento = req
				n_gnt.posicion 	= 'zj'
				n_gnt.fecha_modif	= datetime.datetime.now()
				n_gnt.fecha_clave	= '20'+ArrID[2]+'-'+ArrID[3]+'-'+ArrID[5]
				n_gnt.imputacion =  float(val)
				n_gnt.save()
				jsn += '"ok"}'	#	Registró nuevo Gant.

			# Recálculos _ de _ acumulados _ semanales _ _ _ _ _ _ _ _ _ _ _ //
			llv = 'idr_'+str(llv)
			ArrID = llv.split('_')

			# Total H.Acuerdo semanal
			sem_v1 = ArrID[5]
			CalcularHAcuerdo(ArrID,cli0,col0,req)

			# Calcula la disponibilidad
			ArrID[5] = sem_v1
			CalcularDisponibilidad(ArrID,cli0,col0,req)

			# Calcular resumen diarios 
			ArrID[5] = sem_v1
			CalcularZdia(ArrID,cli0,col0,req)

		#print("  >> "+str(jsn))
		return HttpResponse(jsn)
"""
	'Nll' : No llegó
"""


# Listar días no laborables
class GntDnlLst(View):

	def get(self,request,*args,**kwargs):
		#
		consum = self.request.GET.get('consum')
		#print(" >>: "+str(consum)) 
		jsn = '{ "0":'

		if consum == '':
			jsn += '"Nll"}'
		else:
			if Hardcode.objects.filter( Q(app='gest') & Q(asp='gnt') & Q(typcon='clie') & Q(consum='HA-aj') & Q(item=consum) ).exists():
				hrd = Hardcode.objects.filter( Q(app='gest') & Q(asp='gnt') & Q(typcon='clie') & Q(consum='HA-aj') & Q(item=consum) ).first()
				v1 = hrd.val01
				if v1 == None:
					v1 = ''
				v2 = hrd.val02
				if v2 == None:
					v2 = ''
				v3 = hrd.val03
				if v3 == None:
					v3 = ''
				jsn += '"ok","val01":"'+str(v1)+'","val02":"'+str(v2)+''+str(v3)+'"}'

			else:
				jsn += '"Nen"}'

		print("  >> "+str(jsn))
		return HttpResponse(jsn)
"""
	'Nll' : No llegó
	'Nee' : No encontrado
"""



# Actualizar HArdcode de días no laborables
class GntDnlUpd(View):

	def get(self,request,*args,**kwargs):
		#
		consum = self.request.GET.get('consum')
		v1 = self.request.GET.get('val01')
		v2 = self.request.GET.get('val02')
		print(" >>: "+str(consum)+'  -  '+str(v1)+'  -  '+str(v2)) 
		jsn = '{ "0":'

		if consum == '':
			jsn += '"Nll"}'
		else:
			ArrG = consum.split('_')
			if not AuthCliente.objects.filter( Q(idauth=self.request.user.pk) & Q(idcliente=int(ArrG[2])) ).exists():
				jsn += '"NUsr"}'
				return HttpResponse(jsn)



			if Hardcode.objects.filter( Q(app='gest') & Q(asp='gnt') & Q(typcon='clie') & Q(consum='HA-aj') & Q(item=consum) ).exists():
				hrd = Hardcode.objects.filter( Q(app='gest') & Q(asp='gnt') & Q(typcon='clie') & Q(consum='HA-aj') & Q(item=consum) ).first()
				hrd.val01 = v1
				tam = len(v2)
				if tam <= 100:
					hrd.val02 = v2
					hrd.val03 = ''
				else:
					hrd.val02 = v2[0:100]
					hrd.val03 = v2[100:tam]
				hrd.save()

			else:
				hrd = Hardcode()
				hrd.app = 'gest'
				hrd.asp = 'gnt'
				hrd.typcon = 'clie'
				hrd.consum = 'HA-aj'
				hrd.item = consum
				hrd.val01 = v1 
				hrd.val02 = v2[0:100]
				hrd.val03 = v2[100:200]
				hrd.save()
			jsn += '"ok"}'

		#print("  >> "+str(jsn))
		return HttpResponse(jsn)
"""
	'Nll' : No llegó
	'Nee' : No encontrado
"""




#  Elimina todos las horas acuerdo calculadas para que se haga nuevamente el cálculo
class GntDnlRef(View):

	def get(self,request,*args,**kwargs):

		ussr = self.request.user.pk
		ess = False

		# Validamos el permiso
		if AuthUserUserPermissions.objects.filter( Q(user=ussr) & Q(permission=204) ).exists():
			ess = True
		elif AuthUserUserPermissions.objects.filter( Q(user=ussr) & Q(permission=203) ).exists():
			ess = True

		jsn = '{ "0":'

		if ess == True:
			idc  = self.request.GET.get('idc')
			anio = self.request.GET.get('anio')
			mes  = self.request.GET.get('mes')


			# Verificamos para eliminar
			if idc != '0' and idc != 0 and idc != None :
				cli0 = Cliente.objects.get(pk=idc)
				# Eliminamos de todo el mes las horas acuerdo 
				if Gant.objects.filter( Q(idcliente=cli0) & Q(anio=anio[2:4]) & Q(mes=mes) & Q(posicion='za') ).exists():
					Gant.objects.filter( Q(idcliente=cli0) & Q(anio=anio[2:4]) & Q(mes=mes) & Q(posicion='za') ).delete()
					jsn += '"ok"}'

					# Los resúmenes semales también
					# hrs.Acuerdo
					if Gant.objects.filter( Q(idcliente=cli0) & Q(anio=anio[2:4]) & Q(mes=mes) & Q(dia='ha') ).exists():
						Gant.objects.filter( Q(idcliente=cli0) & Q(anio=anio[2:4]) & Q(mes=mes) & Q(dia='ha') ).delete()
						
					# Incurrido
					if Gant.objects.filter( Q(idcliente=cli0) & Q(anio=anio[2:4]) & Q(mes=mes) & Q(dia='in') ).exists():
						Gant.objects.filter( Q(idcliente=cli0) & Q(anio=anio[2:4]) & Q(mes=mes) & Q(dia='in') ).delete()
						
					# Disponibilidad
					if Gant.objects.filter( Q(idcliente=cli0) & Q(anio=anio[2:4]) & Q(mes=mes) & Q(dia='di') ).exists():
						Gant.objects.filter( Q(idcliente=cli0) & Q(anio=anio[2:4]) & Q(mes=mes) & Q(dia='di') ).delete()
						
				else:
					jsn += '"Noe"}'
			else:
				jsn += '"Nll"}'
		else:
			jsn += '"Nel"}'

		#print("  >> "+str(jsn))
		return HttpResponse(jsn)
"""
	'Noe' : No encontrado
	'Nll' : No llegaron los datos al server
"""

