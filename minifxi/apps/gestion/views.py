from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View
from apps.gestion.models import *
from apps.gestion.forms import *
from apps.gestion.gv_view import *

import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django.contrib import messages
from django.db.models import Q


#_______________________________ I N I C I O - - - P A N E L_____________#
class panel(View):

	def get(self,request,*args,**kwargs):
		# Consultamos el SP
		col_cod = request.GET.get('col_cod')
		fech    = request.GET.get('fech')

		msj =""  #  Resumen para 
		alias = ''
		hoy_str = ''
		hoy_dat = '' 
		idr = '1'

		if  fech!= None:
			hoy_str = fech
		else:
			hoy_dat = datetime.datetime.now()

			#hoy_str = ""+str(hoy_dat.year)+"-"+str(hoy_dat.month)+"-"+str(hoy_dat.day)+""
			hoy_str = ""+str(hoy_dat.year)+"-"
			if hoy_dat.month < 10:
				hoy_str = "" + hoy_str + "0"+ str(hoy_dat.month)+"-"
			else:
				hoy_str = "" + hoy_str + "" + str(hoy_dat.month)+"-"
			if hoy_dat.day < 10:
				hoy_str = "" + hoy_str + "0"+ str(hoy_dat.day)+""
			else:
				hoy_str = "" + hoy_str + "" + str(hoy_dat.day)+""



		if col_cod != None and col_cod != '' :
			if AuthUser.objects.filter(codigo=int(col_cod)).exists():
				idr1 = AuthUser.objects.filter(codigo=int(col_cod)).first()
				idr  = idr1.pk
				col_cod = idr1.codigo
				alias = idr1.alias
			else:
				idr = request.user.pk
				msj = "Codigo "+col_cod+" no existe." 
		else:
			idr = request.user.pk
			cola = AuthUser.objects.get(pk=idr)
			col_cod = cola.codigo
			alias = cola.alias
		
		tot_pla = 0.0
		tot_inc = 0.0
		tot_etc = 0.0


		# Get TASK FASE DE ACTIVIDAD
		obj_est = PeticionEstado.objects.all()
		#cad = ''
		for pe in obj_est:
			pass


		#print(" >> "+str(hoy_str)+" - "+str(col_cod))

		#   TAREAS DE HOY
		obj_lst = []
		obj_lst2 = []
		from django.db import connection, transaction
		cursor = connection.cursor()	


		#REQUES
		cursor.execute("CALL sp_panel_req("+str(idr)+")")
		resultado = cursor.fetchall()
		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			obj_lst2.append(dic)
 


		#  TASK
		cursor.execute("CALL sp_panel_tsk('"+hoy_str+"',"+str(idr)+")") # CONSULTA FANTASMA NECESARIA
		cursor.execute("CALL sp_panel_tsk('"+hoy_str+"',"+str(idr)+")")
		resultado = cursor.fetchall()
		for row in resultado:
			dic = dict(zip([col[0] for col in cursor.description], row))
			obj_lst.append(dic)
			if dic['tsk_epl'] != None:
				tot_pla = float(tot_pla) + float(dic['tsk_epl'])
			if dic['tsk_eej'] != None:
				tot_inc = float(tot_inc) + float(dic['tsk_eej'])
			if dic['tsk_etc'] != None:
				tot_etc = float(tot_etc) + float(dic['tsk_etc'])
		cursor.close()


		dicc = {  
			"obj_lst"  : obj_lst,
			"obj_lst2" : obj_lst2,
			'msj': msj + alias +"    ["+ str(col_cod)+ ']       '+ hoy_str+ "." ,
			'msj2': " Mis últimos 100 requerimientos",
			'tot_pla' : tot_pla,
			'tot_inc' : tot_inc,
			'tot_etc' : tot_etc,
			'obj_est' : obj_est
		}


		return render(request,'inicio.html',dicc)







def mylogin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('panel')
        else:
            messages.info(request, '¡Error intente nuevamente!')
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')




def ErrorPage(request):
	dicc={
		'msj':'error de los que sea.'
	}

	return render(request,'Err.html',dicc)


# CREAR CONTRASEÑA DE COLABORADOR
# col_set_pas
class CambPass1(View):
	def get(self,request,*args,**kwargs):
		rpta = PassChange(self.request.user.pk,self.request.GET.get('cod'),self.request.GET.get('pss'))
		return HttpResponse(rpta)
"""
'OK'  = Ok
'nco' = no existe código
"""
def PassChange(ussr,cod,pss):
	rpta = 'Ok'
	ess = False
	# Validamos el permiso
	if AuthUserUserPermissions.objects.filter( Q(user=ussr) & Q(permission=204) ).exists():
		ess = True
	elif AuthUserUserPermissions.objects.filter( Q(user=ussr) & Q(permission=203) ).exists():
		ess = True
	else:
		rpta = 'Err'
		print("  >> rpta:  Err ")
	if ess:
		#usr1 = AuthUser.objects.get(codigo=cod)
		if AuthUser.objects.filter(codigo=cod).exists() :
			usr = AuthUser.objects.filter(codigo=cod).first()
			u = User.objects.get(pk=usr.pk)
			u.set_password(pss)
			u.save()
		else:
			rpta = 'nco'
	return rpta 



# CAMBIO CONTRASEÑA DE COLABORADOR
class CambPass2(View):

	def get(self,request,*args,**kwargs):

		rpta = "Inv"
		prmr = self.request.GET.get('prmr')
		sgnd = self.request.GET.get('sgnd')
		ussr = self.request.user
		#print("  >> ps1:"+str(prmr)+"  >> ps2:"+str(sgnd))
		user = authenticate(request, username=ussr, password=sgnd)
		if user is not None:
			u=User.objects.get(pk=ussr.pk)
			u.set_password(prmr)
			u.save()
			rpta = 'Ok'
		else:
			print("  >> err")
		return HttpResponse(rpta)







#===================================  S F  ===================================#

class ActSF(View):
	def get(self, request, *args, **kwargs):
		ide = self.request.GET.get('ide')
		tip = self.request.GET.get('tip')
		rpta = '9'
		if tip == 'i':
			elm=Incidencia.objects.get(idincidencia =int(ide))
		elif tip == 'r':
			elm=Riesgo.objects.get(idriesgo =int(ide))
		elif tip == 'd':
			elm=Dudas.objects.get(iddudas =int(ide))
		else:
			print("  >> Err view")


		if elm.subida_a_fenix == '1':
			elm.subida_a_fenix = '0';
			elm.save();
			rpta = '0'
		elif elm.subida_a_fenix == '0' or elm.subida_a_fenix == '' :
			elm.subida_a_fenix = '1';
			elm.save();
			rpta = '1'
		else:
			rpta = '9'
		return HttpResponse(rpta)









"""  =================================== E S T A T U S =================================== """



"""  ================================  P E T I C I O N =================================== """



"""  ============================= R E Q U E R I M  I E N T O =============================== """



"""  ===================================== T A S K =================================== """



"""  =====================================  T E A M =================================== """






class ColCre(CreateView):
	model=AuthUser
	form_class=AuthUserForm
	template_name='team/col/cre.html'
	success_url=reverse_lazy('col_lis')

	def post(self,request,*args,**kwargs):
		aut = AuthUser()
		aut.username=self.request.POST.get('username')
		aut.codigo=self.request.POST.get('codigo')
		aut.alias=self.request.POST.get('alias')
		aut.first_name=self.request.POST.get('first_name')
		aut.last_name=self.request.POST.get('last_name')
		aut.email=self.request.POST.get('email')
		aut.categoria= ColCategoria.objects.get(pk=int(self.request.POST.get('categoria')))
		if	self.request.POST.get('pais') != '':
			aut.pais=Pais.objects.get(pk=int(self.request.POST.get('pais')))
		else:
			aut.pais=Pais.objects.get(pk=1)
		aut.dni=self.request.POST.get('dni')
		aut.foto_perfil=self.request.POST.get('foto_perfil')
		aut.sexo=self.request.POST.get('sexo')
		aut.celular=self.request.POST.get('celular')
		aut.telefono=self.request.POST.get('telefono')
		if self.request.POST.get('fecha_nacimiento') != '':
			aut.fecha_nacimiento=self.request.POST.get('fecha_nacimiento')
		aut.save()
		# Create user
		rpta = PassChange(self.request.user.pk,aut.codigo,aut.codigo)
		return redirect('col_lis')
		



class ColLis2(ListView):
	model=AuthUser
	template_name='team/col/lis.html'



class ColLis(ListView):
	model=AuthUser
	template_name='team/col/lis.html'

	def get(self, request, *args, **kwargs):
		#self.object = None
		object_list = []

		# Get 1° & last days
		ArrR = ObtUltDiaDelMes(str(datetime.datetime.now().year),str(datetime.datetime.now().month))

		if AuthCliente.objects.filter(idauth=self.request.user.pk).exists():
			idcli = AuthCliente.objects.filter(idauth=self.request.user.pk).first()
				
			from django.db import connection#, transaction
			cursor = connection.cursor()
			#cursor.execute("CALL sp_001_usr_x_equi ("+str(idcli.idcliente.equipo.pk)+")")
			cursor.execute("CALL sp_002_usr_x_equi ("+str(idcli.idcliente.equipo.pk)+" , '"+ArrR[0]+"', '"+ArrR[1]+"')")
			resultado = cursor.fetchall()
			for row in resultado:
				dic = dict(zip([col[0] for col in cursor.description], row))
				object_list.append(dic) 
				#print('  >> ColLis: '+str(dic['alias']))
			cursor.close()

		# Build response
		dicc = { 
			'object_list': object_list
		}
		
		return render(request,self.template_name,dicc)



class ColEdi(UpdateView):
	model=AuthUser
	form_class=AuthUserForm
	template_name='team/col/cre.html'
	success_url=reverse_lazy('col_lis') 

class ColEli(DeleteView):
	model=AuthUser
	form_class=AuthUserForm
	template_name='team/col/eli.html'
	success_url=reverse_lazy('col_lis')


# Consulta al cargar la página 
class ColFot(View):

	def get(self, request, *args, **kwargs):

		# Get User ( foto / código )
		usr = AuthUser.objects.get(pk=self.request.user.pk)
		fto = str(usr.foto_perfil)
		if fto == "":
			fto="Inv"		

		# Get cliente		
		# Obtenemos el cliente para el filtro personalizado
		ahc = MiCliente(self.request.user.pk)
		
		# Obtenemos el equipo asignado
		equi = MiEquipo(ahc)
		equ = equi.pk


		# Diccionario a enviar
		#  dic = '{ "foto":"" , "Codigo" : "" , "Cliente" : "" }'
		dic =          '{ "Foto" : "'+ fto + '" ,'
		dic = '' + dic +' "Codigo" : "'+ str(usr.codigo) + '" ,'
		dic = '' + dic +' "Cliente" : "' + str(ahc) + '" , '
		dic = '' + dic +' "Equipo" : "' + str(equ) + '" '
		dic = '' + dic +' } '

		#print(" >>> " + dic)
		return HttpResponse(dic)



class ColEdiF(UpdateView):
	model=AuthUser
	form_class=AuthUserFormUF
	template_name='team/col/edif.html'
	success_url=reverse_lazy('panel') 


class ColEdiU(UpdateView):
	model=AuthUser
	form_class=AuthUserFormU
	template_name='team/col/cre.html'
	success_url=reverse_lazy('panel') 




# ============ T I P O  D E  I N C

class IncTipCre(CreateView):
	model=IncTipo
	form_class=IncTipoForm
	template_name='recu/inc_t/cre.html'
	success_url=reverse_lazy('inc_t_lis')

class IncTipLis(ListView):
	model=IncTipo
	template_name='recu/inc_t/lis.html'

class IncTipEdi(UpdateView):
	model=IncTipo
	form_class=IncTipoForm
	template_name='recu/inc_t/cre.html'
	success_url=reverse_lazy('inc_t_lis') 

class IncTipEli(DeleteView):
	model=IncTipo
	form_class=IncTipoForm
	template_name='recu/inc_t/eli.html'
	success_url=reverse_lazy('inc_t_lis')



# ============ I N C   E N C  E N

class IncEECre(CreateView):
	model=IncLocalizadaEn
	form_class=IncLocalizadaEnForm
	template_name='recu/inc_ee/cre.html'
	success_url=reverse_lazy('inc_ee_lis')

class IncEELis(ListView):
	model=IncLocalizadaEn
	template_name='recu/inc_ee/lis.html'

class IncEEEdi(UpdateView):
	model=IncLocalizadaEn
	form_class=IncLocalizadaEnForm
	template_name='recu/inc_ee/cre.html'
	success_url=reverse_lazy('inc_ee_lis') 

class IncEEEli(DeleteView):
	model=IncLocalizadaEn
	form_class=IncLocalizadaEnForm
	template_name='recu/inc_ee/eli.html'
	success_url=reverse_lazy('inc_ee_lis')


# ============ P E T   E S T A D O

class PetEstCre(CreateView):
	model=PeticionEstado
	form_class=PeticionEstadoForm
	template_name='recu/pet_est/cre.html'
	success_url=reverse_lazy('pet_est_lis')

class PetEstLis(ListView):
	model=PeticionEstado
	template_name='recu/pet_est/lis.html'

class PetEstEdi(UpdateView):
	model=PeticionEstado
	form_class=PeticionEstadoForm
	template_name='recu/pet_est/cre.html'
	success_url=reverse_lazy('pet_est_lis') 

class PetEstEli(DeleteView):
	model=PeticionEstado
	form_class=PeticionEstadoForm
	template_name='recu/pet_est/eli.html'
	success_url=reverse_lazy('pet_est_lis')




# ============ D U D   F A S

class DudFLCre(CreateView):
	model=DudasFaseLoc
	form_class=DudasFaseLocForm
	template_name='recu/dud_fl/cre.html'
	success_url=reverse_lazy('dud_fl_lis')

class DudFLLis(ListView):
	model=DudasFaseLoc
	template_name='recu/dud_fl/lis.html'


class DudFLEdi(UpdateView):
	model=DudasFaseLoc
	form_class=DudasFaseLocForm
	template_name='recu/dud_fl/cre.html'
	success_url=reverse_lazy('dud_fl_lis') 

class DudFLEli(DeleteView):
	model=DudasFaseLoc
	form_class=DudasFaseLocForm
	template_name='recu/dud_fl/eli.html'
	success_url=reverse_lazy('dud_fl_lis')


#DudasFaseLocForm




# ============ D U D    R E L

class DudRACre(CreateView):
	model=DudasRelalivaA
	form_class=DudasRelalivaAForm
	template_name='recu/dud_ra/cre.html'
	success_url=reverse_lazy('dud_ra_lis')

class DudRALis(ListView):
	model=DudasRelalivaA
	template_name='recu/dud_ra/lis.html'

class DudRAEdi(UpdateView):
	model=DudasRelalivaA
	form_class=DudasRelalivaAForm
	template_name='recu/dud_ra/cre.html'
	success_url=reverse_lazy('dud_ra_lis') 

class DudRAEli(DeleteView):
	model=DudasRelalivaA
	form_class=DudasRelalivaAForm
	template_name='recu/dud_ra/eli.html'
	success_url=reverse_lazy('dud_ra_lis')

#DudasRelalivaAForm



# ================== D U D A S   ====================#


# ============ I N C I D E N C I A ====================#



# ======================  R I E S G O ================



# ======================  R I E   C A T ================

class RieCatCre(CreateView):
	model=RiesgoCategoria
	form_class=RiesgoCategoriaForm
	template_name='recu/rie_cat/cre.html'
	success_url=reverse_lazy('rie_cat_lis')

class RieCatLis(ListView):
	model=RiesgoCategoria
	template_name='recu/rie_cat/lis.html'

class RieCatEdi(UpdateView):
	model=RiesgoCategoria
	form_class=RiesgoCategoriaForm
	template_name='recu/rie_cat/cre.html'
	success_url=reverse_lazy('rie_cat_lis') 

class RieCatEli(DeleteView):
	model=RiesgoCategoria
	form_class=RiesgoCategoriaForm
	template_name='recu/rie_cat/eli.html'
	success_url=reverse_lazy('rie_cat_lis')


#  ===================================  G R A F I C O S  =================================== #




# ====================== D O M I N I O =======
class DomCre(CreateView):
	model=Dominio
	form_class=DominioForm
	template_name='mant/dom/cre.html'
	success_url=reverse_lazy('dom_lis')

class DomLis(ListView):
	model=Dominio
	template_name='mant/dom/lis.html'

class DomEdi(UpdateView):
	model=Dominio
	form_class=DominioForm
	template_name='mant/dom/cre.html'
	success_url=reverse_lazy('dom_lis') 

class DomEli(DeleteView):
	model=Dominio
	form_class=DominioForm
	template_name='mant/dom/eli.html'
	success_url=reverse_lazy('dom_lis')



# ====================== E Q U I P O  =======
class EquCre(CreateView):
	model=Equipo
	form_class=EquipoForm
	template_name='mant/equ/cre.html'
	success_url=reverse_lazy('equ_lis')

class EquEdi(UpdateView):
	model=Equipo
	form_class=EquipoForm
	template_name='mant/equ/cre.html'
	success_url=reverse_lazy('equ_lis') 

class EquEli(DeleteView):
	model=Equipo
	form_class=EquipoForm
	template_name='mant/equ/eli.html'
	success_url=reverse_lazy('equ_lis')

 

class EquLis(View):
	model=Equipo
	template_name='mant/equ/lis.html'

	def get(self, request, *args, **kwargs):
		object_list = Equipo.objects.all()
		lst_cli = Cliente.objects.filter()

		dicc = {
			'object_list': object_list,
			'lst_cli':lst_cli
		}
		return render(request,self.template_name,dicc)





# Devuelve el detalle de los clientes asociados al equipo
class EquDetLis(View):

	def get(self, request, *args, **kwargs):
		json = '{"0":'
		ide = self.request.GET.get('ide')
		if ide == "" or ide == None: 
			json += '"Nee"}'	
		else:
			if EquiDetalle.objects.filter(idequipo=int(ide)).exists():
				json += '"Ok"'	
				lst_equ_det = EquiDetalle.objects.filter(idequipo=int(ide))

				cont = 0
				for x in lst_equ_det:
					cont += 1
					json += ',"'+str(cont)+'":"'+str(x.pk)+''
					json += ','+str(x.idcliente.codigo)+''
					json += ','+str(x.idcliente.cliente)+''
					json += ','+str(x.idcliente.idpais.pais)+''
					json += ','+str(x.creado_el)+''
					json += ','+str(x.creador.username)+''
					json += ','+str(x.estado)+'"'
				json += '}'

			else:
				json += '"Ned"}'	

		#print(" >>> " + json)
		return HttpResponse(json)
"""
Nee : No existe equipo
Ned : No existe detalle
"""



class EquDetCre(View):

	def get(self, request, *args, **kwargs):
		ide = self.request.GET.get('ide')
		idc = self.request.GET.get('idc')
		json = '{"0":'
		#print(" >> ide:"+str(ide)+"   idc:"+str(idc))
		if Cliente.objects.filter(idcliente=idc).exists():
			cli = Cliente.objects.get(pk=idc)

			if Equipo.objects.filter(idequipo=int(ide)).exists():
				equ = Equipo.objects.get(pk=int(ide))

				if EquiDetalle.objects.filter( Q(idcliente=cli) & Q(idequipo=equ) ).filter():
					json += '"Yex"}'

				else:
					json += '"Ok"'
					edet = EquiDetalle()
					edet.idequipo = Equipo.objects.get(pk=int(ide))
					edet.idcliente = Cliente.objects.get(pk=int(idc))
					edet.creador = AuthUser.objects.get(pk=self.request.user.pk)
					edet.creado_el = datetime.datetime.now()
					edet.estado = 1
					edet.save()
					# Set json {}
					json += ',"2":"'+str(edet.pk)+''
					json += ','+str(edet.idcliente.codigo)+''
					json += ','+str(edet.idcliente.cliente)+''
					json += ','+str(edet.idcliente.idpais.pais)+''
					json += ','+str(edet.creado_el.year)+'-'+str(edet.creado_el.month)+'-'+str(edet.creado_el.day)+''
					json += ','+str(edet.creador.username)+''
					json += ','+str(edet.estado)+'"}'

			else:
				json += '"Nee"}'
		else:
			json += '"Nec"}'

		#print("  >> "+json)
		return HttpResponse(json)
"""
	Nec : No existe cliente					
	Nee : No existe equipo
	Yex : Ya existe		
"""



class EquDetEli(View):

	def get(self, request, *args, **kwargs):
		idec = self.request.GET.get('idec')
		json = '{"0":'

		if EquiDetalle.objects.filter(idequi_detalle=int(idec)).exists():
			edet = EquiDetalle.objects.get(pk=int(idec))
			json += '"Ok","2":"'+str(edet.pk)+'"}'
			edet.delete()

		else:
			json += '"Ned"}'

		return HttpResponse(json)
"""
	Ned : No existe detalle	
"""







# ====================== C L I E N T E  =======
class CliCre(CreateView):
	model=Cliente
	form_class=ClienteForm
	template_name='mant/cli/cre.html'
	success_url=reverse_lazy('cli_lis')

class CliLis(ListView):
	model=Cliente
	template_name='mant/cli/lis.html'

class CliEdi(UpdateView):
	model=Cliente
	form_class=ClienteForm
	template_name='mant/cli/cre.html'
	success_url=reverse_lazy('cli_lis') 

class CliEli(DeleteView):
	model=Cliente
	form_class=ClienteForm
	template_name='mant/cli/eli.html'
	success_url=reverse_lazy('cli_lis')



class CliLis2(ListView):
	model=Cliente
	template_name='mant/cli/lis.html'

	def get(self,request,*args,**kwargs):
		equ = self.request.GET.get('equ')
		lst_cli = Cliente.objects.filter(equipo=int(equ))
		dicc = {  'object_list' : lst_cli }
		return render(request,self.template_name,dicc)
 


# ====================== P A I S  =======
class PaiCre(CreateView):
	model=Pais
	form_class=PaisForm
	template_name='mant/pai/cre.html'
	success_url=reverse_lazy('pai_lis')

class PaiLis(ListView):
	model=Pais
	template_name='mant/pai/lis.html'

class PaiEdi(UpdateView):
	model=Pais
	form_class=PaisForm
	template_name='mant/pai/cre.html'
	success_url=reverse_lazy('pai_lis') 

class PaiEli(DeleteView):
	model=Pais
	form_class=PaisForm
	template_name='mant/pai/eli.html'
	success_url=reverse_lazy('pai_lis')






#  ===============  A U T H   C L I E N T E  ========

class AuthCCre(CreateView):
	model=AuthCliente
	form_class=AuthClienteForm
	template_name='mant/au_c/cre.html'
	success_url=reverse_lazy('au_c_lis')
 
class AuthCLis(ListView):
	model=AuthCliente
	template_name='mant/au_c/lis.html'

	def get(self,request,*args,**kwargs):
		req_lst = AuthCliente.objects.all().order_by('idcliente', 'fecha_alta')
		dicc = {  'object_list' : req_lst }
		return render(request,self.template_name,dicc)





class AuthCEdi(UpdateView):
	model=AuthCliente
	form_class=AuthClienteEdiForm
	template_name='mant/au_c/cre.html'
	success_url=reverse_lazy('au_c_lis') 

class AuthCEli(DeleteView):
	model=AuthCliente
	form_class=AuthClienteForm
	template_name='mant/au_c/eli.html'
	success_url=reverse_lazy('au_c_lis')






# ====================== p r i o r i d a d  =======
class PrioCre(CreateView):
	model=ReqPrioridad
	form_class=ReqPrioridadForm
	template_name='recu/prio/cre.html'
	success_url=reverse_lazy('prio_lis')

class PrioLis(ListView):
	model=ReqPrioridad
	template_name='recu/prio/lis.html'

class PrioEdi(UpdateView):
	model=ReqPrioridad
	form_class=ReqPrioridadForm
	template_name='recu/prio/cre.html'
	success_url=reverse_lazy('prio_lis') 

class PrioEli(DeleteView):
	model=ReqPrioridad
	form_class=ReqPrioridadForm
	template_name='recu/prio/eli.html'
	success_url=reverse_lazy('prio_lis')






# ====================== M Ó D U L O S   S A P   ======= #
class ModuCre(CreateView):
	model=ModulosSap
	form_class=ModulosSapForm
	template_name='recu/modu/cre.html'
	success_url=reverse_lazy('modu_lis')

class ModuLis(ListView):
	model=ModulosSap
	template_name='recu/modu/lis.html'

class ModuEdi(UpdateView):
	model=ModulosSap
	form_class=ModulosSapForm
	template_name='recu/modu/cre.html'
	success_url=reverse_lazy('modu_lis') 

class ModuEli(DeleteView):
	model=ModulosSap
	form_class=ModulosSapForm
	template_name='recu/modu/eli.html'
	success_url=reverse_lazy('modu_lis')







# ===========            R E Q   C R I T I C I D A D             ============ #
class ReqCriCre(CreateView):
	model=ReqCriticidad
	form_class=ReqCriticidadForm
	template_name='recu/req_cri/cre.html'
	success_url=reverse_lazy('req_cri_lis')

class ReqCriLis(ListView):
	model=ReqCriticidad
	template_name='recu/req_cri/lis.html'

class ReqCriEdi(UpdateView):
	model=ReqCriticidad
	form_class=ReqCriticidadForm
	template_name='recu/req_cri/cre.html'
	success_url=reverse_lazy('req_cri_lis') 

class ReqCriEli(DeleteView):
	model=ReqCriticidad
	form_class=ReqCriticidadForm
	template_name='recu/req_cri/eli.html'
	success_url=reverse_lazy('req_cri_lis')







# ===========            I N P U T   F I N A L   P E T             ============ # 
class PetInpFCre(CreateView):
	model=PeticionInputFinal
	form_class=PeticionInputFinalForm
	template_name='recu/pet_inpf/cre.html'
	success_url=reverse_lazy('pet_inpf_lis')

class PetInpFLis(ListView):
	model=PeticionInputFinal
	template_name='recu/pet_inpf/lis.html'

class PetInpFEdi(UpdateView):
	model=PeticionInputFinal
	form_class=PeticionInputFinalForm
	template_name='recu/pet_inpf/cre.html'
	success_url=reverse_lazy('pet_inpf_lis') 

class PetInpFEli(DeleteView):
	model=PeticionInputFinal
	form_class=PeticionInputFinalForm
	template_name='recu/pet_inpf/eli.html'
	success_url=reverse_lazy('pet_inpf_lis')







# ===========        C A L I D A D   D E L    I N P U T       ============ # 
class ReqCalInputCre(CreateView):
	model=ReqCalidadInput
	form_class=ReqCalidadInputForm
	template_name='recu/req_cal/cre.html'
	success_url=reverse_lazy('req_cal_lis')

class ReqCalInputLis(ListView):
	model=ReqCalidadInput
	template_name='recu/req_cal/lis.html'

class ReqCalInputEdi(UpdateView):
	model=ReqCalidadInput
	form_class=ReqCalidadInputForm
	template_name='recu/req_cal/cre.html'
	success_url=reverse_lazy('req_cal_lis') 

class ReqCalInputEli(DeleteView):
	model=ReqCalidadInput
	form_class=ReqCalidadInputForm
	template_name='recu/req_cal/eli.html'
	success_url=reverse_lazy('req_cal_lis')







# ===========            I N P U T   F I N A L   P E T             ============ # 
class ReqInpFCre(CreateView):
	model=ReqInputFinal
	form_class=ReqInputFinalForm
	template_name='recu/req_inpf/cre.html'
	success_url=reverse_lazy('req_inpf_lis')

class ReqInpFLis(ListView):
	model=ReqInputFinal
	template_name='recu/req_inpf/lis.html'

class ReqInpFEdi(UpdateView):
	model=ReqInputFinal
	form_class=ReqInputFinalForm
	template_name='recu/req_inpf/cre.html'
	success_url=reverse_lazy('req_inpf_lis') 

class ReqInpFEli(DeleteView):
	model=ReqInputFinal
	form_class=ReqInputFinalForm
	template_name='recu/req_inpf/eli.html'
	success_url=reverse_lazy('req_inpf_lis')














# =========================  H A R D C O D E  ===================== #

# Crea Hardcode y devuelve los datos de la creación
class HrdSvd(View):

	def get(self,request,*args,**kwargs):

		#  Get request
		json = '{"0":'

		# Guardamos el nuevo harcode
		n_hrd = Hardcode()
		n_hrd.app = self.request.GET.get('app')
		n_hrd.asp = self.request.GET.get('asp')
		n_hrd.typcon = self.request.GET.get('typcon')
		n_hrd.consum = self.request.GET.get('consum')
		n_hrd.item = self.request.GET.get('item')
		n_hrd.val01 = self.request.GET.get('val01')
		n_hrd.val02 = self.request.GET.get('val02')
		n_hrd.val03 = self.request.GET.get('val03')
		n_hrd.save()

		# Creamos el request
		json += '"ok",'
		json += '"id":"'+str(n_hrd.pk)+'",'
		json += '"app":"'+str(n_hrd.app)+'",'
		json += '"asp":"'+str(n_hrd.asp)+'",'
		json += '"typcon":"'+str(n_hrd.typcon)+'",'
		json += '"consum":"'+str(n_hrd.consum)+'",'
		json += '"item":"'+str(n_hrd.item)+'",'
		json += '"val01":"'+str(n_hrd.val01)+'",'
		json += '"val02":"'+str(n_hrd.val02)+'",'
		json += '"val03":"'+str(n_hrd.val03)+'" }'

		#print("  >>"+json)
		return HttpResponse(json)



#  Elimina el Hardcode y devuelve todo su contenido
class HrdRmv(View):

	def get(self,request,*args,**kwargs):
		json = '{"0":'
		idh = self.request.GET.get('idh')

		if  Hardcode.objects.filter(id=idh).exists():
			# Si existe guardamos los datos a devolver
			hrd = Hardcode.objects.get(id=idh)

			json += '"ok","app":"'+str(hrd.app)+'",'
			json += '"asp":"'+str(hrd.asp)+'",'
			json += '"typcon":"'+str(hrd.typcon)+'",'
			json += '"consum":"'+str(hrd.consum)+'",'
			json += '"item":"'+str(hrd.item)+'",'
			json += '"val01":"'+str(hrd.val01)+'",'
			json += '"val02":"'+str(hrd.val02)+'",'
			json += '"val03":"'+str(hrd.val03)+'" }'
			# Y eliminamos
			hrd.delete()
		else:
			json += '"Noe"}'

		#print("  >>"+json)
		return HttpResponse(json)

"""
	Noe : Error, no encontrado
"""



"""
class Hardcode(models.Model):
    app = models.CharField(max_length=5)
    asp = models.CharField(max_length=5)
    typcon = models.CharField(max_length=5)
    consum = models.CharField(max_length=5)
    item = models.CharField(max_length=10, blank=True, null=True)
    val01 = models.CharField(max_length=50)
    val02 = models.CharField(max_length=50, blank=True, null=True)
    val03 = models.CharField(max_length=50, blank=True, null=True)
"""
# Consulta un harcode por: [ app ~ asp ~ typcon ~ consum ~ item ]
class HrdLst(View):

	def get(self,request,*args,**kwargs):
		#print("  >> - - - ")
		json = '{"0":'
		# Guardamos el nuevo harcode
		app = self.request.GET.get('app')
		asp = self.request.GET.get('asp')
		typcon = self.request.GET.get('typcon')
		consum = self.request.GET.get('consum')
		item = self.request.GET.get('item')

		if Hardcode.objects.filter( Q(app=app) & Q(asp=asp) & Q(typcon=typcon) & Q(consum=consum) & Q(item=item) ).exists():
			hrd = Hardcode.objects.filter( Q(app=app) & Q(asp=asp) & Q(typcon=typcon) & Q(consum=consum) & Q(item=item) ).first()
			json += '"ok",'
			json += '"hrd":"'+str(hrd.app)+'~'+str(hrd.asp)+'~'+str(hrd.typcon)+'~'+str(hrd.consum)+'~'
			json += '~'+str(hrd.item)+'~'+str(hrd.val01)+'~'+str(hrd.val02)+'~'+str(hrd.val03)+'" }'

		else:
			json += '"Nen"}'

		#print("  >> "+json)
		return HttpResponse(json)
"""
	'Nen' : No encontrado

"""








# ===========            L O G   D E   A C C I Ó N            ============ #
class LogLis(ListView):
	paginate_by = 20
	model=LogDeModificaciones
	template_name='mant/log/lis.html' 
	
	def get_queryset(self):
		return LogDeModificaciones.objects.all().order_by('-pk')









# ================================  G A N T =====================



#"""  ========================= P E E R   R E V I E W  --------------------- """



#"""  ============================= O T R O S --------------------- """


def LogDeAccion(usu, tab, camp, tm,  val, val_ant, log):
	#print("  >> log > tab:"+tab+"  camp:"+camp+"  tm:"+str(tm)+"  usu:"+str(usu))
	hora = datetime.datetime.now()
	fecha=datetime.datetime(year=hora.year,month=hora.month,day=hora.day)
	nlog = LogDeModificaciones(usuario =usu, fecha = fecha, hora = hora,
		tipo_modificacion = tm , tabla = tab , campo = camp , id_entidad = val_ant, log=log)
	nlog.save()
"""
C:0		R:1		U:2		D:3
"""
def LogDeAccion1(request):
	LogDeAccion(184443,'peticion', 'estado',1, '2', 1, 'Log add++')
	return render(request,'inicio.html')







""" # Actualizar fechas
def Actualizaciones(request):

	print("  -----------------------------------------> trabajo")
	gnts = Gant.objects.filter()

	cont = 1

	for x in gnts:
		x.idcol_edit = AuthUser.objects.get(pk=cont)
		#x.save()
		cont = cont +  1
		if cont > 32:
			cont = 1
		print("  >> "+str(cont)+'  :: '+str(x.idcol_edit))

	print("  <----------------------------------------- trabajo")

	return HttpResponse("Ok")




def Actualizaciones(request):
	tks = Task.objects.all()
	for x in tks:
		print("  >a> "+str(x.fecha_inicio)+" | "+str(x.fecha_fin))
		if x.fecha_inicio != None:
			x.fecha_inicio = add_months(x.fecha_inicio,1)
		if x.fecha_fin !=  None:
			x.fecha_fin = add_months(x.fecha_fin,1)
		print("  --> "+str(x.fecha_inicio)+" | "+str(x.fecha_fin))
		#x.save()
	return HttpResponse("Ok")

def Actualizaciones(request):
	reqs = Requerimientos.objects.all()
	for x in reqs:
		print("  >a> "+str(x.fecha_estimacion)+" | "+str(x.fecha_inicio_planificada)+str(x.fehca_inicio_real)+str(x.fecha_fin_planificada))
		x.fecha_estimacion = add_months(x.fecha_estimacion,1)
		if x.fecha_inicio_planificada != None:
			x.fecha_inicio_planificada = add_months(x.fecha_inicio_planificada,1)
		if x.fehca_inicio_real !=  None:
			x.fehca_inicio_real = add_months(x.fehca_inicio_real,1)
		x.fecha_fin_planificada = add_months(x.fecha_fin_planificada,1)
		if x.fecha_entrega_real !=  None:
			x.fecha_entrega_real = add_months(x.fecha_entrega_real,1)
		print("  --> "+str(x.fecha_estimacion)+" | "+str(x.fecha_inicio_planificada)+str(x.fehca_inicio_real)+str(x.fecha_fin_planificada))
		#x.save()
	return HttpResponse("Ok")



def Actualizaciones(request):
	pets = Peticion.objects.all()
	for x in pets:
		print("  >a> "+str(x.fecha_solicitud)+" | "+str(x.fecha_fin_acuerdo)+"  | "+str(x.fecha_real_entrega))
		x.fecha_solicitud = add_months(x.fecha_solicitud,1)
		x.fecha_fin_acuerdo = add_months(x.fecha_fin_acuerdo,1)
		if x.fecha_real_entrega == 'None':
			x.fecha_real_entrega = add_months(x.fecha_real_entrega,1)
		print("  --> "+str(x.fecha_solicitud)+" | "+str(x.fecha_fin_acuerdo)+"  | "+str(x.fecha_real_entrega))
		#x.save()
	return HttpResponse("Ok")



def Actualizaciones(request):
	pets = Incidencia.objects.all()
	for x in pets:
		print("  >a> "+str(x.fecha_ident)+" | "+str(x.fecha_ini)+"  | "+str(x.fecha_fin))
		x.fecha_ident = add_months(x.fecha_ident,1)
		x.fecha_ini = add_months(x.fecha_ini,1)
		if x.fecha_fin == 'None':
			x.fecha_fin = add_months(x.fecha_fin,1)
		print("   --> "+str(x.fecha_ident)+" | "+str(x.fecha_ini)+"  | "+str(x.fecha_fin))
		#x.save()

		y = Incidencia()
		y.num_bug = x.num_bug
		y.requerimiento = x.requerimiento
		y.idetificador = x.idetificador
		y.descripcion = x.descripcion
		y.categoria = x.categoria
		y.localizada_en = x.localizada_en
		y.tipo_incidencia = x.tipo_incidencia
		y.criticidad = x.criticidad
		y.fecha_ident = x.fecha_ident
		y.categoria_inc = x.categoria_inc
		y.fecha_ini = x.fecha_ini
		y.fecha_fin = x.fecha_fin
		y.estado_inc_car = x.estado_inc_car
		y.esfuerzo = x.esfuerzo
		y.comentario_car = x.comentario_car
		y.subida_a_fenix = x.subida_a_fenix
		#y.save()
	return HttpResponse("Ok")



def Actualizaciones(request):
	tks = Riesgo.objects.all()
	for x in tks:
		print("  >a> "+str(x.fecha_indentificacion)+" | "+str(x.zultima_modificacion))
		if x.fecha_indentificacion != None:
			x.fecha_indentificacion = add_months(x.fecha_indentificacion,1)
		if x.zultima_modificacion !=  None:
			x.zultima_modificacion = add_months(x.zultima_modificacion,1)
		print("  --> "+str(x.fecha_indentificacion)+" | "+str(x.zultima_modificacion))
		x.save()
	return HttpResponse("Ok")



import datetime
import calendar
def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

"""


def Actualizaciones(request):
	return HttpResponse("Ok-1")