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

from django.core.mail import send_mail
from django.conf import settings
import random
from .models import GastosFixos, Colaboradores, Cargos, Endereco, Empresa, CalendarioMensal, Employee, Beneficios, DescricaoObra, Rubrica
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
        try:
            colaborador = Colaboradores.objects.get(usuario=request.user)
            nome = colaborador.nome
        except Colaboradores.DoesNotExist:
        # Se não houver um nome na tabela "Colaboradores", pegue o username da tabela "auth_user"
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

        # Verifique se já existe um registro com o mesmo CPF
        if not Colaboradores.objects.filter(cpf=cpf.replace('.', '').replace('-', '')):
            #cargo = Cargos.objects.get(id=cargo_id)
        
            mao_de_obra = Colaboradores(
                matricula=matricula,
                nome=nome,
                cpf=cpf.replace('.', '').replace('-', ''),
               # cargo=cargo,  # Associando o cargo à mão de obra
            )
            mao_de_obra.save()
            return redirect('dashboard')
        else:
            # Retorne uma mensagem de erro informando que o CPF já existe
            error_message = "Já existe um registro com o mesmo CPF."
            return render(request, 'dashboard1.html', {'error_message': error_message})
    
    return render(request, 'dashboard1.html')

def buscar_colaborador(request): 
    q = request.GET.get('search')   
    colaboradores = Colaboradores.objects.filter(nome__icontains=q).order_by('id')
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
       # cpf = request.POST['cpf']

        # Atualize os campos do colaborador existente
        colaborador.nome = nome
        colaborador.matricula = matricula
        #colaborador.cpf = cpf
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
        dias_uteis_str = request.POST.get("dias_uteis")  # Pegar a string dos dias úteis
        # Substituir ',' por '.' para garantir a formatação correta
        dias_uteis_str = dias_uteis_str.replace(",", ".")
        feriado = float(request.POST.get("feriados"))
        
        # Converter a string formatada para um número de ponto flutuante
        dias_uteis = float(dias_uteis_str)
        print(dias_uteis)

        funcionario = Colaboradores.objects.get(pk=funcionario_id)

        calendario = CalendarioMensal(
            mes=mes,
            ano=ano,
            jornada_diaria=jornada_diaria,
            funcionario=funcionario,
            horas_produtivas=horas_produtivas,
            dias_uteis=round(dias_uteis - feriado, 2), # Definir o valor dos dias úteis
            feriado=feriado
        )
        print(dias_uteis)
        calendario.save()
        calcular_media_horas_produtivas(request)

        return redirect("dashboard")  # Redirecionar para uma página de sucesso

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
    q = request.GET.get('searchCal')   
    calendario = CalendarioMensal.objects.filter(ano__icontains=q).order_by('ano', 'mes')
    return render(request, 'pesquisa_calendario.html', {'calendario': calendario})

# def editar_calendario(request, id):
#     calendario = CalendarioMensal.objects.get(id=id)
#     if request.method == "POST":
#         mes = int(request.POST['mes'])
#         ano = int(request.POST.get("ano"))
#         jornada_diaria = float(request.POST.get("jornada_diaria"))
#         funcionario_id = int(request.POST.get("funcionario"))
#         horas_produtivas = float(request.POST.get("horas_produtivas"))
#         dias_uteis = int(request.POST.get("dias_uteis"))  # Pegar o valor dos dias úteis

#         funcionario = Colaboradores.objects.get(pk=funcionario_id)

#         calendario.mes = mes
#         calendario.ano = ano
#         calendario.jornada_diaria = jornada_diaria
#         calendario.funcionario = funcionario
#         calendario.horas_produtivas = horas_produtivas
#         calendario.dias_uteis = dias_uteis         
#         calendario.save()
#         calcular_media_horas_produtivas(request)

#         return redirect("dashboard")  # Redirecionar para uma página de sucesso

#     return render(request, 'dashboard1.html', {'calendario': calendario})

# def deletar_calendario(request, calendario_id):
#     if request.method == 'POST':
#         try:
#             calendario = CalendarioMensal.objects.get(pk=calendario_id)
#             calendario.delete()
#             calcular_media_horas_produtivas(request)
#             return redirect('dashboard')
#         except CalendarioMensal.DoesNotExist:
#             return JsonResponse({"success": False, "error": "Registro não encontrado"})
#     else:
#         try:
#             calendario = CalendarioMensal.objects.get(pk=calendario_id)
#             return render(request, 'confirm_delete.html')
#         except CalendarioMensal.DoesNotExist:
#             return JsonResponse({"success": False, "error": "Registro não encontrado"})
        

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
        beneficios = 0

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
            beneficios=beneficios,
            rateio=rateio,
            custo_mes=custo_mes,
        )
        
        colaborador.setor = setor
        colaborador.save() 
        calcular_soma_beneficio_funcionario(request)
        atualizar_dados_banco()
        # Redirecionar para a página desejada após a inserção
        return redirect('dashboard')
    
    return render(request, 'dashboard1.html')

from django.http import HttpResponseServerError

def buscar_encargo(request):
    q = request.GET.get('search')
    print(f'Valor de q: {q}')  # Adicione esta linha para depurar o valor de q

    encargo = Employee.objects.all()  # Começa com todos os registros

    if q:
        if q.isdigit():
            # Tente buscar o colaborador pelo ID
            encargo = encargo.filter(id=q)
        else:
            # Tente buscar o colaborador pelo nome do colaborador ou setor
            encargo = encargo.filter(
                Q(colaborador__nome__icontains=q) | Q(setor__icontains=q)
            ).order_by('id')

    if not encargo:
        # Se nenhum resultado for encontrado, lance um erro 500 (Internal Server Error)
        print('Nenhum colaborador encontrado')  # Mensagem de depuração
        return HttpResponseServerError('Nenhum colaborador encontrado')

    return render(request, 'pesquisa_encargo.html', {'encargo': encargo})


def buscar_encargo_1(request): 
    q = request.GET.get('search')
    print(f'Valor de q: {q}')  # Adicione esta linha para depurar o valor de q

    encargo = Employee.objects.all()  # Começa com todos os registros

    if q:
        if q.isdigit():
            # Tente buscar o colaborador pelo ID
            encargo = encargo.filter(id=q)
        else:
            # Tente buscar o colaborador pelo nome do colaborador ou setor
            encargo = encargo.filter(
                Q(colaborador__nome__icontains=q) | Q(setor__icontains=q)
            ).order_by('id')

    if not encargo:
        # Se nenhum resultado for encontrado, lance um erro 500 (Internal Server Error)
        print('Nenhum colaborador encontrado')  # Mensagem de depuração
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
    if request.method == 'POST':
        descricao = request.POST['descricao']
        valor = request.POST['valor']
        cargo_id = request.POST['cargos']
        cargo = Cargos.objects.get(pk=cargo_id)

        
        beneficio = Beneficios(
            descricao=descricao,
            valor=valor,
            cargo=cargo,
        )
        beneficio.save()
        calcular_soma_beneficio_funcionario(request)
        
        return redirect('dashboard')
    return render(request, 'dashboard1.html')

def buscar_beneficio(request): 
    q = request.GET.get('search')   
    beneficio = Beneficios.objects.filter(descricao__icontains=q).order_by('cargo__nome_cargo')
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
        horas_produtivas = auxiliar_calculo.total_meses_horasprodutivas
        horas_condominio = round(auxiliar_calculo.total_gastos_condominio / auxiliar_calculo.total_meses_horasprodutivas / auxiliar_calculo.total_prestadores, 6)
        horas_condominio = (float(horas_condominio))
        
        # Calcular a soma do custo_mes para todos os funcionários com o mesmo cargo
        total_custo_mes = Employee.objects.filter(cargo=cargo).aggregate(Sum('custo_mes'))['custo_mes__sum']
        
        # Contar o número de funcionários com o mesmo cargo
        num_funcionarios = Employee.objects.filter(cargo=cargo).count()

        # Calcular o custo médio por funcionário
        custo_medio_por_funcionario = round(total_custo_mes / num_funcionarios, 6)
        
        if custo_medio_por_funcionario is None:
            custo_medio_por_funcionario = 0
            
        if horas_produtivas != 0:
            resultado_custo_mod = round(custo_medio_por_funcionario / horas_produtivas, 6)
        else:
            resultado_custo_mod = 0
        
        resultado_custo_mod = float(resultado_custo_mod)
                
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
            custo_mod=resultado_custo_mod,
            custo_hora_con=horas_condominio,
            custo_total=round(horas_condominio+resultado_custo_mod, 2),
            horas_produtivas=horas_produtivas,
            total_mod=total_mod,
            total_condominio=total_condominio,
            total_custo=total_custo,
            auxiliarcalculo=auxiliar_calculo
        )
        vinculo.save()
        # calcular_soma_beneficio_funcionario(request)
        
        return redirect('dashboard')
    return render(request, 'dashboard1.html')

def buscar_vinculo(request): 
    q = request.GET.get('search')   
    vinculo = DescricaoObra.objects.filter(orcamento_id__icontains=q).order_by('orcamento_id', 'cargo__nome_cargo')
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
    numero_novo_orcamento = request.GET.get('numeroNovoOrcamento', '')           
    
    descricao_obras = DescricaoObra.objects.filter(orcamento_id__iexact=numero_novo_orcamento)
    auxiliar_calculo = AuxiliarCalculo.objects.first()
    horas_obras = DescricaoObra.objects.filter(orcamento_id__iexact=numero_novo_orcamento).values_list('horas', flat=True)
    quantidade_linhas = len(horas_obras)        
    primeira_hora_produtiva = DescricaoObra.objects.filter(orcamento_id__iexact=numero_novo_orcamento).first()
    gestores = Employee.objects.filter(setor='Gestores')
    
    soma_horas = 0
    totalGes = 0

    # # Percorra as horas e calcule a soma
    # for horas in horas_obras:
    #     soma_horas += horas

    # total_beneficios_gestores = 0

    # for gestor in gestores:
    #     total_beneficios_gestores += gestor.beneficios
        
    # print(f'Total dos benefícios dos gestores: {total_beneficios_gestores}')
    
    # if primeira_hora_produtiva:
    #     valor_primeira_hora = primeira_hora_produtiva.horas_produtivas
    # else:
    #     valor_primeira_hora = None
    # print(f'Valor da primeira hora produtiva: {valor_primeira_hora}')
    
    # media_para_gestores = soma_horas / quantidade_linhas
    # print(f'Média para gestores: {media_para_gestores}')
    # totalGes += round(total_beneficios_gestores * 1 / valor_primeira_hora * media_para_gestores, 2)
    # print(f'Total dos benefícios dos gestores: {totalGes}')
    
    # total = 0
    
    # for descricao_obra in descricao_obras:
    #     # Consulte a tabela Beneficios para encontrar registros correspondentes
    #     beneficios = Beneficios.objects.filter(cargo_id=descricao_obra.cargo_id)

    #     # Para cada registro correspondente na tabela Beneficios, calcule o valor e adicione ao total
    #     for beneficio in beneficios:
    #         total += round(beneficio.valor * descricao_obra.quantidade / descricao_obra.horas_produtivas * descricao_obra.horas, 2)
            
    # totalSoma = round(total + totalGes, 2)
    # print(totalSoma)
    

    # Calcule a soma dos valores
    custo_total = sum(descricao.total_mod for descricao in descricao_obras)
    total_prestadores = sum(descricao.quantidade for descricao in descricao_obras)
    capacidade_produtiva = auxiliar_calculo.total_prestadores
    custo_condominio = sum(descricao.total_condominio for descricao in descricao_obras)
    
    totalSoma = round(custo_total * 10 / 100, 2)
    
    if request.method == 'POST':
        compra_materiais = request.POST['orcamentoCompraMateriais']
        materiais_dvs = request.POST['orcamentoMateriaisDvs']
        dvs_socio = request.POST['orcamentoDvsSocios']
        telefonia_comunicacao = request.POST['orcamentoTelefonia']
        seguro_maquinas_equipamentos = request.POST['orcamentoSeguroEquipamentos']
        manutencao = request.POST['orcamentoManutencao']
        dvs_operacao = request.POST['orcamentoDvsOperacao']
        bonus_resultado = request.POST['orcamentoBonus']
        plr = request.POST['orcamentoPlr']
        horas_extras = request.POST['orcamentoHorasExtras']
        exames_adiciona_demissional = request.POST['orcamentoExame']
        terceirizados = request.POST['orcamentoTerceirizados']
        alimentacao = request.POST['orcamentoAlimentacao']
        hospedagem = request.POST['orcamentoHospedagem']
        quilometragem = request.POST['orcamentoQuilometragem']
        deslocamento = request.POST['orcamentoDeslocamento']
        combustivel =  request.POST['orcamentoCombustivel']
        estacionamento_pedagio = request.POST['orcamentoEstacionamento']
        comissoes = request.POST['orcamentoComissoes']
        seguros_obra_dvs = request.POST['orcamentoSeguroObra']
        insumos = request.POST['orcamentoInsumos']
        manutencao_conservacao = request.POST['orcamentoManutencaoECons']
        distrato_multas = request.POST['orcamentoDistrato']
        # condominio = request.POST['orcamentoCondominio']
        tributos = request.POST['orcamentoImpostos']
        lucros = request.POST['orcamentoLucro']
        valor_sugerido = request.POST.get('totalSugerido', 0)
        
        Rubrica.objects.create(orcamento_id=numero_novo_orcamento, quantidade=total_prestadores, compra_materiais=compra_materiais, 
                               materiais_dvs=materiais_dvs, dvs_socio=dvs_socio, custo_hora=custo_total, beneficios=totalSoma, 
                               telefonia_comunicacao=telefonia_comunicacao, seguro_maquinas_equipamentos=seguro_maquinas_equipamentos, 
                               manutencao=manutencao, dvs_operacao=dvs_operacao, bonus_resultado=bonus_resultado, plr=plr, 
                               horas_extras=horas_extras, exames_adiciona_demissional=exames_adiciona_demissional, 
                               terceirizados=terceirizados, alimentacao=alimentacao, hospedagem=hospedagem, quilometragem=quilometragem, 
                               deslocamento=deslocamento, combustivel=combustivel, estacionamento_pedagio=estacionamento_pedagio, 
                               comissoes=comissoes, seguros_obra_dvs=seguros_obra_dvs, insumos=insumos, manutencao_conservacao=manutencao_conservacao, 
                               distrato_multas=distrato_multas, condominio=custo_condominio, tributos=tributos, lucros=lucros, status='Aberto', valor_sugerido=valor_sugerido)
        return redirect('dashboard')

    return render(request, 'novo_orcamento.html', {'numero_novo_orcamento': numero_novo_orcamento,
                'custo_total': custo_total, 'custo_condominio': custo_condominio, 'totalSoma': totalSoma,
                'total_prestadores': total_prestadores, "capacidade_produtiva": capacidade_produtiva})

def buscar_orcamento(request): 
    q = request.GET.get('search')   
    orcamento = Rubrica.objects.filter(orcamento_id__icontains=q).order_by('orcamento_id')
    return render(request, 'pesquisa_orcamento.html', {'orcamento': orcamento})

def orcamento_view(request):
    orcamento = Rubrica.objects.all()
    orcamento_list = [
        {
            'id': orcamento.id,
            'orcamento': f"{orcamento.id}"
        }
        for orcamento in orcamento
    ]
    return JsonResponse({'orcamento': orcamento_list})


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
    
    if auxiliar_calculo.total_meses_horasprodutivas != 0:
        custo_hora_condominio = auxiliar_calculo.total_gastos_condominio / auxiliar_calculo.total_meses_horasprodutivas
    else:
        custo_hora_condominio = None
        
    if auxiliar_calculo.total_prestadores != 0:
        custo_hora_percapta = custo_hora_condominio / auxiliar_calculo.total_prestadores
    else:
        custo_hora_percapta = None
        
    return render(request, 'lista_condominio.html', {'auxiliar_calculo': auxiliar_calculo, 'custo_hora_condominio': custo_hora_condominio, 'custo_hora_percapta': custo_hora_percapta})


# Função para calcular a média de horas produtivas
def calcular_media_horas_produtivas(request):
    search_query = request.GET.get('search_query')
    
    # Certifique-se de que search_query seja uma string não vazia antes de tentar convertê-la em um inteiro
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
        media = soma_total / quantidade if quantidade > 0 else 0.0
    else:
        soma_total = 0
        quantidade = 0
        media = 0.0
 
    # data_atual = datetime.now()
    
    # resultados = []
    # total_horas_produtivas = 0
    # quantidade_meses = 0
    # quantidade_registros = 0
    
    # data_inicio = data_atual - timedelta(days=365)
    
    # auxiliar_calculo, created = AuxiliarCalculo.objects.get_or_create(pk=1)
    # if created:
    #     auxiliar_calculo.total_meses_calendario = 0
    #     auxiliar_calculo.total_meses_horasprodutivas = 0
    #     auxiliar_calculo.save()

    # # Dicionário para armazenar as horas produtivas de cada mês
    # horas_por_mes = defaultdict(list)
    
    # # Loop para obter os 12 últimos meses e calcular as horas produtivas médias
    # for i in range(12):
    #     # Calcule o mês e o ano para o mês atual
    #     mes = (data_inicio.month + i) % 12
    #     ano = data_inicio.year + ((data_inicio.month + i) // 12)  # Ajuste do ano
        
    #     # Certifique-se de que o mês está dentro do intervalo correto (1 a 12)
    #     if mes <= 0:
    #         mes += 12
    #         ano -= 1
            
    #     # Calcule o primeiro dia e o último dia do mês
    #     primeiro_dia = datetime(ano, mes, 1)
    #     ultimo_dia = primeiro_dia + timedelta(days=31)
        
    #     # Consulte o banco de dados para obter os registros do mês atual
    #     registros_do_mes = CalendarioMensal.objects.filter(mes=mes, ano=ano)
        
    #     for registro in registros_do_mes:
    #         horas_produtivas = registro.horas_produtivas
    #         horas_por_mes[(ano, mes)].append(horas_produtivas)
    #         quantidade_registros += 1
        
    #     # Calcule a média de horas produtivas para cada mês
    # for (ano, mes), horas_lista in horas_por_mes.items():
    #     total_horas_mes = sum(horas_lista)
    #     quantidade_meses += 1

    #     media_mes = total_horas_mes / len(horas_lista) if len(horas_lista) > 0 else 0
        
    #     resultados.append({
    #         'mes': mes,
    #         'ano': ano,
    #         'media_horas_produtivas': media_mes
    #     })
        
    # # Calcule a média anual das médias mensais
    # media_anual = sum([resultado['media_horas_produtivas'] for resultado in resultados]) / quantidade_meses if quantidade_meses > 0 else 0

    # auxiliar_calculo.total_meses_calendario = quantidade_meses
    # auxiliar_calculo.total_meses_horasprodutivas = media_anual
    # auxiliar_calculo.save()
        
    # # Imprima os resultados no console
    # for resultado in resultados:
    #     print(f'Mês: {resultado["mes"]} / Ano: {resultado["ano"]} / Média de Horas Mês: {resultado["media_horas_produtivas"]}')
    # print(f'Quantidade Total de Registros: {quantidade_registros}')
    # print(f'Quantidade Meses com Registros: {quantidade_meses}')
    # print(f'Média Anual de Horas Produtivas: {media_anual}')
    print(f'Soma Total: {soma_total}')
    print(f'Quantidade: {quantidade}')
    print(f'Média: {media}')
    
    response_data = {
        'soma_total': soma_total if soma_total else 0.0,  # Garante que a soma seja 0.0 se for None
        'quantidade': quantidade,
        'media': media,
    }
    
    ano_corrente = datetime.now().year  # Use datetime.now() corretamente
    if ano_consulta == ano_corrente:
        with transaction.atomic():
            auxiliar_calculo = AuxiliarCalculo.objects.first()  # Suponho que haja apenas um registro
            auxiliar_calculo.total_meses_horasprodutivas = media
            auxiliar_calculo.total_meses_calendario = quantidade
            auxiliar_calculo.save()

    return JsonResponse(response_data)
    

def calcular_soma_beneficio_funcionario(request):
    cargos = Cargos.objects.all()
    
    resultados = []

    for cargo in cargos:
        soma_beneficios = Beneficios.objects.filter(cargo=cargo).aggregate(Sum('valor'))['valor__sum'] or 0

        # Cria um dicionário com as informações do funcionário e a soma dos benefícios
        resultado = {
            'cargo': cargo,
            'soma_beneficios': soma_beneficios
        }

        # Adiciona o resultado à lista
        resultados.append(resultado)
        
        print(f"Soma dos benefícios para o cargo {cargo.nome_cargo}: R$ {soma_beneficios}")
        
        # Atualiza os valores na tabela Employee para o funcionário atual
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

# def verificar_cpf(request):
#     cpf = request.GET.get('cpf')

#     return JsonResponse({
#         'cpf_existe': Colaboradores.objects.filter(cpf=cpf).exists()
#     })


def verificar_matricula(request):
    matricula = request.GET.get('matricula')
    if Colaboradores.objects.filter(matricula=matricula).exists():
        return JsonResponse({'matricula_existe': True})
    else:
        return JsonResponse({'matricula_existe': False})


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
    # Crie um arquivo temporário para o PDF
    temp_file = tempfile.NamedTemporaryFile(delete=False)

    # Crie o PDF no arquivo temporário
    doc = SimpleDocTemplate(temp_file, pagesize=landscape(A3))

    data = []
    auxiliares = AuxiliarCalculo.objects.all()  # Use o queryset apropriado aqui

    # Adicionar os nomes das colunas como a primeira linha dos dados
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

    # Abra o arquivo temporário para leitura
    temp_file = open(temp_file.name, 'rb')
    response = HttpResponse(temp_file.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="auxiliar_calculo.pdf"'
    temp_file.close()

    return response
def export_pdf_condominio_temporary():
    # Crie um arquivo temporário para o PDF
    temp_file = tempfile.NamedTemporaryFile(delete=False)

    # Crie o PDF no arquivo temporário
    doc = SimpleDocTemplate(temp_file, pagesize=landscape(A3))

    data = []
    auxiliares = AuxiliarCalculo.objects.all()  # Use o queryset apropriado aqui

    # Adicionar os nomes das colunas como a primeira linha dos dados
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

    # Não feche o arquivo temporário aqui
    return temp_file


def export_csv_condominio(request):
    response = HttpResponse(content_type='text/csv')
    timestamp = timezone.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"auxiliar_calculo_{timestamp}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    response.write(codecs.BOM_UTF8)
    # Crie o objeto CSV
    writer = csv.writer(response, delimiter=';')
    
    # Crie o cabeçalho do CSV
    writer.writerow([
        'Total Salários Gestores', 'Total Salários Prestadores', 'Total Prestadores',
        'Total Meses Condomínio', 'Total Gastos Condomínio', 'Total Meses Calendário',
        'Total Meses Horas Produtivas','Custo Hora Condominio'
    ])

    # Obtenha todos os objetos AuxiliarCalculo
    auxiliares = AuxiliarCalculo.objects.all()

    # Adicione os dados ao CSV
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

# V1 Funcionando, porém não envia arquivo .html
# def enviar_email_personalizado(request, auxiliar_calculo_id):
#     auxiliar_calculo = AuxiliarCalculo.objects.get(pk=auxiliar_calculo_id)

#     if request.method == 'POST':
#         destinatario_email = request.POST['destinatario_email']

#         # Construa o conteúdo do email personalizado
#         subject = 'Assunto do Email'
#         message = f'Olá, aqui estão os valores do modelo AuxiliarCalculo:\n\n' \
#                   f'Total Salários Gestores: {auxiliar_calculo.total_salarios_gestores}\n' \
#                   f'Total Salários Prestadores: {auxiliar_calculo.total_salarios_prestadores}\n' \
#                   f'Total Prestadores: {auxiliar_calculo.total_prestadores}\n' \
#                   f'Total Meses Condomínio: {auxiliar_calculo.total_meses_condominio}\n' \
#                   f'Total Gastos Condomínio: {auxiliar_calculo.total_gastos_condominio}\n' \
#                   f'Total Meses Calendário: {auxiliar_calculo.total_meses_calendario}\n' \
#                   f'Total Meses Horas Produtivas: {auxiliar_calculo.total_meses_horasprodutivas}\n' \
#                   f'Hora Condominio : R${auxiliar_calculo.total_gastos_condominio / auxiliar_calculo.total_meses_horasprodutivas:.2f}\n'

#         # Anexar o arquivo PDF ao e-mail
#         pdf_file = export_pdf_condominio_temporary()
#         pdf_file.seek(0)
#         email = EmailMessage(subject, message, to=[destinatario_email])
#         email.attach('auxiliar_calculo.pdf', pdf_file.read(), 'application/pdf')
#         email.send()

#         # Feche e exclua o arquivo temporário
#         pdf_file.close()

#         return HttpResponse('Email enviado com sucesso!')

#     return render(request, 'dashaboard1.html', {'auxiliar_calculo': auxiliar_calculo})



def enviar_email_personalizado(request, auxiliar_calculo_id):
    auxiliar_calculo = AuxiliarCalculo.objects.get(pk=auxiliar_calculo_id)

    if request.method == 'POST':
        destinatario_email = request.POST['destinatario_email']

        # Calcular a hora do condomínio
        if auxiliar_calculo.total_meses_horasprodutivas != 0:
            hora_condominio = auxiliar_calculo.total_gastos_condominio / auxiliar_calculo.total_meses_horasprodutivas
        else:
            hora_condominio = 'Divisão por zero'

        # Renderize o novo template personalizado em uma string
        context = {
            'auxiliar_calculo': auxiliar_calculo,
            'hora_condominio': hora_condominio,
        }
        email_body = render_to_string('template_email.html', context)

        # Anexe o arquivo PDF ao e-mail
        pdf_file = export_pdf_condominio_temporary()
        pdf_file.seek(0)

        # Crie um objeto EmailMessage
        email = EmailMessage('Assunto do Email', email_body, to=[destinatario_email])

        # Anexe o PDF
        email.attach('auxiliar_calculo.pdf', pdf_file.read(), 'application/pdf')

        # Adicione o conteúdo HTML personalizado como parte do e-mail
        email.content_subtype = 'html'

        # Envie o e-mail
        email.send()

        # Feche e exclua o arquivo temporário
        pdf_file.close()

        return render(request, 'email_condominio.html')

    return render(request, 'dashboard1.html', {'auxiliar_calculo': auxiliar_calculo})


def imprimir_tabela(request):
    # Crie uma resposta HTTP com tipo de conteúdo HTML
    response = HttpResponse(content_type='text/html; charset=utf-8')

    # Abra um buffer para escrever os dados HTML
    buffer = io.StringIO()

    # Crie uma tabela HTML
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

    employees = Employee.objects.all()  # Use o queryset apropriado

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
    # Adicione o botão para acionar a impressão
    buffer.write('<button class="botao-imprimir btn btn-success" onclick="imprimir()">Imprimir Tabela</button>')

    # Adicione o código CSS para ocultar o botão durante a impressão
    buffer.write('<style>')
    buffer.write('@media print {')
    buffer.write('  .botao-imprimir {')
    buffer.write('    display: none;')
    buffer.write('  }')
    buffer.write('  @page {')
    buffer.write('    header: "Impressão Cargos";')  # Defina o título no cabeçalho da página impressa
    buffer.write('  }')
    buffer.write('</style>')

    # Adicione o código JavaScript no final da página
    buffer.write('<script>')
    buffer.write('function imprimir() {')
    buffer.write('  window.print();')
    buffer.write('}')
    buffer.write('</script>')

    # Feche o buffer e defina o conteúdo da resposta HTTP
    buffer.seek(0)
    response.content = buffer.read()

    return response

#  Começo DRE relatório

def dre_report(request):
   q = request.GET.get('search')   
   orcamento = Rubrica.objects.filter(orcamento_id__icontains=q).order_by('orcamento_id')
   return render(request, 'dre_template.html', {'orcamento': orcamento})

