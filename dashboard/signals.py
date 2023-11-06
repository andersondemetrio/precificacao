from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cargos, Employee, AuxiliarCalculo
from django.db.models import Sum, Count
from django.db import transaction
from datetime import datetime, timedelta


def recalcula_encargos(sender, instance, **kwargs):
    salario_nominal = float(instance.salario)
    
    if instance.setor == "Gestores":
        periculosidade = 0
        rateio = 0
    else:
        periculosidade = salario_nominal * 0.3
        rateio = 0
        
    fgts = (salario_nominal + periculosidade) * 0.08
    terco_ferias = (salario_nominal + periculosidade) / 3 / 12
    fgts_ferias = terco_ferias * 0.08
    decimo_terceiro = (salario_nominal + periculosidade) / 12
    fgts_decimo_terceiro = decimo_terceiro * 0.08
    multa_rescisoria = (fgts + fgts_ferias + fgts_decimo_terceiro) * 0.4

    for employee in Employee.objects.filter(cargo=instance):
        employee.periculosidade = periculosidade
        employee.fgts = fgts
        employee.um_terco_ferias = terco_ferias
        employee.fgts_ferias = fgts_ferias
        employee.decimo_terceiro = decimo_terceiro
        employee.fgts_decimo_terceiro = fgts_decimo_terceiro
        employee.multa_rescisoria = multa_rescisoria
        employee.custo_salario = (salario_nominal + periculosidade + fgts + terco_ferias +
                                 fgts_ferias + decimo_terceiro + fgts_decimo_terceiro +
                                 multa_rescisoria)
        employee.rateio = rateio
        employee.custo_mes = (employee.custo_salario + rateio)

        employee.save()
        atualizar_dados_banco()
        
def atualizar_dados_banco():
    # prestadores_count = Employee.objects.filter(setor='Prestador de Serviço').count()
    custo_prestadores = Employee.objects.filter(setor='Prestador de Serviço').aggregate(Sum('custo_salario'))['custo_salario__sum']
    custo_gestores = Employee.objects.filter(setor='Gestores').aggregate(Sum('custo_salario'))['custo_salario__sum']
    
    auxiliar_calculo, created = AuxiliarCalculo.objects.get_or_create(pk=1)
    if created:
        auxiliar_calculo.total_salarios_gestores = 0
        auxiliar_calculo.total_salarios_prestadores = 0
        # auxiliar_calculo.total_prestadores = 0
        auxiliar_calculo.save()
  
      
    if custo_prestadores is not None and custo_prestadores >= 0 and custo_gestores is not None:
        with transaction.atomic():
            employees = Employee.objects.all()
            for employee in employees:
                porcentagem = (employee.custo_salario * 100) / custo_prestadores

                if employee.setor == "Gestores":
                    rateio = 0
                else:
                    rateio = (porcentagem * custo_gestores) / 100
                    
                auxiliar_calculo.total_salarios_gestores = custo_gestores
                auxiliar_calculo.total_salarios_prestadores = custo_prestadores
                # auxiliar_calculo.total_prestadores = prestadores_count

                auxiliar_calculo.save()

                employee.rateio = rateio
                employee.custo_mes = employee.custo_salario + rateio
                employee.save()
                
    print(f'Custo Prestadores: {custo_prestadores}')
    print(f'Custo Gestores: {custo_gestores}')

    return {
        # 'prestadores_count': prestadores_count,
        'custo_prestadores': custo_prestadores,
        'custo_gestores': custo_gestores,
    }