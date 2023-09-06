from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cargos, Employee  # Importe Employee


def recalcula_encargos(sender, instance, **kwargs):
    # Acesse as informações relevantes do cargo
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

    # Atualize os encargos para os colaboradores associados a este cargo
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
