from django import forms

from apps.gestion.models import *


class RiesgoForm(forms.ModelForm):
	class Meta:
		model = Riesgo
		fields = ['codigo', 'fecha_indentificacion','requerimiento','tipo','estado','resolucion',
			'responsable' ,'categoria','descripcion','acciones','seguimiento']

		widgets={
		    'fecha_indentificacion':forms.DateInput(attrs={'type':'date'}),
		    'descripcion':forms.Textarea(attrs={'rows':'2'}),
		    'seguimiento':forms.Textarea(attrs={'rows':'2'}),
		    'acciones':forms.Textarea(attrs={'rows':'2'}),
		}

class RiesgoEdiForm(forms.ModelForm):
	class Meta:
		model = Riesgo
		fields = ['codigo', 'fecha_indentificacion','requerimiento','tipo','estado','resolucion',
			'responsable' ,'categoria','descripcion','acciones','seguimiento']

		widgets={
		    'descripcion':forms.Textarea(attrs={'rows':'2'}),
		    'seguimiento':forms.Textarea(attrs={'rows':'2'}),
		    'acciones':forms.Textarea(attrs={'rows':'2'}),
		}

