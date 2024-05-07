from django import forms

from apps.gestion.models import *



class ReqForm(forms.ModelForm):

	class Meta:
		model = Requerimientos

		fields = [
					'codigo',
					#'requerimien_asociado',
					'modulo',
					#'codigo_cliente',
					'breve_descripcion' ,
					#'descripcion' ,
					'peticion',
					'contacto',
					'estado' ,
					#'fecha_estimacion',
					'fecha_inicio_planificada',
					#'fehca_inicio_real',
					'fecha_fin_planificada',
					#'fecha_entrega_real' ,
					'prioridad' ,
					'criticidad',
					'calidad_input',
					'input_final',
					'estimacion_acuerdo',
					#'estimacion_fenix_h',
					#'horas_adicionales',
					#'horas_acuerddo_mes',
					#'seguimiento_diario',
					#'ordent',
					#'programas',
					#GRCL4  -> ( Valores para actualozaciones masivas )
					'responsable'
				]

		labels = {
			'breve_descripcion':'Título',
			#'descripcion':'Descripción',
			'codigo':'Código ',
			#'codigo_cliente':'Codigo interno del cliente ',
			'seguimiento_diario':'Seguimiento diario (Colocar fecha)',
			#'fecha_estimacion':'Fecha de estimación (*)',
			'fecha_inicio_planificada':'Fecha inicio planificado (*)',
			#'fehca_inicio_real':'Fecha inicio real',
			'fecha_fin_planificada':'Fecha fin planificada (*)',
			#'fecha_entrega_real':'Fecha entrega real',
			#'estimacion_acuerdo':'Estimación acuerdo (*)',
			#'ordent':'OT',
			#'programas':'Programas modificados',

		}
		widgets={
		    'codigo':forms.TextInput(attrs={'readonly':'readonly','ondblclick':'hcrEditable(this.id)',
		    								'data-toggle':'tooltip',
		    								'data-original-title':'Doble click para modificar'}),
		    #'requerimien_asociado':forms.TextInput(attrs={'placeholder':'Null'}),
		    'breve_descripcion':forms.Textarea(attrs={'class':'form-control','rows':'2'}),
		    #'descripcion':forms.Textarea(attrs={'class':'form-control','rows':'4'}),
		    #'fecha_estimacion':forms.DateInput(attrs={'class':'form-control','type':'date','id':'fecha_desde1'}),
		    'fecha_inicio_planificada':forms.DateInput(attrs={'class':'form-control','type':'date','id':'fecha_hasta1'}),
		    #'fehca_inicio_real':forms.DateInput(attrs={'class':'form-control','type':'date'}),
		    'fecha_fin_planificada':forms.DateInput(attrs={'class':'form-control','type':'date'}),
		    #'fecha_entrega_real':forms.DateInput(attrs={'class':'form-control','type':'date'}),
		    'estimacion_acuerdo':forms.NumberInput(attrs={'class':'form-control','step':'0.25','min':'0'}), 
		    'estimacion_fenix_h':forms.NumberInput(attrs={'class':'form-control','step':'0.25','min':'0'}),
		    #'horas_adicionales':forms.NumberInput(attrs={'class':'form-control','step':'0.25','min':'0'}),
		    #'horas_acuerddo_mes':forms.NumberInput(attrs={'class':'form-control','step':'0.25','min':'0'}),
		    #'seguimiento_diario':forms.Textarea(attrs={'class':'form-control','rows':'3'}),
		    #'ordent':forms.Textarea(attrs={'class':'form-control','rows':'1'}),
		    #'programas':forms.Textarea(attrs={'class':'form-control','rows':'2'}),
		}
"""
 
"""

class ReqEditForm(forms.ModelForm):

	class Meta:
		model = Requerimientos

		fields = ['codigo','requerimien_asociado','modulo','codigo_cliente', 'breve_descripcion', 'descripcion',
					'peticion','responsable','contacto',
					#'fecha_estimacion',
					'fecha_inicio_planificada',
					#'fehca_inicio_real',
					'fecha_fin_planificada',
					#'fecha_entrega_real' ,
					'calidad_input', 'input_final', 'estimacion_alto_nivel','prioridad', 'criticidad', 
					'estimacion_acuerdo','estimacion_fenix_h',
					#'horas_adicionales',
					'estado' ,
					#'horas_acuerddo_mes',
					'seguimiento_diario',
					'ordent',
					'programas'
				]

		labels = {
			'codigo':'Código (Ejm: 20200516_10)',
			'codigo_cliente':'Codigo interno del cliente (Ejm: COF - 4257)',
			'seguimiento_diario':'Seguimiento diario (Colocar la fecha)',
			#'horas_acuerddo_mes':'horas_acuerddo_mes'
			'ordent':'OT',
			'programas':'Programas modificados',
		}
		widgets={		    
		    'estimacion_acuerdo':forms.NumberInput(attrs={'class':'form-control','step':'0.25','min':'0'}), 
		    'estimacion_fenix_h':forms.NumberInput(attrs={'class':'form-control','step':'0.25','min':'0'}),
		    #'horas_adicionales':forms.NumberInput(attrs={'class':'form-control','step':'0.25','min':'0'}),
		    #'horas_acuerddo_mes':forms.NumberInput(attrs={'class':'form-control','step':'0.25','min':'0'}), 
		    'breve_descripcion':forms.Textarea(attrs={'class':'form-control','rows':'2'}),
		    'descripcion':forms.Textarea(attrs={'class':'form-control','rows':'4'}),
		    'seguimiento_diario':forms.Textarea(attrs={'class':'form-control','rows':'3'}),
		    'ordent':forms.Textarea(attrs={'class':'form-control','rows':'1'}),
		    'programas':forms.Textarea(attrs={'class':'form-control','rows':'2'}),
		}

class ReqDupForm(forms.ModelForm):

	class Meta:
		model = Requerimientos

		fields = ['codigo','requerimien_asociado','modulo','codigo_cliente', 'breve_descripcion', 'descripcion',
					'peticion','responsable','contacto','fecha_inicio_planificada',
					'fecha_fin_planificada','calidad_input', 'estimacion_alto_nivel','prioridad' ,  'criticidad',
					'estimacion_acuerdo','estado','ordent','programas'
				]

		labels = {
			'codigo':'Código (Ejm: 20200516_10)',
			'codigo_cliente':'Codigo interno del cliente (Ejm: COF - 4257)',
			'ordent':'OT',
			'programas':'Programas modificados',
		}
		widgets={		    
		    'estimacion_acuerdo':forms.NumberInput(attrs={'class':'form-control','step':'0.25','min':'0'}),
		    'estimacion_fenix_h':forms.NumberInput(attrs={'class':'form-control','step':'0.25','min':'0'}),
		    'fecha_inicio_planificada':forms.DateInput(attrs={'class':'form-control','type':'date','id':'fecha_hasta1'}),
		    'fecha_fin_planificada':forms.DateInput(attrs={'class':'form-control','type':'date'}),
		    #'horas_adicionales':forms.NumberInput(attrs={'class':'form-control','step':'0.25','min':'0'}),
		    #'horas_acuerddo_mes':forms.NumberInput(attrs={'class':'form-control','step':'0.25','min':'0'}), 
		    'breve_descripcion':forms.Textarea(attrs={'class':'form-control','rows':'2'}),
		    'descripcion':forms.Textarea(attrs={'class':'form-control','rows':'4'}),
		    'seguimiento_diario':forms.Textarea(attrs={'class':'form-control','rows':'3'}),
		    'ordent':forms.Textarea(attrs={'class':'form-control','rows':'1'}),
		    'programas':forms.Textarea(attrs={'class':'form-control','rows':'2'}),
		}

class ReqBitaForm(forms.ModelForm):

	class Meta:
		model = Requerimientos

		fields = ['codigo','breve_descripcion','estado','ordent','seguimiento_diario','programas']
		labels = { 
				'codigo' : 'Req.',
				'breve_descripcion':'',
				'ordent':'OT',
				'seguimiento_diario':'Bitácora',
				'programas': 'Prog. modificados'
				}

		widgets = { 
			'codigo':forms.TextInput(attrs={'cols':'30','rows':'1','readonly':'readonly','style':'background:#E7F0EC;'}) ,
			'breve_descripcion':forms.Textarea(attrs={'cols':'100','rows':'1','readonly':'readonly','style':'background:#E7F0EC;'}) ,
			'ordent':forms.Textarea(attrs={'cols':'100','rows':'2'}) ,
			'seguimiento_diario':forms.Textarea(attrs={'cols':'100','rows':'5'}) ,
			'programas':forms.Textarea(attrs={'cols':'100','rows':'3'}) ,
			}

