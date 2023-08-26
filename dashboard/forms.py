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

class InsumosForm(forms.ModelForm):
    class Meta:
        model = Insumos
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




class EmployeeForm(forms.Form):
    colaborador = forms.ModelChoiceField(queryset=Colaboradores.objects.all(), label='Colaborador')
    setor = forms.ChoiceField(choices=Employee.SETOR_CHOICES)
    cargo = forms.ChoiceField(choices=Employee.CARGO_CHOICES)
    cargo_secundario = forms.CharField(max_length=50)
    periculosidade = forms.DecimalField(max_digits=10, decimal_places=2)
    fgts = forms.DecimalField(max_digits=10, decimal_places=2)
    um_terco_ferias = forms.DecimalField(max_digits=10, decimal_places=2)
    fgts_ferias = forms.DecimalField(max_digits=10, decimal_places=2)
    decimo_terceiro = forms.DecimalField(max_digits=10, decimal_places=2)
    fgts_decimo_terceiro = forms.DecimalField(max_digits=10, decimal_places=2)
    multa_rescisoria = forms.DecimalField(max_digits=10, decimal_places=2)
    rateio = forms.DecimalField(max_digits=10, decimal_places=2)
    custo_mes = forms.DecimalField(max_digits=10, decimal_places=2)
