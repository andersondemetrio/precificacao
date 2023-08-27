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
from .forms import EmployeeForm
from .models import GastosFixos,Colaboradores,Cargos, Endereco, Empresa,CalendarioMensal,Employee
import csv

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import io
from reportlab.lib.pagesizes import landscape, A3


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

def inserir_gasto_fixo(request):
    if request.method == 'POST':
        descricao = request.POST['descricao']
        valor = request.POST['valor']
        GastosFixos.objects.create(descricao=descricao, valor=valor)
        return redirect('dashboard')
    return render(request, 'dashboard1.html', context={})

def inserir_mao_de_obra(request):
    if request.method == 'POST':
        matricula = request.POST['matricula']
        nome = request.POST['nome']
        cpf = request.POST['cpf']
        salario = request.POST['salario']
        beneficios = request.POST['beneficios']
        encargos = request.POST['encargos']
        cargo_id = request.POST['cargo']  # Certifique-se de que esse é o nome correto do campo
        # endereco_id = request.POST['endereco']

        cargo = Cargos.objects.get(id=cargo_id)
        
        mao_de_obra = Colaboradores(
            matricula=matricula,
            nome=nome,
            cpf=cpf,
            salario=salario,
            beneficios=beneficios,
            encargos=encargos,
            cargo=cargo,  # Associando o cargo à mão de obra
            # endereco_id=endereco_id
        )
        mao_de_obra.save()
        return HttpResponse("Mão de obra cadastrada com sucesso!")

# Funções do CRUD de cargos

def inserir_cargo(request):
    print("request.POST")
    if request.method == 'POST':
        nome_cargo = request.POST['nome_cargo']

        cargo = Cargos(
            nome_cargo=nome_cargo,
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

        cargo.nome_cargo = nome_cargo        
        cargo.save()
        return redirect('dashboard')

    return render(request, 'dashboard1.html', {'cargo': cargo})

def cargos_vieww(request):
    cargos = Cargos.objects.all()
    cargos_list = [{'id': cargo.id, 'nome_cargo': cargo.nome_cargo} for cargo in cargos]
    return JsonResponse({'cargos': cargos_list})

def busca_cargo(request): 
    q = request.GET.get('search')   
    cargos = Cargos.objects.filter(nome_cargo__icontains=q).order_by('id')
    return render(request, 'pesquisa_cargo.html', {'cargo': cargos})

def deletar_cargo(request, cargo_id):
    if request.method == 'POST':
        try:
            cargo = Cargos.objects.get(pk=cargo_id)
            cargo.delete()
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

def inserir_endereco(request):
    if request.method == 'POST':
        logradouro = request.POST['logradouro']
        numero = request.POST['numero']
        complemento = request.POST['complemento']
        bairro = request.POST['bairro']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        Endereco.objects.create(logradouro=logradouro, numero=numero, complemento=complemento, bairro=bairro, cidade=cidade, 
                                estado=estado)
        return redirect('dashboard')
    return render(request, 'dashboard1.html', context={})

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

def inserir_beneficio(request):
    return render(request, 'dashboard1.html', context={})

# função para inserir o encargo trabalhista para o funcionário

def inserir_encargo(request):
    if request.method == 'POST':
        colaborador_id = request.POST['funcionario']
        colaborador = Colaboradores.objects.get(id=colaborador_id)
        setor = request.POST['setor']
        cargo = request.POST['cargo']

        # Verificar se já existe um encargo para o mesmo colaborador, setor e cargo
        if Employee.objects.filter(colaborador=colaborador, setor=setor, cargo=cargo).exists():
            # Lidar com encargo já existente (pode ser uma renderização de erro ou outra ação)
            return render(request, 'encargo_duplicado.html')

        # Cálculo do salário nominal
        salario_nominal = float(colaborador.salario)
        
        # Definir valores padrão para periculosidade e rateio
        periculosidade = 0
        rateio = 0

        # Verificar se o setor é "Gestores" e ajustar a periculosidade e rateio
        if setor == "Gestores":
            periculosidade = 0
            rateio = 0
        else:
            periculosidade = salario_nominal * 0.3
            rateio = (salario_nominal + periculosidade) * 0.2  # Exemplo de cálculo para o rateio

        # Cálculos dos outros campos...
        fgts = (salario_nominal + periculosidade) * 0.08
        terco_ferias = (salario_nominal + periculosidade)/3 / 12
        fgts_ferias = terco_ferias * 0.08
        decimo_terceiro = (salario_nominal + periculosidade) / 12
        fgts_decimo_terceiro = decimo_terceiro * 0.08
        multa_rescisoria = (fgts + fgts_ferias + fgts_decimo_terceiro) * 0.4
        custo_mes = (salario_nominal + periculosidade + fgts + terco_ferias +
                     fgts_ferias + decimo_terceiro + fgts_decimo_terceiro +
                     multa_rescisoria + rateio)

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
            rateio=rateio,
            custo_mes=custo_mes,
        )
        # Redirecionar para a página desejada após a inserção
        return redirect('dashboard')
    
    return render(request, 'dashboard1.html')




def inserir_data(request):
    return render(request, 'dashboard1.html', context={})    

def inserir_jornada(request):
    return render(request, 'dashboard1.html', context={})

def inserir_horas(request):
    return render(request, 'dashboard1.html', context={})       



# Função para validar a inserção dos dias uties e horas produtiva do mes 

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

        return redirect("dashboard")  # Redirecionar para uma página de sucesso

    return render(request, "dashboard1.html")

# funçaõ para listar os colaboradores no select do calendario
def colaboradores_view(request):
    colaboradores = Colaboradores.objects.all()
    colaboradores_list = [{'id': colaborador.id, 'nome': colaborador.nome} for colaborador in colaboradores]
    return JsonResponse({'colaboradores': colaboradores_list})


# Função para listar os encargos dos colaboradores
def lista_salarios_view(request):
    # Consulta para buscar os registros da tabela Employee juntamente com os dados dos colaboradores
    employees = Employee.objects.select_related('colaborador').all()

    context = {
        'employees': employees
    }

    return render(request, 'lista_salarios.html', context)

# Função para exportar os encargos para o CSV
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="encargos_funcionarios.csv"'

    writer = csv.writer(response)
    writer.writerow(['Colaborador', 'Salário', 'Setor', 'Cargo', 'Periculosidade', 'FGTS', '1/3 Férias', 'FGTS Férias', '13º Salário', 'FGTS 13º', 'Multa Rescisória', 'Rateio', 'Custo Mês'])

    employees = Employee.objects.all()  # Use apropriate queryset here
    for employee in employees:
        writer.writerow([employee.colaborador.nome, employee.colaborador.salario, employee.setor, employee.cargo, employee.periculosidade, employee.fgts, employee.um_terco_ferias, employee.fgts_ferias, employee.decimo_terceiro, employee.fgts_decimo_terceiro, employee.multa_rescisoria, employee.rateio, employee.custo_mes])

    return response

# funcão para exportar os encargos para o PDF
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="salaries.pdf"'

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A3))

    data = []
    employees = Employee.objects.all()  # Use appropriate queryset here
    for employee in employees:
        data.append([
            employee.colaborador.nome,
            f"R$ {employee.colaborador.salario:.2f}",
            employee.setor,
            employee.cargo,
            f"R$ {employee.periculosidade:.2f}",
            f"R$ {employee.fgts:.2f}",
            f"R$ {employee.um_terco_ferias:.2f}",
            f"R$ {employee.fgts_ferias:.2f}",
            f"R$ {employee.decimo_terceiro:.2f}",
            f"R$ {employee.fgts_decimo_terceiro:.2f}",
            f"R$ {employee.multa_rescisoria:.2f}",
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
