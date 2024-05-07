

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View
from apps.gestion.models import Incidencia, Requerimientos
from apps.inci.forms import *

from django.db.models import Q
import datetime
import calendar



# ============ I N C I D E N C I A

class IncCre(CreateView):
	model=Incidencia
	form_class=IncidenciaForm
	template_name='inci/cre.html'
	success_url=reverse_lazy('inc_lis')

	def get_form(self, form_class=None):
		form=super(CreateView,self).get_form(form_class=self.form_class)
		form.fields["requerimiento"].queryset=Requerimientos.objects.filter(idrequerimiento=self.kwargs['pk'])
		form.fields["num_bug"].initial=CrearCodigoInc(self.kwargs['pk'])
		form.fields["idetificador"].queryset=AuthUser.objects.filter(id=self.request.user.pk)
		return form

# 	Creams el codigo del bug
def CrearCodigoInc(idr):
	n_bug = Requerimientos.objects.get(idrequerimiento=idr).peticion.cliente.codigo
	n_bug = n_bug+'_'
	ultm_cod = Incidencia.objects.filter(num_bug__contains=(n_bug)).last().num_bug
	tm1 = len(ultm_cod)
	tm2 = tm1 - 4

	cod = int(ultm_cod[tm2:tm1]) + 1
	if cod < 10:
		n_bug += "BUG000"+str(cod)
	elif cod < 100:
		n_bug += "BUG00"+str(cod)
	elif cod < 1000:
		n_bug += "BUG0"+str(cod)
	else:
		n_bug += "BUG"+str(cod)
	return n_bug




class IncLis(View):
	template_name='inci/lis.html'

	def get(self,request,*args,**kwargs):
		
		clie = self.request.GET.get('clie')
		fecha_desde = self.request.GET.get('fecha_desde')
		fecha_hasta = self.request.GET.get('fecha_hasta')

		# Para el matcode de clientes
		obj2 = Cliente.objects.all()
		for ob in obj2:
			pass

		# Obtenemos el cliente para el filtro personalizado
		# Solo si la consulta no viene desde el listado
		# y si el usuario está asignado a algún cliente
		if clie == None:
			userpk = self.request.user.pk
			if AuthCliente.objects.filter( idauth = userpk ).exists():
				asig01 = AuthCliente.objects.filter(idauth = userpk ).first()
				clie = asig01.idcliente.pk
			else:
				clie = '0'
		
		# Build date
		if fecha_desde == None:
			fh1 = datetime.datetime.now()
			fecha_desde = "'"+str(fh1.year)+"-"+str(fh1.month)+"-01'"
		if fecha_hasta == None:
			fh = datetime.datetime.now()
			cant_dias = calendar.monthrange(fh.year,fh.month)
			fecha_hasta = "'"+str(fh.year)+"-"+str(fh.month)+"-"+str(cant_dias[1])+"'"

		from django.db import connection, transaction
		object_list = []		
		cursor = connection.cursor()
		if clie == '0':
			cursor.execute("CALL sp_inc_x_fecha ("+str(fecha_desde)+","+str(fecha_hasta)+",1)")
		else:
			cursor.execute("CALL sp_inc_x_fecha_1 ("+str(fecha_desde)+","+str(fecha_hasta)+","+str(clie)+",1)")

		
		resultado = cursor.fetchall()

		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)
		cursor.close()


		# Bluid mensaje
		msj = "Reporte de incidencias entre el "+fecha_desde+" hasta "+fecha_hasta
		if clie != '0':
			for x in (x for x in obj2 if x.idcliente == int(clie)):
				msj = msj + " en "+x.cliente

		dicc2 = { 
			'object_list': object_list,
			'msj': msj,
			"obj2": obj2
		}
		return render(request,'inci/lis.html', dicc2)





#	Incidencias por requerimiento.
class IncXReq(View):

	template_name='inci/lis.html'

	def get(self,request,*args,**kwargs):

		idr = self.request.GET.get('idr')

		# Para el matcode de clientes
		obj2 = Cliente.objects.all()
		for ob in obj2:
			pass
		
		from django.db import connection, transaction
		object_list = []		
		cursor = connection.cursor()
		cursor.execute("CALL sp_inc_x_req ("+str(idr)+",1)")
		resultado = cursor.fetchall()

		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)
		cursor.close()

		dicc2 = { 
			'object_list': object_list,
			'msj': "Reporte de incidencias por requerimiento ",
			"obj2": obj2
		}
		return render(request,'inci/lis.html', dicc2)



#	Incidencias por requerimiento.
class IncXPet(View):

	template_name='inci/lis.html'

	def get(self,request,*args,**kwargs):

		idp = self.request.GET.get('idp')

		# Para el matcode de clientes
		obj2 = Cliente.objects.all()
		for ob in obj2:
			pass
		
		from django.db import connection, transaction
		object_list = []		
		cursor = connection.cursor()
		cursor.execute("CALL sp_inc_x_pet ("+str(idp)+",1)")
		resultado = cursor.fetchall()

		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)
		cursor.close()

		dicc2 = { 
			'object_list': object_list,
			'msj': "Reporte de incidencias por petición ",
			"obj2": obj2
		}
		return render(request,'inci/lis.html', dicc2)



class IncEdi(UpdateView):
	model=Incidencia
	form_class=IncidenciaEdiForm
	template_name='inci/cre.html'
	success_url=reverse_lazy('inc_lis') 

	def get_form(self, form_class=None):
		form=super(UpdateView,self).get_form(form_class=self.form_class)
		inc = Incidencia.objects.get(pk=self.kwargs['pk'])
		rqs = Requerimientos.objects.filter(peticion=inc.requerimiento.peticion).exclude(estado=3)
		form.fields["requerimiento"].queryset= rqs
		return form



class IncEli(DeleteView):
	model=Incidencia
	form_class=IncidenciaForm
	template_name='inci/eli.html'
	success_url=reverse_lazy('inc_lis')

class IncExp(View):

	def get(self,request,*args,**kwargs):
		cod_col = self.request.GET.get('cod_col')
		id_cli = self.request.GET.get('id_cli')

		cad = ''

		if cod_col:
			#	Consulta por Cliente y responsable.
			cad ="CALL sp_inc_exp01 ("+str(id_cli)+","+str(cod_col)+")"
		else:
			#	Consulta solo por Cliente y responsable.
			cad = "CALL sp_inc_exp02 ("+str(id_cli)+")"

		from django.db import connection, transaction
		print(cad)

		object_list = []		
		cursor = connection.cursor()
		cursor.execute(cad)
		resultado = cursor.fetchall()

		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)
		cursor.close()

		dicc = { 'object_list':object_list,
				 'msj': "No se encontró data para exportar." }

		return render(request,'inci/exp.html',dicc)




