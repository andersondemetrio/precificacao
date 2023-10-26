from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

class Endereco(models.Model):
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=30)
    numero = models.CharField(max_length=30)
    complemento = models.CharField(max_length=30)
    bairro = models.CharField(max_length=30)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(max_length=30)
    # empresa_endereco = models.ForeignKey('Empresa', on_delete=models.CASCADE, related_name='enderecos')

class Usuarios(models.Model):
    email = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    permissao = models.CharField(max_length=50)
    # empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

class Cargos(models.Model):
    nome_cargo = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    # empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)

class HorasProdutivas(models.Model):
    data = models.DateField()
    jornada_diaria = models.DecimalField(max_digits=5, decimal_places=2) 
    # empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

class GastosFixos(models.Model):
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    mes = models.PositiveIntegerField()
    ano = models.PositiveIntegerField()
    tipo = models.CharField(max_length=12)
    # empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    
class AuxiliarCalculo(models.Model):
    total_salarios_gestores = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_salarios_prestadores = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_prestadores = models.PositiveIntegerField(default=0)
    total_meses_condominio = models.PositiveIntegerField(default=0)
    total_gastos_condominio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_meses_calendario = models.PositiveIntegerField(default=0)    
    total_meses_horasprodutivas = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    destinatario_email = models.EmailField() 
    # empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)      

class Empresa(models.Model):
    cnpj = models.CharField(max_length=18)
    numero_empresa = models.DecimalField(max_digits=4, decimal_places=0)
    nome_empresa = models.CharField(max_length=100)
    nome_fantasia = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    ativa = models.BooleanField()
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    # usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

class Colaboradores(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=12)
    cpf = models.CharField(max_length=14)
    setor = models.CharField(max_length=50, null=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    
class Beneficios(models.Model):
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    cargo = models.ForeignKey(Cargos, on_delete=models.CASCADE)
    # empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

class GastosVariaveis(models.Model):
    colaborador = models.ForeignKey(Colaboradores, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    # empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

class Propostas(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    data_proposta = models.DateField()
    aprovada = models.BooleanField()
    # empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

class CalendarioMensal(models.Model):
    ano = models.PositiveIntegerField()
    mes = models.PositiveIntegerField()
    descricao = models.CharField(max_length=100)
    dias_uteis = models.DecimalField(max_digits=5, decimal_places=2)
    jornada_diaria = models.PositiveIntegerField()
    feriado = models.DecimalField(max_digits=5, decimal_places=2)
    horas_produtivas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

class Employee(models.Model):
    SETOR_CHOICES = (
        ('Prestador de Serviço', 'Prestador de Serviço'),
        ('Gestores', 'Gestores'),
    )

    setor = models.CharField(max_length=50, choices=SETOR_CHOICES)
    beneficios = models.DecimalField(max_digits=10, decimal_places=2)
    periculosidade = models.DecimalField(max_digits=10, decimal_places=2)
    fgts = models.DecimalField(max_digits=10, decimal_places=2)
    um_terco_ferias = models.DecimalField(max_digits=10, decimal_places=2)
    fgts_ferias = models.DecimalField(max_digits=10, decimal_places=2)
    decimo_terceiro = models.DecimalField(max_digits=10, decimal_places=2)
    fgts_decimo_terceiro = models.DecimalField(max_digits=10, decimal_places=2)
    multa_rescisoria = models.DecimalField(max_digits=10, decimal_places=2)
    rateio = models.DecimalField(max_digits=10, decimal_places=2)
    custo_salario = models.DecimalField(max_digits=10, decimal_places=2)    
    custo_mes = models.DecimalField(max_digits=10, decimal_places=2)    
    colaborador = models.ForeignKey(Colaboradores, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargos, on_delete=models.CASCADE)
    # empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

class DescricaoObra(models.Model):
    horas = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField(default=0)
    orcamento_id = models.CharField(max_length=100)
    custo_mod = models.DecimalField(max_digits=10, decimal_places=2)
    custo_hora_con = models.DecimalField(max_digits=10, decimal_places=2)
    custo_total = models.DecimalField(max_digits=10, decimal_places=2)
    cargo = models.ForeignKey(Cargos, on_delete=models.CASCADE)
    horas_produtivas = models.DecimalField(max_digits=10, decimal_places=2)
    total_mod = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_condominio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_custo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    auxiliarcalculo= models.ForeignKey(AuxiliarCalculo, on_delete=models.CASCADE)
    # empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

class Rubrica(models.Model):
    orcamento_id = models.CharField(max_length=20)
    capacidade_produtiva = models.PositiveIntegerField(default=0)
    quantidade = models.PositiveIntegerField(default=0)
    custo_hora=models.DecimalField(max_digits=10, decimal_places=2)
    beneficios =models.DecimalField(max_digits=10, decimal_places=2)
    condominio =models.DecimalField(max_digits=10, decimal_places=2)
    outros = models.PositiveIntegerField(default=0)
    tributos = models.PositiveIntegerField(default=0)
    lucros = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=100)
    cliente = models.CharField(max_length=100)
    valor_sugerido = models.DecimalField(max_digits=10, decimal_places=2)
    valor_outros = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_tributos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_lucro = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
                
    
class DespesasDinamicas(models.Model):
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    rubrica= models.ForeignKey(Rubrica, on_delete=models.CASCADE)
    # empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
