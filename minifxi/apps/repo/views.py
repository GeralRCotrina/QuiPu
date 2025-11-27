
from pprint import pprint
from django.views.generic import  View
from django.shortcuts import render
from apps.gestion.models import *
from apps.gestion.gv_view import *
from django.db.models import Q
import datetime
import calendar
from django.db import connection


# Create your views here.

#	Reporte los Viernes 
class Rep008(View): 

	def get(self,request,*args,**kwargs):

		# Get request
		idu = self.request.GET.get('idu')
		fd1 = self.request.GET.get('fd1')
		fh1 = self.request.GET.get('fh1')
		usr = AuthUser.objects.get(pk=self.request.user.pk)

		# Código default
		if idu == None:
			idu = usr.codigo

		# Fecha Hasta default
		if fd1 == None:
			fd2 = datetime.datetime.now()
			fd1 = "'"+str(fd2.year)+"-"+str(fd2.month)+"-01'"
			#print(">> No :. fd1 : "+str(fd1))
		if fh1 == None:
			fh2 = datetime.datetime.now()
			fh1 = "'"+str(fh2.year)+"-"+str(fh2.month)+"-"+str(fh2.day)+"'"
			#print(">> No :. fh1 : "+str(fh1))

		#-----------------LISTA DE TAREAS--------------#
		cursor = connection.cursor()
		cursor.execute("CALL sp_rep008("+str(fd1)+","+str(fh1)+",'"+str(idu)+"')")
		resultado = cursor.fetchall()
		

		row_lst = []
		import numpy as np
		cont = -1
		object_list = []
		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)

			# llenamos la matriz
			cont += 1
			row_lst[cont] = row

			print(" -----------> row[1]: "+str(row[1]))
			#print(" -----------> dic: "+str(dic)+"     -  row[1]: "+str(row[1]))
			#horas = horas + float(row[5])
		cursor.close()

		#-----------------LISTA DE CLIENTES--------------#
		cursor = connection.cursor()
		cursor.execute("CALL sp_rep008_cli("+str(self.request.user.pk)+")")
		cursor.execute("CALL sp_rep008_cli("+str(self.request.user.pk)+")")
		resultado = cursor.fetchall()
		
		cli_lst = []
		#cli_lst.append("{'idcliente': 33, 'cliente': 'Locura', 'codigo': 'USISAP', 'wi_id': '10', 'color': '#3d5dff'}")
		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			cli_lst.append(dic)
			#print("---->"+str(dic))
		cursor.close()

		#-----------------ARMAMOS LA TABLA--------------#
		tabla_list = []
		lin = 0
		import ast
		import json

		for row in cli_lst:
			# Convertimos a string para luego a diccionario
			dic_1 = ast.literal_eval(str(row))
			lin += 1
			linea = '{"item":"' + str(lin) + '",'
			linea += '"cliente":"'+str(dic_1.get("cliente")) +'",'
			linea += '"color":"'+str(dic_1.get("color")) +'",'
			linea += '"codigo":"'+str(dic_1.get("codigo")) +'",'
			linea += '"wi_id":"'+str(dic_1.get("wi_id")) + '",'
			
			# -------------------------------------------------------
			dia1 = 0
			while dia1 <= 30:

				# Acumulamos del día 
				#for item in object_list if :


				dia1 += 1
				linea += '"dia_'+str(dia1)+'":"dia__'+str(dia1) + '"'
				if dia1 != 31:
					linea += ','

			# -------------------------------------------------------
			
			
			linea += '}'
			# Agregamos la línea del cliente / en formato diccionario
			#print("-------------->"+linea)
			tabla_list.append(json.loads(linea))
			
		dicc = { 
			'msj' : ' trabajadas',
			'object_list' : object_list,
			'tabla_list' : tabla_list
		}
		return render(request,'repo/rep008.html',dicc)










#	Reporte los Viernes
class Rep007(View): 

	def get(self,request,*args,**kwargs):

		# Get request
		idu = self.request.GET.get('idu')
		fd1 = self.request.GET.get('fd1')
		fh1 = self.request.GET.get('fh1')
		usr = AuthUser.objects.get(pk=self.request.user.pk)

		# Código default
		if idu == None:
			idu = usr.codigo
			#print(">> No :. cod : "+str(idu))

		# Fecha Hasta default
		if fd1 == None:
			fd2 = datetime.datetime.now()
			fd1 = "'"+str(fd2.year)+"-"+str(fd2.month)+"-01'"
			#print(">> No :. fd1 : "+str(fd1))
		if fh1 == None:
			fh2 = datetime.datetime.now()
			fh1 = "'"+str(fh2.year)+"-"+str(fh2.month)+"-"+str(fh2.day)+"'"
			#print(">> No :. fh1 : "+str(fh1))

		# Get report
		cursor = connection.cursor()
		# Reporte de incurridopor días por claborador
		qry = "CALL sp_rep007("+str(fd1)+","+str(fh1)+",'"+str(idu)+"')"
		#print("  >> qry = "+qry)
		cursor.execute(qry)
		resultado = cursor.fetchall()
		horas = 0.0
		object_list = []
		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)
			horas = horas + float(row[5])
		cursor.close()

		sfh1 = ''+fh1[9:11]+'.'+fh1[6:8]+'.'+fh1[1:5]
		
		dicc = { 
			'msj' : 'Reporte de hrs ' + usr.alias+' ' + usr.last_name + ' - '+sfh1+'.xlsx       :.       ' +str(horas)+'h. trabajadas',
			'object_list' : object_list
		}
		return render(request,'repo/rep007.html',dicc)






"""  ===================================  G R A F I C O S  =================================== """
#	Reporte de Incurrido vs disponibilidad
class Rep006(View): 

	def get(self,request,*args,**kwargs):

		# Get request
		equ = self.request.GET.get('equ')
		fecha_desde = self.request.GET.get('fd1')
		fecha_hasta = self.request.GET.get('fh1')


		# Para el matcode de clientes
		lst_equs = Equipo.objects.all()
		for equs in lst_equs:
			pass

		# Get user
		userpk = self.request.user.pk

		# Obtenemos el equipo asignado
		#print(" >> equ:"+str(equ)+"  fd1:"+str(fecha_desde)+"  fh1:"+str(fecha_hasta))
		if equ == None or equ == '' or equ == '0':
			if AuthCliente.objects.filter(idauth=userpk).exists():
				acl = AuthCliente.objects.filter(idauth=userpk).first()
				equi = acl.idcliente.equipo
			else: 
				equi = Equipo.objects.get(idequipo=1) # Toma valor inicial será uno
		else:
			equi = Equipo.objects.get(idequipo=equ)

		# Get dates default
		if fecha_desde == None:
			fh1 = datetime.datetime.now()
			fecha_desde = "'"+str(fh1.year)+"-"+str(fh1.month)+"-01'"
		if fecha_hasta == None:
			fh = datetime.datetime.now()
			cant_dias = calendar.monthrange(fh.year,fh.month)
			fecha_hasta = "'"+str(fh.year)+"-"+str(fh.month)+"-"+str(cant_dias[1])+"'"

		#print(" >> eq2:"+str(equi.pk)+"  fd1:"+str(fecha_desde)+"  fh1:"+str(fecha_hasta))
		#object_list = []		
		cursor = connection.cursor()
		qry = "CALL sp_rep006 ("+str(equi.pk)+","+str(fecha_desde)+","+str(fecha_hasta)+")"
		#print("  >> qry6 = " + qry)
		cursor.execute(qry)
		resultado = cursor.fetchall()
		cursor.close()

		lst_fe = []
		cad_za = []
		cad_zi = []
		cad_zd = []
		for row in resultado:
			ol = dict(zip([col[0] for col in cursor.description], row))
			if ol['posicion'] == 'zi':
				cad_zi.append(ol['imputacion'])
			elif ol['posicion'] == 'za':
				cad_za.append(ol['imputacion'])
			elif ol['posicion'] == 'zd':
				cad_zd.append(ol['imputacion'])
				lst_fe.append(ol['nombre'])

		dicc = {
			'msj':'Equipo '+equi.nombre+', desde '+str(fecha_desde)+" hasta "+str(fecha_hasta)+".",
			'cad_zi':cad_zi,
			'cad_za':cad_za,
			'cad_zd':cad_zd,
			'lst_fe' : lst_fe,
			'lst_equs' : lst_equs
		}
		return render(request,'repo/rep006.html',dicc)







# Reportes de totales de incurrido
class Rep005(View): 

	def get(self,request,*args,**kwargs):

		# Get request
		equ = self.request.GET.get('equ')
		fecha_desde = self.request.GET.get('fd1')
		fecha_hasta = self.request.GET.get('fh1')


		# Para el matcode de clientes
		lst_equs = Equipo.objects.all()
		for equs in lst_equs:
			pass

		# Get user
		userpk = self.request.user.pk

		# Obtenemos el equipo asignado
		#print(" >> equ:"+str(equ)+"  fd1:"+str(fecha_desde)+"  fh1:"+str(fecha_hasta))
		if equ == None or equ == '' or equ == '0':
			if AuthCliente.objects.filter(idauth=userpk).exists():
				acl = AuthCliente.objects.filter(idauth=userpk).first()
				equi = acl.idcliente.equipo
			else: 
				equi = Equipo.objects.get(idequipo=1) # Toma valor inicial será uno
		else:
			equi = Equipo.objects.get(idequipo=equ)

		# Get dates default
		if fecha_desde == None:
			fh1 = datetime.datetime.now()
			fecha_desde = "'"+str(fh1.year)+"-"+str(fh1.month)+"-01'"
		if fecha_hasta == None:
			fh = datetime.datetime.now()
			cant_dias = calendar.monthrange(fh.year,fh.month)
			fecha_hasta = "'"+str(fh.year)+"-"+str(fh.month)+"-"+str(cant_dias[1])+"'"

		#print(" >> eq2:"+str(equi.pk)+"  fd1:"+str(fecha_desde)+"  fh1:"+str(fecha_hasta))

		object_list = []		
		cursor = connection.cursor()
		cursor.execute("CALL sp_rep005 ("+str(equi.pk)+","+str(fecha_desde)+","+str(fecha_hasta)+")")
		resultado = cursor.fetchall()
		cursor.close()

		cli_nomb = []
		pet_hac  = []
		estm_esf = []
		req_hac = []
		tsk_pla = []
		tsk_eje = []
		gnt_inc = []
		etc_lst = []


		for row in resultado:
			ol = dict(zip([col[0] for col in cursor.description], row))
			cli_nomb.append(str(ol['cli_nombre']))
			pet_hac.append(ol['pet_hac'])
			estm_esf.append(ol['estm_esf'])
			req_hac.append(ol['req_hac'])
			tsk_pla.append(ol['tsk_pla'])
			tsk_eje.append(ol['tsk_eje'])
			gnt_inc.append(ol['gnt_inc'])
			etc_lst.append(ol['etc_lst'])


		cli_det = []
		cont = 0
		cad = ''
		cli_res = []


		for x in cli_nomb:
			cli = CliRes()
			cad = " data: [ { name: 'Pet.Horas Acuerdo',  y: "+str(pet_hac[cont])+",  sliced: true, selected: true }"
			cad += ",{  name: 'Estimación',  y: "+str(estm_esf[cont])+" }"
			cad += ",{  name: 'Req.Horas Acuerdo',  y: "+str(req_hac[cont])+" }"
			cad += ",{  name: 'Planificado en Task',  y: "+str(tsk_pla[cont])+" }"
			cad += ",{  name: 'Ejecutado en Task',  y: "+str(tsk_eje[cont])+" }"
			cad += ",{  name: 'Planificado en Gant',  y: "+str(gnt_inc[cont])+" }"
			cad += ",{  name: 'ETC',  y: "+str(etc_lst[cont])+" } ]"

			cli.cont = str(cont)
			cli.clie = str(x)
			cli.fd1 = str(fecha_desde)
			cli.fh1 = str(fecha_hasta)
			cli.resu = cad
			cli.pet_hac = pet_hac[cont]
			cli.estm_esf = estm_esf[cont]
			cli.req_hac = req_hac[cont]
			cli.tsk_pla = tsk_pla[cont]
			cli.tsk_eje = tsk_eje[cont]
			cli.gnt_inc = gnt_inc[cont]
			cli.etc_lst = etc_lst[cont]
			# Append
			cli_res.append(cli)

			cont += 1


		dicc = {
			'msj':'Equipo '+equi.nombre+', desde '+str(fecha_desde)+" hasta "+str(fecha_hasta)+".",
			
			'lst_equs':lst_equs,
			'cli_nomb': cli_nomb,
			'pet_hac' : pet_hac,
			'estm_esf': estm_esf,
			'req_hac' : req_hac,
			'tsk_pla' : tsk_pla,
			'tsk_eje' : tsk_eje,
			'gnt_inc' : gnt_inc,
			'cli_res' : cli_res,
			'etc_lst' : etc_lst 
		}

		return render(request,'repo/rep005.html',dicc)
	


class CliRes(models.Model):
    cont = models.CharField(max_length=4)
    clie = models.CharField(max_length=100)
    fd1 = models.CharField(max_length=10)
    fh1 = models.CharField(max_length=10)
    resu = models.CharField(max_length=300)
    pet_hac = models.FloatField()
    estm_esf = models.FloatField()
    req_hac = models.FloatField()
    tsk_eje = models.FloatField()
    gnt_inc = models.FloatField()
    etc = models.FloatField()



#  
class Graficos(View): 

	def get(self,request,*args,**kwargs):

		# Get request
		fecha_desde = self.request.GET.get('fecha_desde')
		fecha_hasta = self.request.GET.get('fecha_hasta')

		
		if fecha_desde == None:
			fh1 = datetime.datetime.now()
			fecha_desde = "'"+str(fh1.year)+"-"+str(fh1.month)+"-01'"
		if fecha_hasta == None:
			fh = datetime.datetime.now()
			cant_dias = calendar.monthrange(fh.year,fh.month)
			fecha_hasta = "'"+str(fh.year)+"-"+str(fh.month)+"-"+str(cant_dias[1])+"'"


		object_list = []		
		cursor = connection.cursor()
		cursor.execute("CALL sp_rep001 ("+str(fecha_desde)+","+str(fecha_hasta)+")")
		resultado = cursor.fetchall()

		clie = []
		hacu = []
		plan = []
		incu = []
		cant_p = []
		cant_r = []
		cant_t = []

		for row in resultado:
			ol = dict(zip([col[0] for col in cursor.description], row))
			clie.append(str(ol['cod_cliente']))
			hacu.append(ol['horas_acuerdo'])
			plan.append(ol['planificado'])
			incu.append(ol['incurrido'])
			cant_p.append(ol['cant_pet'])
			cant_r.append(ol['cant_req'])
			cant_t.append(ol['cant_task'])	
		cursor.close()

		dicc = {
			'msj':'Reporte de clientes desde '+str(fecha_desde)+" hasta "+str(fecha_hasta)+".",
			'len': ''+str(len(incu) + 1),
			'clie':clie,
			'hacu':hacu,
			'plan':plan,
			'incu':incu,
			'cant_p':cant_p,
			'cant_r':cant_r,
			'cant_t':cant_t,
		}

		return render(request,'repo/inic.html',dicc)
	





#alias	codigo	sem_1	sem_2	sem_3	sem_4	sem_5	sem_6
class Rep002(View):

	def get(self,request,*args,**kwargs):
		fecha = self.request.GET.get('fecha')
		if fecha == None:
			fh1 = datetime.datetime.now()
			ms = str(fh1.month)
			if fh1.month < 10:
				ms = '0'+str(fh1.month)
			fecha = "'"+str(fh1.year)+"-"+ms+"-01'"
		else:
			fecha = fecha[0:8]+"-01'"

		object_list = []		
		cursor = connection.cursor()
		cursor.execute("CALL sp_rep002 ("+str(fecha)+")")
		resultado = cursor.fetchall()

		col = []
		cod = []
		sem_1 = []
		sem_2 = []
		sem_3 = []
		sem_4 = []
		sem_5 = []
		sem_6 = []

		for row in resultado:
			ol = dict(zip([col[0] for col in cursor.description], row))
			col.append(str(ol['alias']))
			cod.append(ol['codigo'])
			sem_1.append(ol['sem_1'])
			sem_2.append(ol['sem_2'])
			sem_3.append(ol['sem_3'])
			sem_4.append(ol['sem_4'])
			sem_5.append(ol['sem_5'])
			sem_6.append(ol['sem_6'])	
		cursor.close()

		dicc = {
			'msj':'Reporte de de incurrido por colaborador al mes '+fecha[6:8]+'/'+fecha[1:5]+'.',
			'len': ''+str(len(col) + 1),
			'col':col,
			'cod':cod,
			'sem_1':sem_1,
			'sem_2':sem_2,
			'sem_3':sem_3,
			'sem_4':sem_4,
			'sem_5':sem_5,
			'sem_6':sem_6
		}
		return render(request,'repo/rep002.html',dicc)
	




#alias	codigo	sem_1	sem_2	sem_3	sem_4	sem_5	sem_6
class Rep003(View):

	def get(self,request,*args,**kwargs):
		anio = self.request.GET.get('anio')
		mes = self.request.GET.get('mes')

		if anio == None:
			fh1 = datetime.datetime.now()
			anio = str(fh1.year)[0:2]

		if mes == None:
			fh1 = datetime.datetime.now()
			mes = str(fh1.month)

		if len(mes) == 1:
			mes = '0'+mes

		object_list = []		
		cursor = connection.cursor()
		cursor.execute("CALL sp_rep003 ('"+str(anio)+"','"+str(mes)+"')")
		resultado = cursor.fetchall()

		clie = []
		hacu = []
		disp = []
		incu = []
		lent = 1

		for row in resultado:
			ol = dict(zip([col[0] for col in cursor.description], row))
			#print("   ->> :- "+str(ol['cliente'])+" :: ha_"+str(ol['ha'])+" | in_"+str(ol['inc'])+" | di_"+str(ol['di']))
			clie.append(str(ol['cliente']))
			hacu.append(ol['ha'])
			disp.append(ol['di'])
			incu.append(ol['inc'])
			lent += 1
		cursor.close()

		dicc = {
			'msj':'Incurrido vs Disponibilidad '+str(mes)+'/20'+str(anio)+'.',
			'clie':clie,
			'hacu':hacu,
			'disp':disp,
			'incu':incu,
			'len': lent
		}
		return render(request,'repo/rep003.html',dicc)





class Rep004(View):

	def get(self,request,*args,**kwargs):

		pet_cod = self.request.GET.get('pet_cod')
		fec_des = self.request.GET.get('fec_des')
		fec_has = self.request.GET.get('fec_has')


		pet_hac = 0.0
		tsk_pla = 0.0
		tsk_inc = 0.0
		gnt_inc = 0.0
		etc_tsk = 0.0
		etc_gnt = 0.0

		msj = "Acotamiento por fechas para petición"


		#print("   >>-----|--->> "+str(pet_cod)+" - "+str(fec_des)+" - "+str(fec_has))

		if pet_cod != None and fec_des != None and fec_has != None:

			pet_ent = Peticion.objects.get(id_pet_fenix=int(pet_cod))
			msj = 'Resumen por intervale para  '+str(pet_ent)+'.'
			
			cursor = connection.cursor()
			cursor.execute("CALL sp_rep004 ("+str(pet_cod)+","+str(fec_des)+","+str(fec_has)+")")
			resultado = cursor.fetchall()

			for row in resultado:
				dic = dict(zip([col[0] for col in cursor.description], row))
				pet_hac =  dic['pet_hac']
				tsk_pla =  dic['tsk_pla']
				tsk_inc =  dic['tsk_inc']
				gnt_inc =  dic['gnt_inc']
				etc_tsk =  dic['etc_tsk']
				etc_gnt =  dic['etc_gnt']
				print("   >> ")

			cursor.close()



		dicc = {
			'pet': msj,
			'msj':'Incurridos desde '+str(fec_des)+' hasta '+str(fec_has)+'.',
			'pet_hac' : pet_hac,
			'tsk_pla' : tsk_pla,
			'tsk_inc' : tsk_inc,
			'gnt_inc' : gnt_inc,
			'etc_tsk' : etc_tsk,
			'etc_gnt' : etc_gnt,
			'pet_cod' : pet_cod,

		}
		return render(request,'repo/rep004.html',dicc)



def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)