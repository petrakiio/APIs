from django import forms
from ..models.tarefa import TarefasModel

class TarefaForm(forms.ModelForm):
    class Meta:
        model = TarefasModel
        fields = ['nome', 'descricao', 'concluido']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'input'}),
            'descricao': forms.Textarea(attrs={'class': 'textarea', 'rows': 4}),
            'concluido': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }
        
