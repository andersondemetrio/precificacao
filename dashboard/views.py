from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.http import HttpResponse
from django.core.paginator import Paginator

from django.core.mail import send_mail
from django.conf import settings
import random
from .models import GastosFixos,Colaboradores,Cargos, Endereco, Empresa,CalendarioMensal,Employee
import csv

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import io
from reportlab.lib.pagesizes import landscape, A3
from django.utils.encoding import smart_str
import codecs
from django.db.models import Sum, Count
from django.db import transaction
from datetime import datetime, timedelta
from django.dispatch import Signal
from .signals import *
from decimal import Decimal
from collections import defaultdict

from .signals import recalcula_encargos

@login_required
def dashboard_view(request):
    if request.session.get('empresa_cadastrada'):
        success = True
        # Limpar a variável de sessão após verificar
        request.session['empresa_cadastrada'] = False
    else:
        success = False

    context = {
        # ... seu contexto existente ...
        'success': success,
    }
    if request.user.is_authenticated:
        return render(request, 'dashboard1.html')
    else:
        return render(request, 'account/login.html', context)
    
# @login_required
def alterar_senha(request):
    if request.method == 'POST':
        nova_senha = request.POST.get('novaSenha')
        repetir_senha = request.POST.get('repetirSenha')

        if nova_senha == repetir_senha:
            user = request.user
            user.set_password(nova_senha)
            user.save()
            
            # Atualiza a sessão de autenticação para evitar logout automático
            # update_session_auth_hash(request, user)

            messages.success(request, 'Senha alterada com sucesso.')
            return redirect('login')
        else:
            messages.error(request, 'As senhas não coincidem.')
    return render(request, 'dashboard1.html', {'keep_modal_open': True})


# Funções do CRUD de Colaboradores

def inserir_mao_de_obra(request):
    if request.method == 'POST':
        matricula = request.POST['matricula']
        nome = request.POST['nome']
        cpf = request.POST['cpf']
        cargo_id = request.POST['cargo']

        cargo = Cargos.objects.get(id=cargo_id)
        
        mao_de_obra = Colaboradores(
            matricula=matricula,
            nome=nome,
            cpf=cpf.replace('.', '').replace('-', ''),
            cargo=cargo,  # Associando o cargo à mão de obra
        )
        mao_de_obra.save()
        return redirect('dashboard')
    return render(request, 'dashboard1.html')

def buscar_colaborador(request): 
    q = request.GET.get('search')   
    colaboradores = Colaboradores.objects.filter(nome__icontains=q).order_by('id')
    return render(request, 'pesquisa_colaborador.html', {'colaborador': colaboradores})

def colaboradores_vieww(request):
    colaboradores = Colaboradores.objects.all()
    colaboradores_list = [{'id': colaboradores.id, 'nome': colaboradores.nome, 'matricula': colaboradores.matricula, 'cargo': colaboradores.cargo} for colaborador in colaboradores]
    return JsonResponse({'colaboradores': colaboradores_list})

def detalhes_colaborador(request, id):
    colaborador = Colaboradores.objects.get(id=id)
    return render(request, 'detalhes_colaborador.html', {'colaborador':colaborador})

def editar_colaborador(request, id):
    colaborador = Colaboradores.objects.get(id=id)
    if request.method == 'POST':
        matricula = request.POST['matricula']
        nome = request.POST['nome']
        cpf = request.POST['cpf']
        cargo_id = request.POST['cargo']
        
        cargo = Cargos.objects.get(id=cargo_id)

        # Atualize os campos do colaborador existente
        colaborador.nome = nome
        colaborador.matricula = matricula
        colaborador.cpf = cpf
        colaborador.cargo = cargo
        colaborador.save()
        return redirect('dashboard')

    return render(request, 'dashboard1.html', {'colaborador': colaborador})

def deletar_colaborador(request, colaborador_id):
    if request.method == 'POST':
        try:
            colaborador = Colaboradores.objects.get(pk=colaborador_id)
            colaborador.delete()
            atualizar_dados_banco()
            return redirect('dashboard')
        except Colaboradores.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})
    else:
        try:
            colaborador = Colaboradores.objects.get(pk=colaborador_id)
            return render(request, 'confirm_delete.html')
        except colaborador.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})


# Funções do CRUD de cargos

def inserir_cargo(request):
    print("request.POST")
    if request.method == 'POST':
        nome_cargo = request.POST['nome_cargo']
        salario = request.POST['salario']


        cargo = Cargos(
            nome_cargo=nome_cargo,
            salario=salario,
        )   

        cargo.save()
        return redirect('dashboard')

    return render(request, 'dashboard1.html', context={})

def detalhes_cargo(request, id):
    cargo = Cargos.objects.get(id=id)
    return render(request, 'detalhes_cargo.html', {'cargo':cargo})

# def editar_cargo(request, id):
#     cargo = Cargos.objects.get(id=id)
#     if request.method == 'POST':
#         nome_cargo = request.POST.get('nome_cargo')
#         salario= request.POST.get('salario')

#         cargo.nome_cargo = nome_cargo
#         cargo.salario = salario        
#         cargo.save()
#         return redirect('dashboard')

#     return render(request, 'dashboard1.html', {'cargo': cargo})
def editar_cargo(request, id):
    cargo = Cargos.objects.get(id=id)
    if request.method == 'POST':
        nome_cargo = request.POST.get('nome_cargo')
        salario = request.POST.get('salario')
        setor = request.POST.get('setor')  # Supondo que você tenha um campo 'setor' em seu formulário

        # Antes de salvar as alterações, colete as informações relevantes do cargo
        nome_anterior = cargo.nome_cargo
        salario_anterior = cargo.salario

        cargo.nome_cargo = nome_cargo
        cargo.salario = salario
        cargo.setor = setor  # Atualize o setor do cargo

        cargo.save()  # Salve as alterações no cargo

        # Verifique se houve alterações no nome ou salário do cargo
        if nome_anterior != nome_cargo or salario_anterior != salario:
            # Chame o sinal manualmente para recalcular os encargos
            recalcula_encargos(sender=Cargos, instance=cargo)

        return redirect('dashboard')

    return render(request, 'dashboard1.html', {'cargo': cargo})


def cargos_vieww(request):
    cargos = Cargos.objects.all()
    cargos_list = [{'id': cargo.id, 'nome_cargo': cargo.nome_cargo, 'salario': cargo.salario} for cargo in cargos]
    return JsonResponse({'cargos': cargos_list})

def buscar_cargo(request): 
    q = request.GET.get('search')   
    cargos = Cargos.objects.filter(nome_cargo__icontains=q).order_by('id')
    return render(request, 'pesquisa_cargo.html', {'cargo': cargos})

def deletar_cargo(request, cargo_id):
    if request.method == 'POST':
        try:
            cargo = Cargos.objects.get(pk=cargo_id)
            cargo.delete()
            atualizar_dados_banco()
            return redirect('dashboard')
        except Cargos.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})
    else:
        try:
            cargo = Cargos.objects.get(pk=cargo_id)
            return render(request, 'confirm_delete.html')
        except cargo.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})


# Funções do CRUD de endereços

def inserir_endereco(request):
    if request.method == 'POST':
        cep = request.POST['cep']
        logradouro = request.POST['logradouro']
        numero = request.POST['numero']
        complemento = request.POST['complemento']
        bairro = request.POST['bairro']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        Endereco.objects.create(cep=cep, logradouro=logradouro, numero=numero, complemento=complemento, bairro=bairro, cidade=cidade, 
                                estado=estado)
        return redirect('dashboard')
    return render(request, 'dashboard1.html', context={})

def endereco_view(request):
    enderecos = Endereco.objects.all()
    enderecos_list = [
        {
            'id': endereco.id,
            'endereco': f"{endereco.logradouro}, {endereco.numero}, {endereco.complemento}, {endereco.bairro}, {endereco.cidade}, {endereco.estado}"
        }
        for endereco in enderecos
    ]
    return JsonResponse({'enderecos': enderecos_list})

def detalhes_endereco(request, id):
    endereco = Endereco.objects.get(id=id)
    return render(request, 'detalhes_endereco.html', {'endereco':endereco})

def buscar_endereco(request): 
    q = request.GET.get('search')   
    endereco = Endereco.objects.filter(logradouro__icontains=q).order_by('id')
    return render(request, 'pesquisa_endereco.html', {'endereco': endereco})

def editar_endereco(request, id):
    endereco = Endereco.objects.get(id=id)
    if request.method == 'POST':
        # cep = request.POST['cep']
        logradouro = request.POST['logradouro']
        numero = request.POST['numero']
        complemento = request.POST['complemento']
        bairro = request.POST['bairro']
        cidade = request.POST['cidade']
        estado = request.POST['estado']

        # endereco.cep = cep
        endereco.logradouro = logradouro
        endereco.numero = numero
        endereco.complemento = complemento
        endereco.bairro = bairro
        endereco.cidade = cidade
        endereco.estado = estado      
        endereco.save()
        
        return redirect('dashboard')

    return render(request, 'dashboard1.html', {'endereco': endereco})

def deletar_endereco(request, endereco_id):
    if request.method == 'POST':
        try:
            endereco = Endereco.objects.get(pk=endereco_id)
            endereco.delete()
            return redirect('dashboard')
        except Endereco.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})
    else:
        try:
            endereco = Endereco.objects.get(pk=endereco_id)
            return render(request, 'confirm_delete.html')
        except endereco.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})


# Funções do CRUD de Empresa

def inserir_empresa(request):
    if request.method == 'POST':
        cnpj = request.POST['cnpj']
        numero_empresa = request.POST['numero_empresa']
        nome_empresa = request.POST['nome_empresa']
        nome_fantasia = request.POST['nome_fantasia']
        email = request.POST['email']
        telefone = request.POST['telefone']
        ativa = request.POST.get('ativa') == 'on'  # Verifica se a checkbox foi marcada
        endereco_id = request.POST['endereco']

        empresa = Empresa(
            cnpj=cnpj,
            numero_empresa=numero_empresa,
            nome_empresa=nome_empresa,
            nome_fantasia=nome_fantasia,
            email=email,
            telefone=telefone,
            ativa=ativa,
            endereco_id=endereco_id
        )
                
        empresa.save()
        # request.session['empresa_cadastrada'] = True
        return redirect('dashboard')

    return render(request, 'dashboard1.html', context={})

def empresa_view(request):
    empresa = Empresa.objects.all()
    empresa_list = [
        {
            'id': empresa.id,
            'empresa': f"{empresa.cnpj}, {empresa.numero_empresa}, {empresa.nome_empresa}, {empresa.nome_fantasia}, {empresa. email}, {empresa.telefone}, {empresa.endereco} "
        }
        for empresa in empresa
    ]
    return JsonResponse({'empresa': empresa_list})

def detalhes_empresa(request, id):
    empresa = Empresa.objects.get(id=id)
    return render(request, 'detalhes_empresa.html', {'empresa':empresa})

def buscar_empresa(request): 
    q = request.GET.get('search')   
    empresa = Empresa.objects.filter(nome_empresa__icontains=q).order_by('id')
    return render(request, 'pesquisa_empresa.html', {'empresa': empresa})

def editar_empresa(request, id):
    empresa = Empresa.objects.get(id=id)
    if request.method == 'POST':
        # cnpj = request.POST['cnpj']
        numero_empresa = request.POST['numero_empresa']
        nome_empresa = request.POST['nome_empresa']
        nome_fantasia = request.POST['nome_fantasia']
        email = request.POST['email']
        telefone = request.POST['telefone']
        ativa = request.POST.get('ativa') == 'on'  # Verifica se a checkbox foi marcada
        endereco_id = request.POST['endereco']

        # empresa.cnpj = cnpj
        empresa.numero_empresa = numero_empresa
        empresa.nome_empresa = nome_empresa
        empresa.nome_fantasia = nome_fantasia
        empresa.email = email
        empresa.telefone = telefone
        empresa.ativa = ativa
        empresa.endereco_id = endereco_id                  
        empresa.save()

        return redirect('dashboard')

    return render(request, 'dashboard1.html', {'empresa': empresa})

def deletar_empresa(request, empresa_id):
    if request.method == 'POST':
        try:
            empresa = Empresa.objects.get(pk=empresa_id)
            empresa.delete()
            return redirect('dashboard')
        except Empresa.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})
    else:
        try:
            empresa = Empresa.objects.get(pk=empresa_id)
            return render(request, 'confirm_delete.html')
        except empresa.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})


# Funções do CRUD de Calendario

def inserir_calendario(request):
    if request.method == "POST":
        mes = int(request.POST.get("mes"))
        ano = int(request.POST.get("ano"))
        jornada_diaria = float(request.POST.get("jornada_diaria"))
        funcionario_id = int(request.POST.get("funcionario"))
        horas_produtivas = float(request.POST.get("horas_produtivas"))
        dias_uteis = int(request.POST.get("dias_uteis"))  # Pegar o valor dos dias úteis

        funcionario = Colaboradores.objects.get(pk=funcionario_id)

        calendario = CalendarioMensal(
            mes=mes,
            ano=ano,
            jornada_diaria=jornada_diaria,
            funcionario=funcionario,
            horas_produtivas=horas_produtivas,
            dias_uteis=dias_uteis  # Definir o valor dos dias úteis
        )
        calendario.save()
        calcular_media_horas_produtivas(request)

        return redirect("dashboard")  # Redirecionar para uma página de sucesso

    return render(request, "dashboard1.html")

def calendario_view(request):
    calendarios = CalendarioMensal.objects.all()
    calendario_list = [
        {
            'id': calendario.id,
            'calendario': f"{calendario.mes}, {calendario.ano}, {calendario.funcionario}, {calendario.dias_uteis}, {calendario. jornada_diaria}, {calendario.horas_produtivas} "
        }
        for calendario in calendarios
    ]
    return JsonResponse({'calendario': calendario_list})

def detalhes_calendario(request, id):
    calendario = CalendarioMensal.objects.get(id=id)
    return render(request, 'detalhes_calendario.html', {'calendario':calendario})

def buscar_calendario(request): 
    q = request.GET.get('search')   
    calendario = CalendarioMensal.objects.filter(ano__icontains=q).order_by('funcionario__nome', 'ano', 'mes')
    return render(request, 'pesquisa_calendario.html', {'calendario': calendario})

def editar_calendario(request, id):
    calendario = CalendarioMensal.objects.get(id=id)
    if request.method == "POST":
        mes = int(request.POST['mes'])
        ano = int(request.POST.get("ano"))
        jornada_diaria = float(request.POST.get("jornada_diaria"))
        funcionario_id = int(request.POST.get("funcionario"))
        horas_produtivas = float(request.POST.get("horas_produtivas"))
        dias_uteis = int(request.POST.get("dias_uteis"))  # Pegar o valor dos dias úteis

        funcionario = Colaboradores.objects.get(pk=funcionario_id)

        calendario.mes = mes
        calendario.ano = ano
        calendario.jornada_diaria = jornada_diaria
        calendario.funcionario = funcionario
        calendario.horas_produtivas = horas_produtivas
        calendario.dias_uteis = dias_uteis         
        calendario.save()
        calcular_media_horas_produtivas(request)

        return redirect("dashboard")  # Redirecionar para uma página de sucesso

    return render(request, 'dashboard1.html', {'calendario': calendario})

def deletar_calendario(request, calendario_id):
    if request.method == 'POST':
        try:
            calendario = CalendarioMensal.objects.get(pk=calendario_id)
            calendario.delete()
            calcular_media_horas_produtivas(request)
            return redirect('dashboard')
        except CalendarioMensal.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})
    else:
        try:
            calendario = CalendarioMensal.objects.get(pk=calendario_id)
            return render(request, 'confirm_delete.html')
        except CalendarioMensal.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})
        

# Funções do CRUD de Despesas Condominio

def inserir_gasto_fixo(request):
    if request.method == 'POST':
        descricao = request.POST['descricao']
        valor = request.POST['valor']
        mes = request.POST['mes']
        ano = request.POST['ano']
        escolha = request.POST['escolha']

        if escolha  == 'totalMes':
            tipo = 'Total Mês'
        else:
            tipo = 'Lista Mês'
            
        gasto_fixo = GastosFixos(descricao=descricao, valor=valor, mes=mes, ano=ano, tipo=tipo)
        gasto_fixo.save()
        calcular_gastos_ultimos_12_meses(request)

        
        return redirect('dashboard')
    return render(request, 'dashboard1.html', context={})

def gasto_fixo_view(request):
    gastosfixos = GastosFixos.objects.all()
    gasto_list = [
        {
            'id': gasto.id,
            'gasto': f"{gasto.descricao}, {gasto.valor}, {gasto.mes}, {gasto.ano} "
        }
        for gasto in gastosfixos
    ]
    return JsonResponse({'gasto': gasto_list})

def detalhes_gasto_fixo(request, id):
    gastosfixos = GastosFixos.objects.get(id=id)
    return render(request, 'detalhes_gasto_fixo.html', {'gastosfixos':gastosfixos})

def buscar_gasto_fixo(request): 
    q = request.GET.get('search')   
    gastosfixos = GastosFixos.objects.filter(descricao__icontains=q).order_by('ano', 'mes')
    return render(request, 'pesquisa_gasto_fixo.html', {'gastosfixos': gastosfixos})

def editar_gasto_fixo(request, id):
    gastosfixos = GastosFixos.objects.get(id=id)
    if request.method == "POST":
        descricao = request.POST['descricao']
        valor = request.POST['valor']
        mes = request.POST['mes']
        ano = request.POST['ano']
        escolha = request.POST['escolha']


        gastosfixos.mes = mes
        gastosfixos.ano = ano
        gastosfixos.descricao = descricao
        gastosfixos.valor = valor
        gastosfixos.tipo = escolha   
        gastosfixos.save()
        calcular_gastos_ultimos_12_meses(request)

        return redirect("dashboard")  # Redirecionar para uma página de sucesso

    return render(request, 'dashboard1.html', {'gastosfixos': gastosfixos})

def deletar_gasto_fixo(request, gasto_fixo_id):
    if request.method == 'POST':
        try:
            gastosfixos = GastosFixos.objects.get(pk=gasto_fixo_id)
            gastosfixos.delete()
            calcular_gastos_ultimos_12_meses(request)
            return redirect('dashboard')
        except GastosFixos.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})
    else:
        try:
            gastosfixos = GastosFixos.objects.get(pk=gasto_fixo_id)
            return render(request, 'confirm_delete.html')
        except GastosFixos.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})
        

#Funções do CRUD de Encargo

def inserir_encargo(request):
    if request.method == 'POST':
        colaborador_id = request.POST['funcionario']
        cargo_id = request.POST['cargos']
        colaborador = Colaboradores.objects.get(id=colaborador_id)
        cargo = Cargos.objects.get(id=cargo_id)
        setor = request.POST['setor']
        # cargo = request.POST['cargo']

        # Verificar se já existe um encargo para o mesmo colaborador, setor e cargo
        if Employee.objects.filter(colaborador=colaborador, setor=setor, cargo=cargo).exists():
            # Lidar com encargo já existente (pode ser uma renderização de erro ou outra ação)
            return render(request, 'encargo_duplicado.html')

        # Cálculo do salário nominal
        salario_nominal = float(cargo.salario)
        
        # Definir valores padrão para periculosidade e rateio
        periculosidade = 0
        rateio = 0

        # Verificar se o setor é "Gestores" e ajustar a periculosidade e rateio
        if setor == "Gestores":
            periculosidade = 0
            rateio = 0
        else:
            periculosidade = salario_nominal * 0.3
            rateio = 0 

        # Cálculos dos outros campos...
        fgts = (salario_nominal + periculosidade) * 0.08
        terco_ferias = (salario_nominal + periculosidade)/3 / 12
        fgts_ferias = terco_ferias * 0.08
        decimo_terceiro = (salario_nominal + periculosidade) / 12
        fgts_decimo_terceiro = decimo_terceiro * 0.08
        multa_rescisoria = (fgts + fgts_ferias + fgts_decimo_terceiro) * 0.4
        custo_salario = (salario_nominal + periculosidade + fgts + terco_ferias +
                     fgts_ferias + decimo_terceiro + fgts_decimo_terceiro +
                     multa_rescisoria)
        custo_mes = (custo_salario + rateio)

        # Criação do registro na tabela Employee e redirecionamento após a inserção
        employee = Employee.objects.create(
            colaborador=colaborador,
            setor=setor,
            cargo=cargo,
            periculosidade=periculosidade,
            fgts=fgts,
            um_terco_ferias=terco_ferias,
            fgts_ferias=fgts_ferias,
            decimo_terceiro=decimo_terceiro,
            fgts_decimo_terceiro=fgts_decimo_terceiro,
            multa_rescisoria=multa_rescisoria,
            custo_salario=custo_salario,
            rateio=rateio,
            custo_mes=custo_mes,
        )
        atualizar_dados_banco()
        # Redirecionar para a página desejada após a inserção
        return redirect('dashboard')
    
    return render(request, 'dashboard1.html')

def buscar_encargo(request): 
    q = request.GET.get('search')   
    encargo = Employee.objects.filter(setor__icontains=q).order_by('id')
    return render(request, 'pesquisa_encargo.html', {'encargo': encargo})

def encargo_view(request):
    encargo = Employee.objects.all()
    encargo_list = [
        {
            'id': encargo.id,
            'encargo': f"{encargo.id}, {encargo.setor}"
        }
        for encargo in encargo
    ]
    return JsonResponse({'encargo': encargo_list})

def deletar_encargo(request, encargo_id):
    if request.method == 'POST':
        try:
            encargo = Employee.objects.get(pk=encargo_id)
            encargo.delete()
            atualizar_dados_banco()
            return redirect('dashboard')
        except Employee.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})
    else:
        try:
            encargo = Employee.objects.get(pk=encargo_id)
            return render(request, 'confirm_delete.html')
        except Employee.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})


#Funções do CRUD de Beneficios

def inserir_beneficio(request):
    return render(request, 'dashboard1.html', context={})

def buscar_beneficio(request): 
    q = request.GET.get('search')   
    beneficio = Beneficios.objects.filter(descricao__icontains=q).order_by('id')
    return render(request, 'pesquisa_beneficio.html', {'beneficio': beneficio})

def beneficio_view(request):
    beneficio = Beneficios.objects.all()
    beneficio_list = [
        {
            'id': beneficio.id,
            'beneficio': f"{beneficio.id}"
        }
        for beneficio in beneficio
    ]
    return JsonResponse({'beneficio': beneficio_list})

def deletar_beneficio(request, beneficio_id):
    if request.method == 'POST':
        try:
            beneficio = Beneficios.objects.get(pk=beneficio_id)
            beneficio.delete()
            return redirect('dashboard')
        except Beneficios.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})
    else:
        try:
            beneficio = Beneficios.objects.get(pk=beneficio_id)
            return render(request, 'confirm_delete.html')
        except Beneficios.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})



def inserir_data(request):
    return render(request, 'dashboard1.html', context={})    

def inserir_jornada(request):
    return render(request, 'dashboard1.html', context={})

def inserir_horas(request):
    return render(request, 'dashboard1.html', context={})       


# funçaõ para listar os colaboradores no select do calendario
def colaboradores_view(request):
    colaboradores = Colaboradores.objects.all()
    colaboradores_list = [{'id': colaborador.id, 'nome': colaborador.nome} for colaborador in colaboradores]
    return JsonResponse({'colaboradores': colaboradores_list})


# Função para listar os encargos dos colaboradores
def lista_salarios_view(request):
    employees = Employee.objects.select_related('colaborador').all()

    context = {
        'employees': employees
    }

    return render(request, 'lista_salarios.html', context)

# Função para exportar os encargos para o CSV
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="encargos_funcionarios.csv"'

    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Colaborador', 'Salário', 'Setor', 'Cargo', 'Periculosidade', 'FGTS', '1/3 Férias', 'FGTS Férias', 
                     '13º Salário', 'FGTS 13º', 'Multa Rescisória', 'Custo Salário', 'Rateio', 'Custo Mês'])

    employees = Employee.objects.all()  # Use apropriate queryset here
    for employee in employees:
        writer.writerow([employee.colaborador.nome, employee.cargo.salario, employee.setor, employee.cargo.nome_cargo, employee.periculosidade, 
                         employee.fgts, employee.um_terco_ferias, employee.fgts_ferias, employee.decimo_terceiro, employee.fgts_decimo_terceiro, 
                         employee.multa_rescisoria, employee.custo_salario, employee.rateio, employee.custo_mes])

    return response


# funcão para exportar os encargos para o PDF
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="salaries.pdf"'

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A3))

    data = []
    employees = Employee.objects.all()  # Use appropriate queryset here

    # Adicionar os nomes das colunas como a primeira linha dos dados
    data.append([
        'Colaborador', 'Salário', 'Setor', 'Cargo', 'Periculosidade', 'FGTS',
        '1/3 Férias', 'FGTS Férias', '13º Salário', 'FGTS 13º',
        'Multa Rescisória', 'Custo Salário', 'Rateio', 'Custo Mês'
    ])

    for employee in employees:
        data.append([
            employee.colaborador.nome,
            f"R$ {employee.cargo.salario:.2f}",
            employee.setor,
            employee.cargo.nome_cargo,
            f"R$ {employee.periculosidade:.2f}",
            f"R$ {employee.fgts:.2f}",
            f"R$ {employee.um_terco_ferias:.2f}",
            f"R$ {employee.fgts_ferias:.2f}",
            f"R$ {employee.decimo_terceiro:.2f}",
            f"R$ {employee.fgts_decimo_terceiro:.2f}",
            f"R$ {employee.multa_rescisoria:.2f}",
            f"R$ {employee.custo_salario:.2f}",
            f"R$ {employee.rateio:.2f}",
            f"R$ {employee.custo_mes:.2f}"
        ])

    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    table.setStyle(style)
    elements = [table]

    doc.build(elements)
    response.write(buffer.getvalue())
    buffer.close()

    return response
#create a function to list all the employees

def list_employee(request):
    employees = Colaboradores.objects.all()
    return render(request, 'list_employee.html', {'employees': employees})


# Função para calcular gastos com condominio
def calcular_gastos_ultimos_12_meses(request):
    data_atual = datetime.now()
    
    resultados = []
    total_gastos_12_meses = 0
    quantidadeMeses = 0
    
    data_inicio = data_atual - timedelta(days=365)
    
    auxiliar_calculo, created = AuxiliarCalculo.objects.get_or_create(pk=1)
    if created:
        auxiliar_calculo.total_meses_condominio = 0
        auxiliar_calculo.total_gastos_condominio = 0
        auxiliar_calculo.save()


    # Loop para obter os 12 últimos meses e calcular os gastos totais
    for i in range(12):
        # Calcule o mês e o ano para o mês atual
        mes = (data_inicio.month + i) % 12
        ano = data_inicio.year + ((data_inicio.month + i) // 12)  # Ajuste do ano
        
        # Certifique-se de que o mês está dentro do intervalo correto (1 a 12)
        if mes <= 0:
            mes += 12
            ano -= 1
        
        # Calcule o primeiro dia e o último dia do mês
        primeiro_dia = datetime(ano, mes, 1)
        ultimo_dia = primeiro_dia + timedelta(days=31)
        
        # Consulte o banco de dados para obter os gastos fixos do mês atual e some os valores
        gastos_mensais = GastosFixos.objects.filter(mes=mes, ano=ano).aggregate(Sum('valor'))['valor__sum']
        
        # Adicione os resultados à lista
        resultados.append({
            'mes': mes,
            'ano': ano,
            'total_gastos': gastos_mensais or 0  # Se não houver gastos, defina como zero
        })
        
        total_gastos_12_meses += gastos_mensais or 0
        
        if gastos_mensais and gastos_mensais != 0:
            quantidadeMeses += 1
            
            
        auxiliar_calculo.total_meses_condominio = quantidadeMeses
        auxiliar_calculo.total_gastos_condominio = total_gastos_12_meses
        auxiliar_calculo.save()
        
    # Imprima os resultados no console
    for resultado in resultados:
        print(f'Mês: {resultado["mes"]} / Ano: {resultado["ano"]} / Total de Gastos: {resultado["total_gastos"]}')
    print(f'Soma Total de Gastos: {total_gastos_12_meses}')
    print(f'Quantidade de Meses com Gastos: {quantidadeMeses}')
    
    response_data = {
        'total_gastos_12_meses': total_gastos_12_meses
    }

    return JsonResponse(response_data)

# Função para listar as horas condomínios
def lista_horas_condiminio_view(request):
    auxiliar_calculo = AuxiliarCalculo.objects.first() 
    return render(request, 'lista_condominio.html', {'auxiliar_calculo': auxiliar_calculo})

from datetime import datetime, timedelta
from django.db.models import Sum
from django.http import JsonResponse
from .models import CalendarioMensal

def calcular_media_horas_produtivas(request): 
    data_atual = datetime.now()
    
    resultados = []
    total_horas_produtivas = 0
    quantidade_meses = 0
    quantidade_registros = 0
    
    data_inicio = data_atual - timedelta(days=365)
    
    auxiliar_calculo, created = AuxiliarCalculo.objects.get_or_create(pk=1)
    if created:
        auxiliar_calculo.total_meses_calendario = 0
        auxiliar_calculo.total_meses_horasprodutivas = 0
        auxiliar_calculo.save()

    # Dicionário para armazenar as horas produtivas de cada mês
    horas_por_mes = defaultdict(list)
    
    # Loop para obter os 12 últimos meses e calcular as horas produtivas médias
    for i in range(12):
        # Calcule o mês e o ano para o mês atual
        mes = (data_inicio.month + i) % 12
        ano = data_inicio.year + ((data_inicio.month + i) // 12)  # Ajuste do ano
        
        # Certifique-se de que o mês está dentro do intervalo correto (1 a 12)
        if mes <= 0:
            mes += 12
            ano -= 1
            
        # Calcule o primeiro dia e o último dia do mês
        primeiro_dia = datetime(ano, mes, 1)
        ultimo_dia = primeiro_dia + timedelta(days=31)
        
        # Consulte o banco de dados para obter os registros do mês atual
        registros_do_mes = CalendarioMensal.objects.filter(mes=mes, ano=ano)
        
        for registro in registros_do_mes:
            horas_produtivas = registro.horas_produtivas
            horas_por_mes[(ano, mes)].append(horas_produtivas)
            quantidade_registros += 1
        
        # Calcule a média de horas produtivas para cada mês
    for (ano, mes), horas_lista in horas_por_mes.items():
        total_horas_mes = sum(horas_lista)
        quantidade_meses += 1

        media_mes = total_horas_mes / len(horas_lista) if len(horas_lista) > 0 else 0
        
        resultados.append({
            'mes': mes,
            'ano': ano,
            'media_horas_produtivas': media_mes
        })
        
    # Calcule a média anual das médias mensais
    media_anual = sum([resultado['media_horas_produtivas'] for resultado in resultados]) / quantidade_meses if quantidade_meses > 0 else 0

    auxiliar_calculo.total_meses_calendario = quantidade_meses
    auxiliar_calculo.total_meses_horasprodutivas = media_anual
    auxiliar_calculo.save()
        
    # Imprima os resultados no console
    for resultado in resultados:
        print(f'Mês: {resultado["mes"]} / Ano: {resultado["ano"]} / Média de Horas Mês: {resultado["media_horas_produtivas"]}')
    print(f'Quantidade Total de Registros: {quantidade_registros}')
    print(f'Quantidade Meses com Registros: {quantidade_meses}')
    print(f'Média Anual de Horas Produtivas: {media_anual}')
    
    response_data = {
        'resultados': resultados
    }

    return JsonResponse(response_data)

# Verifica se o CPF não existe
def verificar_cpf(request):
    cpf = request.GET.get('cpf')
    if Colaboradores.objects.filter(cpf=cpf).exists():
        return JsonResponse({'cpf_existe': True})
    else:
        return JsonResponse({'cpf_existe': False})

# Verifica se o CPF não existe
def verificar_cnpj(request):
    cnpj = request.GET.get('cnpj')
    print(f"Valor {cnpj}")
    if Empresa.objects.filter(cnpj=cnpj).exists():
        return JsonResponse({'cnpj_existe': True})
    else:
        return JsonResponse({'cnpj_existe': False})

def verificar_email(request):
    email = request.GET.get('email')
    print(email)
    if Empresa.objects.filter(email=email).exists():
        print(email)
        return JsonResponse({'email_existe': True})
        
    
    else: 
        print(email)
        return JsonResponse({'email_existe': False})