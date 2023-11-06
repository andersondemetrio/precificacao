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
from django.urls import reverse
from .forms import EmailForm
from django.utils import timezone
import tempfile
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.http import HttpResponseServerError
import json

from django.core.mail import send_mail
from django.conf import settings
import random
from .models import GastosFixos, Colaboradores, Cargos, Endereco, Empresa, CalendarioMensal, Employee, Beneficios, DescricaoObra, Rubrica, DespesasDinamicas
import csv

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
import io
from reportlab.lib.pagesizes import landscape, A3
from django.utils.encoding import smart_str
import codecs
from django.db.models import Sum, Count
from django.db import transaction
from datetime import datetime
from datetime import datetime, timedelta
from django.dispatch import Signal
from .signals import *
from decimal import Decimal
from collections import defaultdict
from django.core.mail import EmailMessage
from .signals import recalcula_encargos

from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from io import BytesIO
from django.db.models import Q

import tempfile
from reportlab.lib.pagesizes import landscape, A3
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from django.http import HttpResponse

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import connection
from django.http import HttpResponseServerError
from django.db.models import F, Sum
import xlsxwriter
import io
from django.http import FileResponse

@login_required
def dashboard_view(request):
    if request.session.get('empresa_cadastrada'):
        success = True
        request.session['empresa_cadastrada'] = False
    else:
        success = False

    context = {
        'success': success,
    }
    if request.user.is_authenticated:
        try:
            colaborador = Colaboradores.objects.get(usuario=request.user)
            nome = colaborador.nome
        except Colaboradores.DoesNotExist:
            nome = request.user.username
            
        context = {'nome_usuario': nome}
        return render(request, 'dashboard1.html', context)
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

        cpf = cpf.replace('.', '').replace('-', '')

        if len(cpf) == 11:
            if not Colaboradores.objects.filter(cpf=cpf):
                empresa_do_admin = request.user.colaboradores.empresa_id
                mao_de_obra = Colaboradores(
                    matricula=matricula,
                    nome=nome,
                    cpf=cpf,
                    empresa_id=empresa_do_admin,
                )
                mao_de_obra.save()
                return redirect('dashboard')
            else:
                error_message = "Já existe um registro com o mesmo CPF."
                return render(request, 'dashboard1.html', {'error_message': error_message})
        else:
            error_message = "CPF inválido. Deve conter exatamente 11 caracteres."
            return render(request, 'dashboard1.html', {'error_message': error_message})
    
    return render(request, 'dashboard1.html')


def buscar_colaborador(request):
    colaborador_logado = request.user.colaboradores
    empresa_id_colaborador = colaborador_logado.empresa.id 
    
    q = request.GET.get('search')   
    colaboradores = Colaboradores.objects.filter(Q(nome__icontains=q)& Q(empresa_id=empresa_id_colaborador)).order_by('id')
    return render(request, 'pesquisa_colaborador.html', {'colaborador': colaboradores})


def colaboradores_vieww(request):
    colaboradores = Colaboradores.objects.all()
    colaboradores_list = [{'id': colaboradores.id, 'nome': colaboradores.nome, 'matricula': colaboradores.matricula, 'cargo': colaboradores.cargo, 'setor': colaboradores.setor} for colaborador in colaboradores]
    return JsonResponse({'colaboradores': colaboradores_list})


def detalhes_colaborador(request, id):
    colaborador = Colaboradores.objects.get(id=id)
    return render(request, 'detalhes_colaborador.html', {'colaborador':colaborador})


def editar_colaborador(request, id):
    colaborador = Colaboradores.objects.get(id=id)
    if request.method == 'POST':
        matricula = request.POST['matricula']
        nome = request.POST['nome']

        colaborador.nome = nome
        colaborador.matricula = matricula
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
    administrador_logado = request.user.colaboradores
    empresa_do_admin = administrador_logado.empresa_id
    
    if request.method == 'POST':
        nome_cargo = request.POST['nome_cargo']
        salario = request.POST['salario']

        cargo = Cargos(
            nome_cargo=nome_cargo,
            salario=salario,
            empresa_id=empresa_do_admin,
        )   

        cargo.save()
        return redirect('dashboard')

    return render(request, 'dashboard1.html', context={})


def detalhes_cargo(request, id):
    cargo = Cargos.objects.get(id=id)
    return render(request, 'detalhes_cargo.html', {'cargo':cargo})


def editar_cargo(request, id):
    cargo = Cargos.objects.get(id=id)
    if request.method == 'POST':
        nome_cargo = request.POST.get('nome_cargo')
        salario = request.POST.get('salario')
        setor = request.POST.get('setor')

        nome_anterior = cargo.nome_cargo
        salario_anterior = cargo.salario

        cargo.nome_cargo = nome_cargo
        cargo.salario = salario
        cargo.setor = setor

        cargo.save()

        if nome_anterior != nome_cargo or salario_anterior != salario:
            recalcula_encargos(sender=Cargos, instance=cargo)

        return redirect('dashboard')

    return render(request, 'dashboard1.html', {'cargo': cargo})


def cargos_vieww(request):
    cargos = Cargos.objects.all()
    cargos_list = [{'id': cargo.id, 'nome_cargo': cargo.nome_cargo, 'salario': cargo.salario} for cargo in cargos]
    return JsonResponse({'cargos': cargos_list})


def buscar_cargo(request):
    colaborador_logado = request.user.colaboradores
    empresa_id_colaborador = colaborador_logado.empresa.id 
    
    q = request.GET.get('search')   
    
    cargos = Cargos.objects.filter(Q(nome_cargo__icontains=q) & Q(empresa_id=empresa_id_colaborador)).order_by('id')
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
    administrador_logado = request.user.colaboradores
    empresa_do_admin = administrador_logado.empresa_id
    
    if request.method == 'POST':
        cep = request.POST['cep']
        logradouro = request.POST['logradouro']
        numero = request.POST['numero']
        complemento = request.POST['complemento']
        bairro = request.POST['bairro']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        Endereco.objects.create(cep=cep, logradouro=logradouro, numero=numero, complemento=complemento, bairro=bairro, cidade=cidade, 
                                estado=estado,empresa_endereco_id=empresa_do_admin)
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
    colaborador_logado = request.user.colaboradores
    empresa_id_colaborador = colaborador_logado.empresa.id
     
    q = request.GET.get('search')
       
    endereco = Endereco.objects.filter(Q(logradouro__icontains=q) & Q(empresa_endereco_id=empresa_id_colaborador)).order_by('id')
    return render(request, 'pesquisa_endereco.html', {'endereco': endereco})


def editar_endereco(request, id):
    endereco = Endereco.objects.get(id=id)
    if request.method == 'POST':
        logradouro = request.POST['logradouro']
        numero = request.POST['numero']
        complemento = request.POST['complemento']
        bairro = request.POST['bairro']
        cidade = request.POST['cidade']
        estado = request.POST['estado']

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
        ativa = request.POST.get('ativa') == 'on'
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
    colaborador_logado = request.user.colaboradores
    empresa_id_colaborador = colaborador_logado.empresa.id 
    
    q = request.GET.get('search')   
    empresa = Empresa.objects.filter(Q(nome_empresa__icontains=q)& Q(id=empresa_id_colaborador)).order_by('id')
    return render(request, 'pesquisa_empresa.html', {'empresa': empresa})


def editar_empresa(request, id):
    empresa = Empresa.objects.get(id=id)
    if request.method == 'POST':
        numero_empresa = request.POST['numero_empresa']
        nome_empresa = request.POST['nome_empresa']
        nome_fantasia = request.POST['nome_fantasia']
        email = request.POST['email']
        telefone = request.POST['telefone']
        ativa = request.POST.get('ativa') == 'on'
        endereco_id = request.POST['endereco']

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
        dias_uteis_str = request.POST.get("dias_uteis")
        dias_uteis_str = dias_uteis_str.replace(",", ".")
        feriado = float(request.POST.get("feriados"))

        dias_uteis = float(dias_uteis_str)
        print(dias_uteis)

        funcionario = Colaboradores.objects.get(pk=funcionario_id)

        calendario = CalendarioMensal(
            mes=mes,
            ano=ano,
            jornada_diaria=jornada_diaria,
            funcionario=funcionario,
            horas_produtivas=horas_produtivas,
            dias_uteis=round(dias_uteis - feriado, 2),
            feriado=feriado
        )
        print(dias_uteis)
        calendario.save()
        calcular_media_horas_produtivas(request)

        return redirect("dashboard")

    return render(request, "dashboard1.html")


def calendario_view(request):
    calendarios = CalendarioMensal.objects.all()
    calendario_list = [
        {
            'id': calendario.id,
            'calendario': f"{calendario.ano}, {calendario.mes}, {calendario.descricao}, {calendario.dias_uteis}, {calendario. jornada_diaria}, {calendario.horas_produtivas} "
        }
        for calendario in calendarios
    ]
    return JsonResponse({'calendario': calendario_list})


def detalhes_calendario(request, id):
    calendario = CalendarioMensal.objects.get(id=id)
    return render(request, 'detalhes_calendario.html', {'calendario':calendario})


def buscar_calendario(request):
    colaborador_logado = request.user.colaboradores
    empresa_id_colaborador = colaborador_logado.empresa.id 
    
    q = request.GET.get('searchCal')   
    
    calendario = CalendarioMensal.objects.filter(Q(ano__icontains=q)& Q(empresa_id=empresa_id_colaborador)).order_by('ano', 'mes')
    return render(request, 'pesquisa_calendario.html', {'calendario': calendario})
        

# Funções do CRUD de Despesas Condominio

def inserir_gasto_fixo(request):
    administrador_logado = request.user.colaboradores
    empresa_do_admin = administrador_logado.empresa_id
    
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
            
        gasto_fixo = GastosFixos(descricao=descricao, valor=valor, mes=mes, ano=ano, tipo=tipo, empresa_id=empresa_do_admin)
        gasto_fixo.save()
        calcular_gastos_ano_corrente(request)
        
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
    colaborador_logado = request.user.colaboradores
    empresa_id_colaborador = colaborador_logado.empresa.id
     
    q = request.GET.get('search')   
    gastosfixos = GastosFixos.objects.filter(Q(descricao__icontains=q)& Q(empresa_id=empresa_id_colaborador)).order_by('ano', 'mes')
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
        calcular_gastos_ano_corrente(request)

        return redirect("dashboard")

    return render(request, 'dashboard1.html', {'gastosfixos': gastosfixos})


def deletar_gasto_fixo(request, gasto_fixo_id):
    if request.method == 'POST':
        try:
            gastosfixos = GastosFixos.objects.get(pk=gasto_fixo_id)
            gastosfixos.delete()
            calcular_gastos_ano_corrente(request)
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
    administrador_logado = request.user.colaboradores
    empresa_do_admin = administrador_logado.empresa_id
    
    if request.method == 'POST':
        colaborador_id = request.POST['funcionario']
        cargo_id = request.POST['cargos']
        colaborador = Colaboradores.objects.get(id=colaborador_id)
        cargo = Cargos.objects.get(id=cargo_id)
        setor = request.POST['setor']

        if Employee.objects.filter(colaborador=colaborador, setor=setor, cargo=cargo).exists():
            return render(request, 'encargo_duplicado.html')

        salario_nominal = float(cargo.salario)
        
        periculosidade = 0
        rateio = 0
        beneficios = 0

        if setor == "Gestores":
            periculosidade = 0
            rateio = 0
        else:
            periculosidade = salario_nominal * 0.3
            rateio = 0 

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
            beneficios=beneficios,
            rateio=rateio,
            custo_mes=custo_mes,
            empresa_id=empresa_do_admin,
        )
        
        colaborador.setor = setor
        colaborador.save() 
        calcular_soma_beneficio_funcionario(request)
        atualizar_dados_banco()
        return redirect('dashboard')
    
    return render(request, 'dashboard1.html')


def buscar_encargo(request):    
    colaborador_logado = request.user.colaboradores
    empresa_id_colaborador = colaborador_logado.empresa.id
    
    q = request.GET.get('search')
    encargo = Employee.objects.filter(empresa__id=empresa_id_colaborador)

    if q:
        if q.isdigit():
            encargo = encargo.filter(id=q)
        else:
            encargo = encargo.filter(
                Q(colaborador__nome__icontains=q) | Q(setor__icontains=q)
            ).order_by('id')

    if not encargo:
        print('Nenhum colaborador encontrado')
        return HttpResponseServerError('Nenhum colaborador encontrado')

    return render(request, 'pesquisa_encargo.html', {'encargo': encargo})


def buscar_encargo_1(request): 
    q = request.GET.get('search')
    encargo = Employee.objects.all()

    if q:
        if q.isdigit():
            encargo = encargo.filter(id=q)
        else:
            encargo = encargo.filter(
                Q(colaborador__nome__icontains=q) | Q(setor__icontains=q)
            ).order_by('id')

    if not encargo:
        print('Nenhum colaborador encontrado')
        return HttpResponseServerError('Nenhum colaborador encontrado')
    return render(request, 'pesquisa_encargo1.html', {'encargo': encargo})


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
    administrador_logado = request.user.colaboradores
    empresa_do_admin = administrador_logado.empresa_id
    
    if request.method == 'POST':
        descricao = request.POST['descricao']
        valor = request.POST['valor']
        cargo_id = request.POST['cargos']
        cargo = Cargos.objects.get(pk=cargo_id)
      
        beneficio = Beneficios(
            descricao=descricao,
            valor=valor,
            cargo=cargo,
            empresa_id=empresa_do_admin,
        )
        beneficio.save()
        calcular_soma_beneficio_funcionario(request)
        
        return redirect('dashboard')
    
    return render(request, 'dashboard1.html')


def buscar_beneficio(request): 
    colaborador_logado = request.user.colaboradores
    empresa_id_colaborador = colaborador_logado.empresa.id
    
    q = request.GET.get('search')

    beneficio = Beneficios.objects.filter(Q(descricao__icontains=q) & Q(empresa_id=empresa_id_colaborador)).order_by('cargo__nome_cargo')

    return render(request, 'pesquisa_beneficio.html', {'beneficio': beneficio})


def beneficio_view(request):
    beneficio = Beneficios.objects.all()
    beneficio_list = [
        {
            'id': beneficio.id,
            'beneficio': f"{beneficio.id}, {beneficio.descricao}, {beneficio.valor}"
        }
        for beneficio in beneficio
    ]
    return JsonResponse({'beneficio': beneficio_list})


def deletar_beneficio(request, beneficio_id):
    if request.method == 'POST':
        try:
            beneficio = Beneficios.objects.get(pk=beneficio_id)
            beneficio.delete()
            calcular_soma_beneficio_funcionario(request)
            return redirect('dashboard')
        except Beneficios.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})
    else:
        try:
            beneficio = Beneficios.objects.get(pk=beneficio_id)
            return render(request, 'confirm_delete.html')
        except Beneficios.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})


#Funções do CRUD de Vincular Cargos

def inserir_vinculo(request):
    administrador_logado = request.user.colaboradores
    empresa_do_admin = administrador_logado.empresa_id
    
    if request.method == 'POST':
        horas_str = request.POST['horas']
        quantidade_str = request.POST['quantidade']
        try:
            horas = float(horas_str)
            quantidade = float(quantidade_str)
        except ValueError:
            horas = 0.0
            quantidade = 0.0
        orcamento_id = request.POST['numeroOrcamento']
        cargo_id = request.POST['cargos']
        cargo = Cargos.objects.get(id=cargo_id)
                
        auxiliar_calculo = AuxiliarCalculo.objects.first()
        horas_produtivas = round(auxiliar_calculo.total_meses_horasprodutivas, 6)
        print(horas_produtivas)
        tot_condominio = round(auxiliar_calculo.total_gastos_condominio / auxiliar_calculo.total_meses_condominio, 6)
        mes_condominio = round(tot_condominio / horas_produtivas, 6) 
        dia_condominio = round(mes_condominio / auxiliar_calculo.total_prestadores, 6)
        horas_condominio = float(dia_condominio)
        
        total_custo_mes = Employee.objects.filter(cargo=cargo).aggregate(Sum('custo_mes'))['custo_mes__sum']
        
        num_funcionarios = Employee.objects.filter(cargo=cargo).count()

        custo_medio_por_funcionario = round(total_custo_mes / num_funcionarios, 6)
        print(custo_medio_por_funcionario)
        
        if custo_medio_por_funcionario is None:
            custo_medio_por_funcionario = 0
            
        if horas_produtivas != 0:
            resultado_custo_mod = round(custo_medio_por_funcionario / horas_produtivas, 6)
            print(resultado_custo_mod)
        else:
            resultado_custo_mod = 0
        
        resultado_custo_mod = float(resultado_custo_mod)
        print(resultado_custo_mod)
                
        if custo_medio_por_funcionario is None:
            custo_medio_por_funcionario = 0
            
        total_mod = round(horas * quantidade * resultado_custo_mod, 6)
        total_condominio = round(horas * quantidade * horas_condominio, 6)
        total_custo = round(total_mod + total_condominio, 6)
        
        vinculo = DescricaoObra.objects.create(
            cargo=cargo,
            horas=horas,
            quantidade=quantidade,
            orcamento_id=orcamento_id,
            custo_mod=round(resultado_custo_mod,6),
            custo_hora_con=round(horas_condominio, 6),
            custo_total=round(horas_condominio+resultado_custo_mod, 2),
            horas_produtivas=horas_produtivas,
            total_mod=total_mod,
            total_condominio=total_condominio,
            total_custo=total_custo,
            auxiliarcalculo=auxiliar_calculo,
            empresa_id=empresa_do_admin,
        )
        vinculo.save()
        # calcular_soma_beneficio_funcionario(request)
        print(resultado_custo_mod)
          
        return redirect('dashboard')
    return render(request, 'dashboard1.html')


def buscar_vinculo(request): 
    colaborador_logado = request.user.colaboradores
    empresa_id_colaborador = colaborador_logado.empresa.id
    
    q = request.GET.get('search')   
    
    vinculo = DescricaoObra.objects.filter(Q(orcamento_id__icontains=q) & Q(empresa_id=empresa_id_colaborador)).order_by('orcamento_id', 'cargo__nome_cargo')
    return render(request, 'pesquisa_vinculo.html', {'vinculo': vinculo})


def vinculo_view(request):
    vinculo = DescricaoObra.objects.all()
    vinculo_list = [
        {
            'id': vinculo.id,
            'vinculo': f"{vinculo.id}, {vinculo.horas}, {vinculo.quantidade}, {vinculo.orcamento_id}, {vinculo.custo_mod}, {vinculo.custo_hora_con}, {vinculo.custo_total}"
        }
        for vinculo in vinculo
    ]
    return JsonResponse({'vinculo': vinculo_list})


def deletar_vinculo(request, vinculo_id):
    if request.method == 'POST':
        try:
            vinculo = DescricaoObra.objects.get(pk=vinculo_id)
            vinculo.delete()
            # calcular_soma_beneficio_funcionario(request)
            return redirect('dashboard')
        except DescricaoObra.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})
    else:
        try:
            vinculo = DescricaoObra.objects.get(pk=vinculo_id)
            return render(request, 'confirm_delete.html')
        except DescricaoObra.DoesNotExist:
            return JsonResponse({"success": False, "error": "Registro não encontrado"})


#Funções do CRUD do Orçamento   

def inserir_orcamento(request):
    administrador_logado = request.user.colaboradores
    empresa_do_admin = administrador_logado.empresa_id
    numero_novo_orcamento = request.GET.get('numeroNovoOrcamento', '')           
    
    descricao_obras = DescricaoObra.objects.filter(orcamento_id__iexact=numero_novo_orcamento)
    auxiliar_calculo = AuxiliarCalculo.objects.first()
    horas_obras = DescricaoObra.objects.filter(orcamento_id__iexact=numero_novo_orcamento).values_list('horas', flat=True)
    quantidade_linhas = len(horas_obras)        
    primeira_hora_produtiva = DescricaoObra.objects.filter(orcamento_id__iexact=numero_novo_orcamento).first()
    gestores = Employee.objects.filter(setor='Gestores')
   
    soma_horas = 0
    totalGes = 0

    custo_total = sum(descricao.total_mod for descricao in descricao_obras)
    total_prestadores = sum(descricao.quantidade for descricao in descricao_obras)
    capacidade_produtiva = auxiliar_calculo.total_prestadores
    custo_condominio = sum(descricao.total_condominio for descricao in descricao_obras)
    
    totalSoma = round(custo_total * 10 / 100, 2)
    
    if request.method == 'POST':
        outros = request.POST['orcamentoOutros']
        cliente = request.POST['orcamentoCliente']
        tributos = request.POST['orcamentoImpostos']
        lucros = request.POST['orcamentoLucro']
        valor_sugerido = request.POST.get('totalSugerido', 0)
        valor_outros = request.POST.get('valorOutros', 0)
        valor_tributos = request.POST.get('valorImpostos', 0)
        valor_lucro = request.POST.get('valorLucro', 0)
        
        if not valor_outros:
            valor_outros = 0
        else:
            valor_outros = valor_outros.replace(',', '.')

        if not valor_tributos:
            valor_tributos = 0
        else:
            valor_tributos = valor_tributos.replace(',', '.')

        if not valor_lucro:
            valor_lucro = 0
        else:
            valor_lucro = valor_lucro.replace(',', '.')
        
        rubrica = Rubrica.objects.create(orcamento_id=numero_novo_orcamento, capacidade_produtiva=capacidade_produtiva, cliente=cliente, quantidade=total_prestadores, custo_hora=custo_total, beneficios=totalSoma, 
                               condominio=custo_condominio, outros=outros, tributos=tributos, lucros=lucros, status='Aberto', valor_sugerido=valor_sugerido, valor_outros=valor_outros, valor_tributos=valor_tributos,
                               valor_lucro=valor_lucro, empresa_id=empresa_do_admin)

        descricoes = request.POST.getlist('descricao[]')
        valores = request.POST.getlist('valor[]')

        if len(descricoes) == len(valores):
            for i in range(len(descricoes)):
                descricao = descricoes[i]
                valor = valores[i]

                despesa = DespesasDinamicas(descricao=descricao, valor=valor, rubrica=rubrica, empresa_id=empresa_do_admin)
                despesa.save()

        return redirect('dashboard')

    return render(request, 'novo_orcamento.html', {'numero_novo_orcamento': numero_novo_orcamento,
                'custo_total': custo_total, 'custo_condominio': custo_condominio, 'totalSoma': totalSoma,
                'total_prestadores': total_prestadores, "capacidade_produtiva": capacidade_produtiva})   


def cancelar_orcamento(request, id):
    rubrica = Rubrica.objects.get(id=id)
    rubrica.status = "Cancelado"
    rubrica.save()

    return redirect('dashboard')


def finalizar_orcamento(request, id):
    rubrica = Rubrica.objects.get(id=id)
    rubrica.status = "Finalizado"
    rubrica.save()

    return redirect('dashboard')
 
    
def editar_orcamento(request, id):
    rubrica = get_object_or_404(Rubrica, id=id)
    status = rubrica.status 
    calcular_valores(request, id)
    
    if request.method == 'POST':
        cliente = request.POST['orcamentoCliente']
        outros = request.POST['orcamentoOutros'].replace(',', '.')
        tributos = request.POST['orcamentoImpostos'].replace(',', '.')
        lucros = request.POST['orcamentoLucro'].replace(',', '.')
        valor_sugerido = request.POST.get('totalSugerido', 0)
        # valor_outros = request.POST['valorOutros']
        # valor_tributos = request.POST['valorImpostos']
        # valor_lucro = request.POST['valorLucro']
        
        # # Trate as strings vazias como zero
        # if not valor_outros:
        #     valor_outros = 0

        # if not valor_tributos:
        #     valor_tributos = 0

        # if not valor_lucro:
        #     valor_lucro = 0
            
        # valor_outros = float(valor_outros)
        # valor_tributos = float(valor_tributos)
        # valor_lucro = float(valor_lucro)    
        
        rubrica.status = 'Cancelado'
        rubrica.save()
        
        calcular_valores(request, id)

        novo_rubrica = Rubrica.objects.create(
            orcamento_id=f'{rubrica.orcamento_id}-V2',
            capacidade_produtiva=rubrica.capacidade_produtiva,
            quantidade=rubrica.quantidade,
            custo_hora=rubrica.custo_hora,
            beneficios=rubrica.beneficios,
            condominio=rubrica.condominio,
            outros=outros.replace(',', '.'),
            tributos=tributos.replace(',', '.'),
            lucros=lucros.replace(',', '.'),
            status='Finalizado',
            cliente=cliente,
            valor_sugerido=valor_sugerido,
        )

        for despesa in rubrica.despesasdinamicas_set.all():
            descricao_key = f'descricao_{despesa.id}'
            valor_key = f'valor_{despesa.id}'
            descricao = request.POST.get(descricao_key)
            valor = request.POST.get(valor_key)

            nova_despesa = DespesasDinamicas(
                rubrica=novo_rubrica, 
                descricao=descricao.replace(',', '.'),
                valor=valor.replace(',', '.'),
            )
            nova_despesa.save()
            
        descricoes = request.POST.getlist('descricaoAd[]')
        valores = request.POST.getlist('valorAd[]')
        
        if len(descricoes) == len(valores):
            for i in range(len(descricoes)):
                descricao = descricoes[i]
                valor = valores[i]

                despesa = DespesasDinamicas(descricao=descricao, valor=valor, rubrica=novo_rubrica)
                despesa.save()

            return redirect('dashboard')
            
            context = {
                'rubrica': rubrica,
                'status': status,
            }
        return redirect('dashboard')
    
    calcular_valores(request,id)
    
    return render(request, 'seu_template.html', {'rubrica': rubrica, 'status': status})


def deletar_orcamento(request):
    return render(request, 'dashboard1.html')


def detalhes_orcamento(request, id):
    rubrica = Rubrica.objects.get(id=id)
    despesas_dinamicas = DespesasDinamicas.objects.filter(rubrica_id=rubrica)

    context = {
        'rubrica': rubrica,
        'despesas_dinamicas': despesas_dinamicas,
        'status': rubrica.status
    }

    return render(request, 'detalhes_orcamento.html', context)


def buscar_orcamento(request): 
    colaborador_logado = request.user.colaboradores
    empresa_id_colaborador = colaborador_logado.empresa.id
    
    q = request.GET.get('search')   
    
    orcamento = Rubrica.objects.filter(Q(orcamento_id__icontains=q) & Q(empresa_id=empresa_id_colaborador)).order_by('orcamento_id')    
    return render(request, 'pesquisa_orcamento.html', {'orcamento': orcamento})


def orcamento_view(request):
    orcamento = Rubrica.objects.annotate(
        descricao_despesa=F('despesasdinamicas__descricao'),
        valor_despesa=F('despesasdinamicas__valor')
    ).values(
        'id',
        'tributos',
        'lucros',
        'valor_sugerido',
        'custo_hora',
        'status',
        'descricao_despesa',
        'valor_despesa'
    )

    orcamento_list = list(orcamento)

    return JsonResponse({'orcamento': orcamento_list}, safe=False)


def calcular_valores(request, id):   
    rubricas = Rubrica.objects.all()
    
    for rubrica in rubricas:
        valor_sugerido = rubrica.valor_sugerido
        aliquota_outros = Decimal(rubrica.outros) 
        aliquota_tributos = Decimal(rubrica.tributos) 
        aliquota_lucros = Decimal(rubrica.lucros) 
        
        total_aliquota = aliquota_outros + aliquota_tributos + aliquota_lucros
        aliquota = (100 - total_aliquota) / 100  
        total = valor_sugerido * aliquota 
        print(aliquota) 
        print(total)
        totalDiminuido = valor_sugerido - total
        print(totalDiminuido)

        valor_lucro = (((aliquota_lucros * 100 ) / total_aliquota) / 100) * totalDiminuido  
        valor_tributos = (((aliquota_tributos * 100 ) / total_aliquota) / 100) * totalDiminuido  
        valor_outros = (((aliquota_outros * 100 ) / total_aliquota) / 100) * totalDiminuido  

        rubrica.valor_outros = valor_outros
        rubrica.valor_tributos = valor_tributos
        rubrica.valor_lucro = valor_lucro
        rubrica.save()
        print("Calculou valores")
        
    return redirect('detalhes_orcamento', id)
    

def inserir_capacidade_produtiva(request):
    auxiliar_calculo, created = AuxiliarCalculo.objects.get_or_create(pk=1)
    
    if created:
        auxiliar_calculo.total_salarios_gestores = 0
        auxiliar_calculo.total_salarios_prestadores = 0
        auxiliar_calculo.save()
    
    if request.method == 'POST':
        total_prestadores = request.POST['capacidadeProdutiva']
        auxiliar_calculo.total_prestadores = total_prestadores
        auxiliar_calculo.save()

        return redirect('dashboard')
    
    return render(request, 'dashboard1.html', context={})


def get_valor_sugerido(request, rubrica_id):
    try:
        rubrica = Rubrica.objects.get(pk=rubrica_id)
        valor_sugerido = rubrica.valor_sugerido
        return JsonResponse({'valor_sugerido': float(valor_sugerido)})
    except Rubrica.DoesNotExist:
        return JsonResponse({'error': 'Rubrica não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def inserir_data(request):
    return render(request, 'dashboard1.html', context={})    


def inserir_jornada(request):
    return render(request, 'dashboard1.html', context={})


def inserir_horas(request):
    return render(request, 'dashboard1.html', context={})       


# funçaõ para listar os colaboradores 

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

    employees = Employee.objects.all()
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
    employees = Employee.objects.all()

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


def list_employee(request):
    employees = Colaboradores.objects.all()
    return render(request, 'list_employee.html', {'employees': employees})


# Função para calcular gastos com condominio

def calcular_gastos_ano_corrente(request):
    data_atual = datetime.now()
    ano_corrente = data_atual.year
    
    auxiliar_calculo, created = AuxiliarCalculo.objects.get_or_create(pk=1)
    if created:
        auxiliar_calculo.total_meses_condominio = 0
        auxiliar_calculo.total_gastos_condominio = 0
        auxiliar_calculo.save()
        
    gastos_ano_corrente = GastosFixos.objects.filter(ano=ano_corrente).aggregate(Sum('valor'))['valor__sum']   
    quantidade_entradas_ano_corrente = GastosFixos.objects.filter(ano=ano_corrente).count()
    
    if gastos_ano_corrente is None or quantidade_entradas_ano_corrente is None:
        gastos_ano_corrente = 0
        quantidade_entradas_ano_corrente = 0         
            
    auxiliar_calculo.total_meses_condominio = quantidade_entradas_ano_corrente
    auxiliar_calculo.total_gastos_condominio = gastos_ano_corrente
    auxiliar_calculo.save()
        
    print(f'Soma Total de Gastos: {gastos_ano_corrente}')
    print(f'Quantidade de Meses com Gastos: {quantidade_entradas_ano_corrente}')
    
    response_data = {
        'total_gastos_ano_corrente': gastos_ano_corrente or 0,
        'quantidade_entradas_ano_corrente': quantidade_entradas_ano_corrente
    }

    return JsonResponse(response_data)


# Função para listar as horas condomínios

def lista_horas_condiminio_view(request):
    auxiliar_calculo = AuxiliarCalculo.objects.first()
    
    if auxiliar_calculo.total_meses_condominio > 0:
        custo_condominio = auxiliar_calculo.total_gastos_condominio / auxiliar_calculo.total_meses_condominio
    else:
        custo_condominio = 0
        
    if custo_condominio != custo_condominio:
        custo_condominio = 0
    
    if auxiliar_calculo.total_meses_horasprodutivas != 0:
        custo_hora_condominio = custo_condominio / auxiliar_calculo.total_meses_horasprodutivas
    else:
        custo_hora_condominio = None
        
    if auxiliar_calculo.total_prestadores != 0:
        custo_hora_percapta = custo_hora_condominio / auxiliar_calculo.total_prestadores
    else:
        custo_hora_percapta = None       

        
    return render(request, 'lista_condominio.html', {'auxiliar_calculo': auxiliar_calculo, 'custo_hora_condominio': custo_hora_condominio, 'custo_hora_percapta': custo_hora_percapta, 'custo_condominio': custo_condominio})


# Função para calcular a média de horas produtivas

def calcular_media_horas_produtivas(request):
    search_query = request.GET.get('search_query')
    
    if search_query and search_query.strip():
        try:
            ano_consulta = int(search_query)
        except ValueError:
            ano_consulta = None
    else:
        ano_consulta = None

    if ano_consulta is not None:
        resultado = CalendarioMensal.objects.filter(ano=ano_consulta).aggregate(
            Sum('horas_produtivas'), Count('horas_produtivas')
        )
        soma_total = resultado['horas_produtivas__sum']
        quantidade = resultado['horas_produtivas__count']
        media = round(soma_total / quantidade, 6) if quantidade > 0 else 0.0
    else:
        soma_total = 0
        quantidade = 0
        media = 0.0
 
    print(f'Soma Total: {soma_total}')
    print(f'Quantidade: {quantidade}')
    print(f'Média: {media}')
    
    response_data = {
        'soma_total': soma_total if soma_total else 0.0,
        'quantidade': quantidade,
        'media': media,
    }
    
    ano_corrente = datetime.now().year
    if ano_consulta == ano_corrente:
        with transaction.atomic():
            auxiliar_calculo = AuxiliarCalculo.objects.first()
            auxiliar_calculo.total_meses_horasprodutivas = media
            auxiliar_calculo.total_meses_calendario = quantidade
            auxiliar_calculo.save()

    return JsonResponse(response_data)
    

def calcular_soma_beneficio_funcionario(request):
    cargos = Cargos.objects.all()
    
    resultados = []

    for cargo in cargos:
        soma_beneficios = Beneficios.objects.filter(cargo=cargo).aggregate(Sum('valor'))['valor__sum'] or 0

        resultado = {
            'cargo': cargo,
            'soma_beneficios': soma_beneficios
        }

        resultados.append(resultado)
        
        print(f"Soma dos benefícios para o cargo {cargo.nome_cargo}: R$ {soma_beneficios}")
        
        Employee.objects.filter(cargo_id=cargo).update(beneficios=soma_beneficios)

    return render(request, 'dashboard1.html', {'resultados': resultados})


# funçaõ para listar os colaboradores por setor

def colaboradores_view_filter(request):
    colaboradores = Colaboradores.objects.filter(setor="Prestador de Serviço")
    colaboradores_datas = [{"id": colaborador.id, "nome": colaborador.nome} for colaborador in colaboradores]
    return JsonResponse({"colaboradores": colaboradores_datas})


#Verifica se o CPF não existe

def verificar_cpf(request):
    cpf = request.GET.get('cpf')
    if Colaboradores.objects.filter(cpf=cpf).exists():
        return JsonResponse({'cpf_existe': True})
    else:
        return JsonResponse({'cpf_existe': False})


def verificar_matricula(request):
    matricula = request.GET.get('matricula')
    if Colaboradores.objects.filter(matricula=matricula).exists():
        return JsonResponse({'matricula_existe': True})
    else:
        return JsonResponse({'matricula_existe': False})


# Verifica se o CNPJ não existe
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
    
    
def verificar_numero(request):
    numero_empresa = request.GET.get('numero_empresa')
    print(numero_empresa)
    if Empresa.objects.filter(numero_empresa= numero_empresa ).exists():
        print(numero_empresa)
        return JsonResponse({'numero_existe' : True})
    else:
        print(numero_empresa)
        return JsonResponse({'numero_existe' : False})


def export_pdf_condominio(request):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    doc = SimpleDocTemplate(temp_file, pagesize=landscape(A3))

    data = []
    auxiliares = AuxiliarCalculo.objects.all()

    data.append([
        'Total Salários Gestores', 'Total Salários Prestadores', 'Total Prestadores',
        'Total Meses Condomínio', 'Total Gastos Condomínio', 'Total Meses Calendário',
        'Total Meses Horas Produtivas', 'Custo Hora Condominio'
    ])

    for auxiliar in auxiliares:
        data.append([
            f"R$ {auxiliar.total_salarios_gestores:.2f}",
            f"R$ {auxiliar.total_salarios_prestadores:.2f}",
            auxiliar.total_prestadores,
            auxiliar.total_meses_condominio,
            f"R$ {auxiliar.total_gastos_condominio:.2f}",
            auxiliar.total_meses_calendario,
            f"R$ {auxiliar.total_meses_horasprodutivas:.2f}",
            f"R${auxiliar.total_gastos_condominio / auxiliar.total_meses_horasprodutivas:.2f}"
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
    temp_file.close()

    temp_file = open(temp_file.name, 'rb')
    response = HttpResponse(temp_file.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="auxiliar_calculo.pdf"'
    temp_file.close()

    return response


def export_pdf_condominio_temporary():
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    doc = SimpleDocTemplate(temp_file, pagesize=landscape(A3))

    data = []
    auxiliares = AuxiliarCalculo.objects.all()
    
    data.append([
        'Total Salários Gestores', 'Total Salários Prestadores', 'Total Prestadores',
        'Total Meses Condomínio', 'Total Gastos Condomínio', 'Total Meses Calendário',
        'Total Meses Horas Produtivas', 'Custo Hora Condominio'
    ])

    for auxiliar in auxiliares:
        data.append([
            f"R$ {auxiliar.total_salarios_gestores:.2f}",
            f"R$ {auxiliar.total_salarios_prestadores:.2f}",
            auxiliar.total_prestadores,
            auxiliar.total_meses_condominio,
            f"R$ {auxiliar.total_gastos_condominio:.2f}",
            auxiliar.total_meses_calendario,
            f"R$ {auxiliar.total_meses_horasprodutivas:.2f}",
            f"R${auxiliar.total_gastos_condominio / auxiliar.total_meses_horasprodutivas:.2f}"
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
    
    return temp_file


def export_csv_condominio(request):
    response = HttpResponse(content_type='text/csv')
    timestamp = timezone.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"auxiliar_calculo_{timestamp}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response, delimiter=';')
    
    writer.writerow([
        'Total Salários Gestores', 'Total Salários Prestadores', 'Total Prestadores',
        'Total Meses Condomínio', 'Total Gastos Condomínio', 'Total Meses Calendário',
        'Total Meses Horas Produtivas','Custo Hora Condominio'
    ])

    auxiliares = AuxiliarCalculo.objects.all()

    for auxiliar in auxiliares:
        gastos_por_hora = auxiliar.total_gastos_condominio / auxiliar.total_meses_horasprodutivas
        gastos_por_hora_formatado = "{:.2f}".format(gastos_por_hora)
        writer.writerow([
            auxiliar.total_salarios_gestores,
            auxiliar.total_salarios_prestadores,
            auxiliar.total_prestadores,
            auxiliar.total_meses_condominio,
            auxiliar.total_gastos_condominio,
            auxiliar.total_meses_calendario,
            auxiliar.total_meses_horasprodutivas,
            gastos_por_hora_formatado
        ])

    return response


def enviar_email_personalizado(request, auxiliar_calculo_id):
    auxiliar_calculo = AuxiliarCalculo.objects.get(pk=auxiliar_calculo_id)

    if request.method == 'POST':
        destinatario_email = request.POST['destinatario_email']

        if auxiliar_calculo.total_meses_horasprodutivas != 0:
            hora_condominio = auxiliar_calculo.total_gastos_condominio / auxiliar_calculo.total_meses_horasprodutivas
        else:
            hora_condominio = 'Divisão por zero'

        context = {
            'auxiliar_calculo': auxiliar_calculo,
            'hora_condominio': hora_condominio,
        }
        email_body = render_to_string('template_email.html', context)

        pdf_file = export_pdf_condominio_temporary()
        pdf_file.seek(0)


        email = EmailMessage('Assunto do Email', email_body, to=[destinatario_email])
        email.attach('auxiliar_calculo.pdf', pdf_file.read(), 'application/pdf')
        email.content_subtype = 'html'
        email.send()

        pdf_file.close()

        return render(request, 'email_condominio.html')

    return render(request, 'dashboard1.html', {'auxiliar_calculo': auxiliar_calculo})


def imprimir_tabela(request):
    response = HttpResponse(content_type='text/html; charset=utf-8')
    buffer = io.StringIO()

    buffer.write('<table border="1">')
    buffer.write('<thead>')
    buffer.write('<tr>')
    buffer.write('<th>Colaborador</th>')
    buffer.write('<th>Salário</th>')
    buffer.write('<th>Setor</th>')
    buffer.write('<th>Cargo</th>')
    buffer.write('<th>Periculosidade</th>')
    buffer.write('<th>FGTS</th>')
    buffer.write('<th>1/3 Férias</th>')
    buffer.write('<th>FGTS Férias</th>')
    buffer.write('<th>13º Salário</th>')
    buffer.write('<th>FGTS 13º</th>')
    buffer.write('<th>Multa Rescisória</th>')
    buffer.write('<th>Custo Salário</th>')
    buffer.write('<th>Rateio</th>')
    buffer.write('<th>Custo Mês</th>')
    buffer.write('</tr>')
    buffer.write('</thead>')
    buffer.write('<tbody>')

    employees = Employee.objects.all()

    for employee in employees:
        buffer.write('<tr>')
        buffer.write(f'<td>{employee.colaborador.nome}</td>')
        buffer.write(f'<td>R$ {employee.cargo.salario:.2f}</td>')
        buffer.write(f'<td>{employee.setor}</td>')
        buffer.write(f'<td>{employee.cargo.nome_cargo}</td>')
        buffer.write(f'<td>R$ {employee.periculosidade:.2f}</td>')
        buffer.write(f'<td>R$ {employee.fgts:.2f}</td>')
        buffer.write(f'<td>R$ {employee.um_terco_ferias:.2f}</td>')
        buffer.write(f'<td>R$ {employee.fgts_ferias:.2f}</td>')
        buffer.write(f'<td>R$ {employee.decimo_terceiro:.2f}</td>')
        buffer.write(f'<td>R$ {employee.fgts_decimo_terceiro:.2f}</td>')
        buffer.write(f'<td>R$ {employee.multa_rescisoria:.2f}</td>')
        buffer.write(f'<td>R$ {employee.custo_salario:.2f}</td>')
        buffer.write(f'<td>R$ {employee.rateio:.2f}</td>')
        buffer.write(f'<td>R$ {employee.custo_mes:.2f}</td>')
        buffer.write('</tr>')

    buffer.write('</tbody>')
    buffer.write('</table>')
    buffer.write('<button class="botao-imprimir btn btn-success" onclick="imprimir()">Imprimir Tabela</button>')

    buffer.write('<style>')
    buffer.write('@media print {')
    buffer.write('  .botao-imprimir {')
    buffer.write('    display: none;')
    buffer.write('  }')
    buffer.write('  @page {')
    buffer.write('    header: "Impressão Cargos";')
    buffer.write('  }')
    buffer.write('</style>')

    buffer.write('<script>')
    buffer.write('function imprimir() {')
    buffer.write('  window.print();')
    buffer.write('}')
    buffer.write('</script>')

    buffer.seek(0)
    response.content = buffer.read()

    return response


#  Começo DRE relatório

def dre_report(request):
    q = request.GET.get('search')   
    orcamento = Rubrica.objects.filter(orcamento_id__icontains=q, status='Finalizado').order_by('orcamento_id')
    
    # orcamento = orcamento.values(
    #     'id',
    #     'orcamento_id',
    #     'valor_tributos',
    #     'valor_lucro',
    #     'valor_sugerido',
    #     'custo_hora',
    #     'status'
    # )
        
    tot_tributos = orcamento.aggregate(Sum('valor_tributos'))['valor_tributos__sum'] or 0
    tot_lucros = orcamento.aggregate(Sum('valor_lucro'))['valor_lucro__sum'] or 0
    
    return render(request, 'dre_template.html', {'orcamento': orcamento, 'tot_tributos': tot_tributos, 'tot_lucros': tot_lucros})


def export_orcamento(request, rubrica_id):
    rubrica = Rubrica.objects.get(id=rubrica_id)
    despesas_dinamicas = rubrica.despesasdinamicas_set.all()

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="rubrica_{rubrica_id}.xlsx'

    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    cell_format = workbook.add_format()
    cell_format.set_border(1) 
    cell_format.set_align('center')
    cell_format.set_align('vcenter')
    
    header_format = workbook.add_format()
    header_format.set_border(1)
    header_format.set_align('center')
    header_format.set_align('vcenter')
    header_format.set_bg_color('#333333')
    header_format.set_font_color('white')
    header_format.set_bold()
    
    data = [
        ['Descrição', 'Valor'],
        ['Orçamento Id', rubrica.orcamento_id],
        ['Cliente', rubrica.cliente],
        ['Capacidade Produtiva', rubrica.capacidade_produtiva],
        ['Qtd Funcionários', rubrica.quantidade],
        ['Total Custo HR/Func.', rubrica.custo_hora],
        ['Total Benefícios', rubrica.beneficios],
        ['Total Condomínio', rubrica.condominio],
        ['Descrição', 'Aliquotas'],
        ['Outros', str(rubrica.outros) + '%'],
        ['Impostos', str(rubrica.tributos) + '%'],
        ['Lucro', str(rubrica.lucros) + '%'],
        ['Descrição', 'Valor'],
        ['Outros R$', rubrica.valor_outros],
        ['Impostos R$', rubrica.valor_tributos],
        ['Lucro R$', rubrica. valor_lucro],
    ]
  
    worksheet.set_column('A:A', 50)
    worksheet.set_column('B:B', 30)

    for row, (col1, col2) in enumerate(data):
        if col1 == 'Descrição': 
            worksheet.write(row, 0, col1, header_format)
            worksheet.write(row, 1, col2, header_format)
        else:
            worksheet.write(row, 0, col1, cell_format)
            worksheet.write(row, 1, col2, cell_format)

    row += 1

    header = ['Despesas Adicionadas', 'Valor']
    for col, col_name in enumerate(header):
        worksheet.write(row, col, col_name, header_format)

    row += 1

    for despesa in despesas_dinamicas:
        worksheet.write(row, 0, despesa.descricao, cell_format)
        worksheet.write(row, 1, despesa.valor, cell_format)
        row += 1
        
    extended_header_format = workbook.add_format()
    extended_header_format.set_border(1)
    extended_header_format.set_align('center')
    extended_header_format.set_align('vcenter')
    extended_header_format.set_bg_color('#333333')  
    extended_header_format.set_font_color('white') 
    extended_header_format.set_bold()
        
    data.extend([
        ['Valor Sugerido', rubrica.valor_sugerido],
    ])
    
    for col1, col2 in data[-1:]:
        worksheet.write(row, 0, col1, extended_header_format)
        worksheet.write(row, 1, col2, extended_header_format)
        row += 1

    workbook.close()

    return response


def export_orcamento_pdf(request, rubrica_id):
    rubrica = Rubrica.objects.get(id=rubrica_id)
    despesas_dinamicas = rubrica.despesasdinamicas_set.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="rubrica_{rubrica_id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    data1 = [
        ['Descrição', 'Valor'],
        ['Orçamento Id', rubrica.orcamento_id],
        ['Cliente', rubrica.cliente],
        ['Capacidade Produtiva', rubrica.capacidade_produtiva],
        ['Qtd Funcionários', rubrica.quantidade],
        ['Total Custo HR/Func.', rubrica.custo_hora],
        ['Total Benefícios', rubrica.beneficios],
        ['Total Condomínio', rubrica.condominio],
    ]

    data2 = [
        ['Descrição', 'Aliquotas'],
        ['Outros', str(rubrica.outros) + '%'],
        ['Impostos', str(rubrica.tributos) + '%'],
        ['Lucro', str(rubrica.lucros) + '%'],
    ]

    data3 = [
        ['Descrição', 'Valor'],
        ['Outros R$', rubrica.valor_outros],
        ['Impostos R$', rubrica.valor_tributos],
        ['Lucro R$', rubrica.valor_lucro],
    ]

    table_data1 = []
    for col1, col2 in data1:
        table_data1.append([col1, col2])

    t1 = Table(table_data1, colWidths=[230, 130])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(t1)

    elements.append(Spacer(1, 12))

    table_data2 = []
    for col1, col2 in data2:
        table_data2.append([col1, col2])

    t2 = Table(table_data2, colWidths=[230, 130])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(t2)

    elements.append(Spacer(1, 12))

    table_data3 = []
    for col1, col2 in data3:
        table_data3.append([col1, col2])

    t3 = Table(table_data3, colWidths=[230, 130])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(t3)

    elements.append(Spacer(1, 12))

    header = ['Despesas Adicionadas', 'Valor']
    table_data = [header]
    for despesa in despesas_dinamicas:
        table_data.append([despesa.descricao, despesa.valor])

    t = Table(table_data, colWidths=[230, 130])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(t)

    elements.append(Spacer(1, 12))
    
    extended_header = ['Valor Sugerido', rubrica.valor_sugerido]
    table_data = [extended_header]
    t = Table(table_data, colWidths=[230, 130])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(t)

    doc.build(elements)

    return response

#Adição do método de enviar a rubrica por e-mail

def enviar_email_rubrica(request, rubrica_id, destinatario_email):
    
    pdf_response = export_orcamento_pdf(request, rubrica_id)

    rubrica = Rubrica.objects.get(id=rubrica_id)
    context = {
        'rubrica': rubrica,
    }
    email_body = render_to_string('template_email_rubrica.html', context)

  
    email = EmailMessage('Assunto do Email', email_body, to=[destinatario_email])
    email.attach('rubrica.pdf', pdf_response.getvalue(), 'application/pdf')
    email.content_subtype = 'html'
    email.send()

    pdf_response.close()

def exportar_beneficios_xlsx(request): 
    beneficios = Beneficios.objects.all()

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=beneficios.xlsx'

    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    cell_format = workbook.add_format()
    cell_format.set_border(1)
    cell_format.set_align('center')
    cell_format.set_align('vcenter')

    header_format = workbook.add_format()
    header_format.set_border(1)
    header_format.set_align('center')
    header_format.set_align('vcenter')
    header_format.set_bg_color('#333333')
    header_format.set_font_color('white')
    header_format.set_bold()

    data = [
        ['Cargo', 'Descrição', 'Valor'],
    ]

    for beneficio in beneficios:
        data.append([beneficio.cargo.nome_cargo, beneficio.descricao, beneficio.valor])

    worksheet.set_column('A:A', 30)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 20)

    for row, row_data in enumerate(data):
        for col, col_data in enumerate(row_data):
            if row == 0:
                worksheet.write(row, col, col_data, header_format)
            else:
                worksheet.write(row, col, col_data, cell_format)

    workbook.close()

    return response

def exportar_beneficios_pdf(request):
    beneficios = Beneficios.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=beneficios.pdf'

    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    elements = []

    data = [
        ['Cargo', 'Descrição', 'Valor'],
    ]

    for beneficio in beneficios:
        data.append([beneficio.cargo.nome_cargo, beneficio.descricao, beneficio.valor])

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

    elements.append(table)

    doc.build(elements)
    return response