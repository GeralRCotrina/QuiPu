from django import forms

from apps.gestion.models import *

"""

    pet_ruta = models.CharField(max_length=200, blank=True, null=True)
    ot_ruta = models.CharField(max_length=200, blank=True, null=True)
    contenedora = models.CharField(max_length=2, choices=CONTENEDORA, default='On')
"""
class PetForm(forms.ModelForm):

	class Meta:
		model = Peticion

		fields = ['id_pet_fenix','id_ot_fenix','nombre','tipo','cliente','gestion', 'contenedora', 'estado','input_final',
					'fecha_solicitud', 'fecha_fin_acuerdo', #'horas_acuerdo', #'pet_ruta','ot_ruta','comentario',
					'color','creador']

		labels = {
			'dni':'DNI',
			'id_pet_fenix':'Id en Fenix',
			'id_ot_fenix':'Work Item ID',
			'nombre':'Nombre',
			'tipo':'Tipo',
			'gestion':'Gestión',
			'estado':'Estado',
			'input_final':'Input final',
			'fecha_solicitud':'Fecha solicitud',
			'fecha_fin_acuerdo':'Fecha fin acordada',
			#'fecha_real_entrega':'Fecha de entrega real',
			#'horas_acuerdo':'Horas Acuerdo',
			#'comentario':'Comentario',
			'color':'Color de gant',
			#'pet_ruta':'Ruta Petición',
			#'ot_ruta':'Ruta OT',
			'creador':'Responsable',
		}

		widgets={
			'id_pet_fenix' : forms.TextInput(attrs={'class':'form-control','maxlength':'7'}), 
		    'id_ot_fenix'  : forms.TextInput(attrs={'class':'form-control','maxlength':'7'}), 
		    'nombre'  : forms.TextInput(attrs={'class':'form-control','maxlength':'45'}), 
		    'tipo' : forms.Select(attrs={'class':'form-control'}),
		    'gestion' : forms.Select(attrs={'class':'form-control'}),
		    'estado' :forms.Select(attrs={'class':'form-control'}),
		    'input_final' :forms.Select(attrs={'class':'form-control'}),
		    'fecha_solicitud':forms.DateInput(attrs={'class':'form-control','type':'date','id':'fecha_desde1'}),
		    'fecha_fin_acuerdo':forms.DateInput(attrs={'class':'form-control','type':'date','id':'fecha_hasta1'}),
		    #'horas_acuerdo':forms.NumberInput(attrs={'class':'form-control','step':'0.25','min':'0'}),
		    #'comentario':forms.Textarea(attrs={'class':'form-control','rows':'2'}),
		    'color':forms.TextInput(attrs={'type':'color'}),

		    'contenedora'  : forms.TextInput(attrs={'type':'checkbox','checked':'checked'}), 
		    #'pet_ruta'  : forms.TextInput(attrs={'class':'form-control'}), 
		   # 'ot_ruta'  : forms.TextInput(attrs={'class':'form-control'}), 
		}


class PetEditForm(forms.ModelForm):

	class Meta:
		model = Peticion

		fields = ['id_pet_fenix','id_ot_fenix','nombre','tipo','cliente','gestion', 'contenedora', 'estado', 'input_final',
					'fecha_solicitud', 'fecha_fin_acuerdo','horas_acuerdo', 'pet_ruta','ot_ruta', 'comentario',
					'creador','color']

		labels = {
			'dni':'DNI',
			'id_pet_fenix':'Id en Fenix',
			'id_ot_fenix':'Work Item ID',
			'nombre':'Nombre',
			'tipo':'Tipo',
			'gestion':'Gestión',
			'estado':'Estado',
			'input_final':'Input final',
			'fecha_solicitud':'Fecha solicitud',
			'fecha_fin_acuerdo':'Fecha fin acordada',
			#'fecha_real_entrega':'Fecha de entrega real',
			'horas_acuerdo':'Horas Acuerdo',
			'comentario':'Comentario',
			'creador':'Creador de petición',
			'color':'Color de gant',
			'pet_ruta':'Ruta Petición',
			'ot_ruta':'Ruta OT',
		}

		widgets={
			'id_pet_fenix' : forms.TextInput(attrs={'class':'form-control','maxlength':'7'}), 
		    'id_ot_fenix'  : forms.TextInput(attrs={'class':'form-control','maxlength':'7'}), 
		    'nombre'  : forms.TextInput(attrs={'class':'form-control','maxlength':'45'}), 
		    'tipo' : forms.Select(attrs={'class':'form-control'}),
		    'gestion' : forms.Select(attrs={'class':'form-control'}),
		    'estado' :forms.Select(attrs={'class':'form-control'}),
		    'input_final' :forms.Select(attrs={'class':'form-control'}),
		    'horas_acuerdo':forms.NumberInput(attrs={'class':'form-control','step':'0.25','min':'0'}),
		    'comentario':forms.Textarea(attrs={'class':'form-control','rows':'2'}),
		    'creador': forms.Select(attrs={'class':'form-control'}),
		    'color':forms.TextInput(attrs={'type':'color'}),
		    'pet_ruta'  : forms.TextInput(attrs={'class':'form-control'}), 
		    'ot_ruta'  : forms.TextInput(attrs={'class':'form-control'}), 
		    'contenedora'  : forms.TextInput(attrs={'type':'checkbox','checked':'checked' }), 
		}









