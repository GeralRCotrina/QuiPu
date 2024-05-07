
from django import forms
from apps.gestion.models import *


class TaskForm(forms.ModelForm):
	class Meta:
		model = Task
		fields = [ 'requerimiento', 'subtarea', 'fase_actividad', 'fecha_inicio',
					'fecha_fin', 'esfuerzo_total_estandar' ]
		widgets={
			'subtarea':forms.Textarea(attrs={'class':'form-control','rows':'3'}),
			'fecha_inicio':forms.DateInput(attrs={'class':'form-control','type':'date','id':'fecha_desde1'}),
			'fecha_fin':forms.DateInput(attrs={'class':'form-control','type':'date','id':'fecha_hasta1'}),
			'esfuerzo_total_estandar':forms.NumberInput(attrs={'class':'form-control','step':'0.25','min':'0'}),
		}


class TaskEdiForm(forms.ModelForm):
	class Meta:
		model = Task
		fields = [ 'idtask', 'id_interno', 'requerimiento', 'responsable', 'subtarea', 'fase_actividad',
				   'fecha_inicio', 'fecha_fin', 'esfuerzo_ejecutado', 'estado' ]
		widgets={
			'subtarea':forms.Textarea(attrs={'class':'form-control','rows':'3'}),
			'fecha_inicio':forms.DateInput(attrs={'class':'form-control'}),
			'fecha_fin':forms.DateInput(attrs={'class':'form-control'}),
			'esfuerzo_total_estandar':forms.NumberInput(attrs={'class':'form-control','step':'0.25','min':'0'}),
			'esfuerzo_ejecutado':forms.NumberInput(attrs={'class':'form-control','step':'0.25','min':'0'}),
		}




