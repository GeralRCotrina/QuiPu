

from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View
from apps.gestion.models import Riesgo, Requerimientos, AuthUser
from apps.ries.forms import *
from django.db.models import Q
import datetime
import calendar




# ======================  R I E S G O ================

class RieCre(CreateView):
	model=Riesgo
	form_class=RiesgoForm
	template_name='ries/cre.html'
	success_url=reverse_lazy('rie_lis')


	def get_form(self, form_class=None):
		form=super(CreateView,self).get_form(form_class=self.form_class)
		form.fields["requerimiento"].queryset=Requerimientos.objects.filter(idrequerimiento=self.kwargs['pk'])
		form.fields["codigo"].initial=CrearCodigoRie()
		form.fields["responsable"].queryset=AuthUser.objects.filter(id=self.request.user.pk)
		return form

def CrearCodigoRie():
	cod = int(Riesgo.objects.last().codigo[3:7]) + 1
	n_bug = ""
	if cod < 10:
		n_bug += "RIE000"+str(cod)
	elif cod < 100:
		n_bug += "RIE00"+str(cod)
	elif cod < 1000:
		n_bug += "RIE0"+str(cod)
	else:
		n_bug += "RIE"+str(cod)
	return n_bug;


class RieLis(View):
	model=Riesgo
	template_name='ries/lis.html'

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
			if AuthCliente.objects.filter(idauth = userpk ).exists():
				asig01 = AuthCliente.objects.filter(idauth = userpk).first()
				clie = asig01.idcliente.pk
			else:
				clie = '0'
			
		#	Build date
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
			cursor.execute("CALL sp_rie_x_fecha ("+str(fecha_desde)+","+str(fecha_hasta)+",1)")
		else:
			cursor.execute("CALL sp_rie_x_fecha_1 ("+str(fecha_desde)+","+str(fecha_hasta)+","+str(clie)+",1)")
		resultado = cursor.fetchall()

		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)
		cursor.close()

		# Bluid mensaje
		msj = "Reporte de riesgos entre el "+fecha_desde+" hasta "+fecha_hasta
		if clie != '0':
			for x in (x for x in obj2 if x.idcliente == int(clie)):
				msj = msj + " en "+x.cliente

		# Build response
		dicc = { 
			'object_list':object_list,
			'obj2' : obj2,
			'msj': msj
		}
		return render(request,'ries/lis.html',dicc)





#	Riesgos por requerimiento
class RieXReq(View):
	model=Riesgo
	template_name='ries/lis.html'

	def get(self,request,*args,**kwargs):

		idr = self.request.GET.get('idr')

		# Para el matcode de clientes
		obj2 = Cliente.objects.all()
		for ob in obj2:
			pass

		from django.db import connection, transaction
		object_list = []		
		cursor = connection.cursor()
		cursor.execute("CALL sp_rie_x_req ("+str(idr)+",1)")
		resultado = cursor.fetchall()

		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)
		cursor.close()

		# Build response
		dicc = { 
			'object_list':object_list,
			'obj2' : obj2,
			'msj': "Reporte de riesgos por requerimiento"
		}
		return render(request,'ries/lis.html',dicc)



#	Riesgos por petición
class RieXPet(View):
	model=Riesgo
	template_name='ries/lis.html'

	def get(self,request,*args,**kwargs):

		idp = self.request.GET.get('idp')

		# Para el matcode de clientes
		obj2 = Cliente.objects.all()
		for ob in obj2:
			pass

		from django.db import connection, transaction
		object_list = []		
		cursor = connection.cursor()
		cursor.execute("CALL sp_rie_x_pet ("+str(idp)+",1)")
		resultado = cursor.fetchall()

		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			object_list.append(dic)
		cursor.close()

		# Build response
		dicc = { 
			'object_list': object_list,
			'obj2' : obj2,
			'msj': "Reporte de riesgos por petición"
		}
		return render(request,'ries/lis.html',dicc)






class RieEdi(UpdateView):
	model=Riesgo
	form_class=RiesgoEdiForm
	template_name='ries/cre.html'
	success_url=reverse_lazy('rie_lis') 

	def get_form(self, form_class=None):
		form=super(UpdateView,self).get_form(form_class=self.form_class)
		rie = Riesgo.objects.get(pk=self.kwargs['pk'])
		rqs = Requerimientos.objects.filter(peticion=rie.requerimiento.peticion).exclude(estado=3)
		form.fields["requerimiento"].queryset= rqs
		return form





class RieEli(DeleteView):
	model=Riesgo
	form_class=RiesgoForm
	template_name='ries/eli.html'
	success_url=reverse_lazy('rie_lis')



