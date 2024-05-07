from django import forms

from apps.gestion.models import *



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



