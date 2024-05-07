from django import forms

from apps.gestion.models import *



class IncidenciaForm(forms.ModelForm):
	class Meta:
		model = Incidencia
		fields = ['num_bug', 'requerimiento','idetificador','descripcion','categoria','localizada_en',
			'tipo_incidencia' ,'criticidad','fecha_ident','categoria_inc','fecha_ini','fecha_fin',
			'estado_inc_car','esfuerzo','comentario_car']

		widgets={
			'num_bug':forms.TextInput(attrs={'readonly':'readonly'}),		
		    'descripcion':forms.Textarea(attrs={'rows':'2'}),
		    'fecha_ident':forms.DateInput(attrs={'type':'date'}),
		    'fecha_ini':forms.DateInput(attrs={'type':'date'}),
		    'fecha_fin':forms.DateInput(attrs={'type':'date'}),
		    'esfuerzo':forms.NumberInput(attrs={'step':'0.25','min':'0'}),
		    'comentario_car':forms.Textarea(attrs={'rows':'2'}),
		}

class IncidenciaEdiForm(forms.ModelForm):
	class Meta:
		model = Incidencia
		fields = ['num_bug', 'requerimiento','idetificador','descripcion','categoria','localizada_en',
			'tipo_incidencia' ,'criticidad','fecha_ident','categoria_inc','fecha_ini','fecha_fin',
			'estado_inc_car','esfuerzo','comentario_car']

		widgets={
		    'descripcion':forms.Textarea(attrs={'rows':'2'}),
		    'esfuerzo':forms.NumberInput(attrs={'step':'0.25','min':'0'}),
		    'comentario_car':forms.Textarea(attrs={'rows':'2'}),
			'requerimiento':forms.Select(attrs={'class':'form-control'}),
		    
		}

 