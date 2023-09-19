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

class Usuarios(models.Model):
    email = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    permissao = models.CharField(max_length=50)

class Cargos(models.Model):
    nome_cargo = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    
    # def __str__(self):
    #     return self.nome

class HorasProdutivas(models.Model):
    data = models.DateField()
    jornada_diaria = models.DecimalField(max_digits=5, decimal_places=2) 

class GastosFixos(models.Model):
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    mes = models.PositiveIntegerField()
    ano = models.PositiveIntegerField()
    tipo = models.CharField(max_length=12)
    
class AuxiliarCalculo(models.Model):
    total_salarios_gestores = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_salarios_prestadores = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_prestadores = models.PositiveIntegerField(default=0)
    total_meses_condominio = models.PositiveIntegerField(default=0)
    total_gastos_condominio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_meses_calendario = models.PositiveIntegerField(default=0)    
    total_meses_horasprodutivas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    destinatario_email = models.EmailField()       

class Insumos(models.Model):
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

class Empresa(models.Model):
    cnpj = models.CharField(max_length=18)
    numero_empresa = models.DecimalField(max_digits=4, decimal_places=0)
    nome_empresa = models.CharField(max_length=100)
    nome_fantasia = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    ativa = models.BooleanField()
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

class Colaboradores(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=12)
    cpf = models.CharField(max_length=14)
    setor = models.CharField(max_length=50, null=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
class Beneficios(models.Model):
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    cargo = models.ForeignKey(Cargos, on_delete=models.CASCADE)

class GastosVariaveis(models.Model):
    colaborador = models.ForeignKey(Colaboradores, on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumos, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)

class Propostas(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    data_proposta = models.DateField()
    aprovada = models.BooleanField()

# Necessário criação de uma nova classe no banco para realizar o valor das horas do colaborador


# Model criada para atener a demanda de 
class CalendarioMensal(models.Model):
    mes = models.PositiveIntegerField()
    ano = models.PositiveIntegerField()
    funcionario = models.ForeignKey(Colaboradores, on_delete=models.CASCADE)
    dias_uteis = models.PositiveIntegerField()
    jornada_diaria = models.DecimalField(max_digits=5, decimal_places=2)  # Adicione este campo
    horas_produtivas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)



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

class Rubrica(models.Model):
    orcamento_id = models.CharField(max_length=20)
    quantidade = models.PositiveIntegerField(default=0)
    compra_materiais=models.DecimalField(max_digits=10, decimal_places=2)
    materiais_dvs=models.DecimalField(max_digits=10, decimal_places=2)
    dvs_socio=models.DecimalField(max_digits=10, decimal_places=2)
    custo_hora=models.DecimalField(max_digits=10, decimal_places=2)
    beneficios =models.DecimalField(max_digits=10, decimal_places=2)
    telefonia_comunicacao=models.DecimalField(max_digits=10, decimal_places=2)
    seguro_maquinas_equipamentos=models.DecimalField(max_digits=10, decimal_places=2)
    manutencao=models.DecimalField(max_digits=10, decimal_places=2)
    dvs_operacao=models.DecimalField(max_digits=10, decimal_places=2)
    bonus_resultado=models.DecimalField(max_digits=10, decimal_places=2)
    plr=models.DecimalField(max_digits=10, decimal_places=2)
    horas_extras=models.DecimalField(max_digits=10, decimal_places=2)
    exames_adiciona_demissional=models.DecimalField(max_digits=10, decimal_places=2)
    terceirizados =models.DecimalField(max_digits=10, decimal_places=2)
    alimentacao=models.DecimalField(max_digits=10, decimal_places=2)
    hospedagem=models.DecimalField(max_digits=10, decimal_places=2)
    quilometragem =models.DecimalField(max_digits=10, decimal_places=2)
    deslocamento =models.DecimalField(max_digits=10, decimal_places=2)
    combustivel=models.DecimalField(max_digits=10, decimal_places=2)
    estacionamento_pedagio=models.DecimalField(max_digits=10, decimal_places=2)
    comissoes=models.DecimalField(max_digits=10, decimal_places=2)
    seguros_obra_dvs=models.DecimalField(max_digits=10, decimal_places=2)
    insumos=models.DecimalField(max_digits=10, decimal_places=2)
    manutencao_conservacao=models.DecimalField(max_digits=10, decimal_places=2)
    distrato_multas=models.DecimalField(max_digits=10, decimal_places=2)
    condominio =models.DecimalField(max_digits=10, decimal_places=2)
    tributos = models.PositiveIntegerField(default=0)
    lucros = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=100)
    valor_sugerido = models.DecimalField(max_digits=10, decimal_places=2)
