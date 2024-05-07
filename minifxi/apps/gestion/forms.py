from django import forms

from apps.gestion.models import *



class AuthUserForm(forms.ModelForm):

	class Meta:
		model = AuthUser
		fields = ['username','codigo','alias','first_name','last_name','email','categoria','pais','dni',
					'foto_perfil','sexo','celular','telefono','fecha_nacimiento']	
		labels = {
			'username':'Usuario',
			'first_name':'Nombres',
			'last_name':'Apellidos',
			'email':'correo',
			'alias':'alias',
			'sexo':'Sexo',
			'telefono':'telefono',
			'celular':'Movil',
			'fecha_nacimiento':'Fecha de nacimiento'
			}
  
		widgets={
		    'username':forms.TextInput(attrs={'class':'form-control'}),
		    'first_name':forms.TextInput(attrs={'class':'form-control'}),
		    'last_name':forms.TextInput(attrs={'class':'form-control'}),
		    'email':forms.TextInput(attrs={'class':'form-control'}),
		    'dni':forms.TextInput(attrs={'class':'form-control','type':'number','maxlength':'8'}),
		    'alias':forms.TextInput(attrs={'class':'form-control'}),
			'sexo':forms.Select(attrs={'class':'form-control'}),
			'telefono':forms.TextInput(attrs={'class':'form-control'}),
			'celular':forms.TextInput(attrs={'class':'form-control'}),
			'foto_perfil':forms.FileInput(),
		    'fecha_nacimiento':forms.DateInput(attrs={'class':'form-control','type':'date'}),
	    }

class AuthUserFormUF(forms.ModelForm):

	class Meta:
		model = AuthUser
		fields = ['foto_perfil']	
		widgets={ 'foto_perfil':forms.FileInput(), }


class AuthUserFormU(forms.ModelForm):

	class Meta:
		model = AuthUser
		fields = ['alias','first_name','last_name','email','pais','dni','sexo','celular','telefono']	
		#widgets={ 'foto_perfil':forms.FileInput(), }




class DominioForm(forms.ModelForm):
	class Meta:
		model = Dominio
		fields = ['codigo','nombre','responsable', 'descripcion']


class EquipoForm(forms.ModelForm):
	class Meta:
		model = Equipo
		fields = ['codigo','nombre','dominio','responsable', 'descripcion']


class ClienteForm(forms.ModelForm):
	class Meta:
		model = Cliente
		fields = ['codigo','equipo','cliente','correlativo','ftes','idpais','descripcion','wi_id']


class PaisForm(forms.ModelForm):
	class Meta:
		model = Pais
		fields = ['codigo','pais','codigo_tel']



class IncLocalizadaEnForm(forms.ModelForm):
	class Meta:
		model = IncLocalizadaEn
		fields = ['descripcion']


class PeticionEstadoForm(forms.ModelForm):
	class Meta:
		model = PeticionEstado
		fields = ['variable','codigo','descripcion','descripcion_fenix','col_str','col_lig']

		widgets={
		    'col_str':forms.TextInput(attrs={'type':'color'}),
		    'col_lig':forms.TextInput(attrs={'type':'color'}),
		}


class IncTipoForm(forms.ModelForm):
	class Meta:
		model = IncTipo
		fields = ['descripcion']


class RiesgoCategoriaForm(forms.ModelForm):
	class Meta:
		model = RiesgoCategoria
		fields = ['categoria']

		widgets={	'categoria':forms.Textarea(attrs={'rows':'1'}), }


class DudasRelalivaAForm(forms.ModelForm):
	class Meta:
		model = DudasRelalivaA
		fields = ['descripcion']

		widgets={	'descripcion':forms.Textarea(attrs={'rows':'1'}), }


class DudasFaseLocForm(forms.ModelForm):
	class Meta:
		model = DudasFaseLoc
		fields = ['descripcion']

		widgets={	'descripcion':forms.Textarea(attrs={'rows':'1'}), }



class DudasRelalivaAForm(forms.ModelForm):
	class Meta:
		model = DudasRelalivaA
		fields = ['descripcion']

		widgets={	'descripcion':forms.Textarea(attrs={'rows':'1'}), }




class DudasForm(forms.ModelForm):
	class Meta:
		model = Dudas
		fields = ['task','estado','acc','descripcion','respuesta','rep_repuesta_proy',
					'rep_respuesta_cli','rep_consulta','fecha_prev_rep','agrupacion','id_realicionada',
					'ambito','criticidad','fase_localizada','realativa_a','doc_entrada_incompleta']
		labels = {
			'descripcion':'Descripcion ¿? (*)',
			'respuesta':'Respuesta (*)',
			'rep_repuesta_proy':'Resp. rpta proyecto (*)',
			'rep_respuesta_cli':'Resp. rpta cliente (*)'

		}

		widgets={
		    'fecha_indentificacion':forms.DateInput(attrs={'type':'date'}),
		    'descripcion':forms.Textarea(attrs={'rows':'2'}),
		    'respuesta':forms.Textarea(attrs={'rows':'2'}),
		    'fecha_prev_rep':forms.DateInput(attrs={'type':'date'}),
		    }


class DudasEdiForm(forms.ModelForm):
	class Meta:
		model = Dudas
		fields = ['task','estado','acc','descripcion','respuesta','rep_repuesta_proy',
					'rep_respuesta_cli','rep_consulta','fecha_prev_rep','agrupacion','id_realicionada',
					'ambito','criticidad','fase_localizada','realativa_a','doc_entrada_incompleta']

		widgets={
		    'fecha_indentificacion':forms.DateInput(attrs={'type':'date'}),
		    'descripcion':forms.Textarea(attrs={'rows':'2'}),
		    'respuesta':forms.Textarea(attrs={'rows':'2'}),
		    }




class AuthClienteForm(forms.ModelForm):
	class Meta:
		model = AuthCliente
		fields = ['idcliente','idauth','asignacion','descripcion','fecha_alta','fecha_baja']#,'activo']

		widgets={
			    'fecha_alta':forms.DateInput(attrs={'type':'date'}),
			    'fecha_baja':forms.DateInput(attrs={'type':'date'}),
			    'descripcion':forms.Textarea(attrs={'rows':'2'}),
			   # 'activo':forms.TextInput(attrs={'type':'checkbox','checked':'checked'}),
		    } 

class AuthClienteEdiForm(forms.ModelForm):
	class Meta:
		model = AuthCliente
		fields = ['idcliente','idauth','asignacion','descripcion','fecha_alta','fecha_baja']#,'activo']

		widgets={ 'descripcion':forms.Textarea(attrs={'rows':'2'}), }
			      #'activo':forms.TextInput(attrs={'type':'checkbox','checked':'checked'}), }


class PeerReviewForm(forms.ModelForm):
	class Meta:
		model = PeerReview
		fields = [ 'idperer', 'codigo', 'requerimiento' , 'revisor' , 'resultado' , 'version' , 'nota' ]

		widgets={ 'nota':forms.Textarea(attrs={'rows':'4','cols':'70'}),
				  'codigo':forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}),
				  'version':forms.TextInput(attrs={'readonly':'readonly'}) }

class PeerReviewEdiForm(forms.ModelForm):
	class Meta:
		model = PeerReview
		fields = [ 'idperer', 'codigo', 'requerimiento' , 'revisor' , 'resultado' , 'version' , 'nota' ]

		widgets={ 'nota':forms.Textarea(attrs={'rows':'4','cols':'70'}),
				  'codigo':forms.TextInput(attrs={'class':'form-control'}) }





# ===========             P R I O R I D A D                  ============ #
class ReqPrioridadForm(forms.ModelForm):
	class Meta:
		model = ReqPrioridad
		fields = ['prioridad','prioridad','descripcion','color1','color2']

		widgets={
		    'color1':forms.TextInput(attrs={'type':'color'}),
		    'color2':forms.TextInput(attrs={'type':'color'}),
		}




# ===========            M Ó D U L O S   S A P                  ============ #

class ModulosSapForm(forms.ModelForm):
	class Meta:
		model = ModulosSap
		fields = ['codigo','modulo','zultima_modificacion','estado']






# ===========            R E Q   C R I T I C I D A D             ============ #
class ReqCriticidadForm(forms.ModelForm):
	class Meta:
		model = ReqCriticidad
		fields = ['criticidad','crit']






# ===========            I N P U T   F I N A L   P E T             ============ #
class PeticionInputFinalForm(forms.ModelForm):
	class Meta:
		model = PeticionInputFinal
		fields = ['codigo','input_final','descripcion']






# ===========            I N P U T   F I N A L   P E T             ============ #
class ReqCalidadInputForm(forms.ModelForm):
	class Meta:
		model = ReqCalidadInput
		fields = ['codigo','calidad','descripcion']






# ===========            I N P U T   F I N A L  R E Q             ============ #
class ReqInputFinalForm(forms.ModelForm):
	class Meta:
		model = ReqInputFinal
		fields = ['codigo','input_final','descripcion']


		

		