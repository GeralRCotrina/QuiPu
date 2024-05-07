from django import forms

from apps.gestion.models import EstimPeso


"""
class EstimPeso(models.Model):
    tarea_tipo = models.ForeignKey('PeticionTipo', models.DO_NOTHING, db_column='tarea_tipo')
    tarea_subtipo = models.ForeignKey('TaskFaseActividad', models.DO_NOTHING, db_column='tarea_subtipo')
    dificultad = models.ForeignKey('Zdificultad', models.DO_NOTHING, db_column='dificultad')
    peso = models.FloatField()
    peso_hist = models.FloatField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    alta = models.CharField(max_length=1, blank=True, null=True)
"""


class EstimPesoForm(forms.ModelForm):

    class Meta:
        model = EstimPeso

        fields = ['tarea_tipo', 'tarea_subtipo', 'dificultad', 'peso', 'peso_hist', 'fecha', 'alta']

        labels = {
            'tarea_tipo':'TIPO',
            'tarea_subtipo':'SUBTIPO',
        }

        widgets={
            'fecha': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'alta':forms.TextInput(attrs={'type':'checkbox'}),
        }


class EstimPesoEdiForm(forms.ModelForm):

    class Meta:
        model = EstimPeso

        fields = ['tarea_tipo', 'tarea_subtipo', 'dificultad', 'peso', 'fecha', 'alta']

        labels = {
            'tarea_tipo':'TIPO',
            'tarea_subtipo':'SUBTIPO',
        }

        widgets={
            'alta': forms.TextInput(attrs={'type':'checkbox'}),
        }