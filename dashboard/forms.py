from django import forms
from dashboard.models import  *

class GastosFixosForm(forms.ModelForm):
    class Meta:
        model = GastosFixos
        fields = "__all__"

class GastosVariaveisForm(forms.ModelForm):
    class Meta:
        model = GastosVariaveis
        fields = "__all__"

class ColaboradoresForm(forms.ModelForm):
    class Meta:
        model = Colaboradores
        fields = "__all__"

class CargosForm(forms.ModelForm):
    class Meta:
        model = Cargos
        fields = "__all__"

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = "__all__"

class EmpresaForm():
    class Meta:
        model = Empresa
        fields = "__all__"

class HorasProdutivasForm(forms.ModelForm):
    class Meta:
        model = HorasProdutivas
        fields = "__all__"

class EmailForm(forms.ModelForm):
    class Meta:
        model = AuxiliarCalculo
        fields = ['destinatario_email']
        
class RubricaForm(forms.ModelForm):
    class Meta:
        model = Rubrica
        fields = '__all__'  # Isso permite que todos os campos do modelo sejam editáveis no formulário


