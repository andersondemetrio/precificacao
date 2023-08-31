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
    
    def __str__(self):
        return self.nome

class HorasProdutivas(models.Model):
    data = models.DateField()
    jornada_diaria = models.DecimalField(max_digits=5, decimal_places=2)

class GastosFixos(models.Model):
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

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
    cargo = models.ForeignKey(Cargos, on_delete=models.CASCADE)
    # salario = models.DecimalField(max_digits=10, decimal_places=2)
    # beneficios = models.DecimalField(max_digits=10, decimal_places=2)
    # encargos = models.DecimalField(max_digits=10, decimal_places=2)
    #endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

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
    periculosidade = models.DecimalField(max_digits=10, decimal_places=2)
    fgts = models.DecimalField(max_digits=10, decimal_places=2)
    um_terco_ferias = models.DecimalField(max_digits=10, decimal_places=2)
    fgts_ferias = models.DecimalField(max_digits=10, decimal_places=2)
    decimo_terceiro = models.DecimalField(max_digits=10, decimal_places=2)
    fgts_decimo_terceiro = models.DecimalField(max_digits=10, decimal_places=2)
    multa_rescisoria = models.DecimalField(max_digits=10, decimal_places=2)
    rateio = models.DecimalField(max_digits=10, decimal_places=2)
    custo_mes = models.DecimalField(max_digits=10, decimal_places=2)    
    colaborador = models.ForeignKey(Colaboradores, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargos, on_delete=models.CASCADE)