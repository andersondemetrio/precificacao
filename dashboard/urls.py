from django.urls import path
from dashboard.views import *
urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('alterar_senha/', alterar_senha, name='alterar_senha'),
    
    path('inserir_empresa/', inserir_empresa, name='inserir_empresa'),
    path('listar_empresa/', empresa_view, name='empresa_view'),
    path('editar_empresa/<int:id>/', editar_empresa, name='editar_empresa'),
    path('buscar_empresa/', buscar_empresa, name='buscar_empresa'),
    path('detalhes_empresa/<int:id>/', detalhes_empresa, name='detalhes_empresa'),
    path('deletar_empresa/<int:empresa_id>/', deletar_empresa, name='deletar_empresa'),
    
    path('inserir_endereco/', inserir_endereco, name='inserir_endereco'),
    path('listar_enderecos/', endereco_view, name='endereco_view'),
    path('editar_endereco/<int:id>/', editar_endereco, name='editar_endereco'),
    path('buscar_endereco/', buscar_endereco, name='buscar_endereco'),
    path('detalhes_endereco/<int:id>/', detalhes_endereco, name='detalhes_endereco'),
    path('deletar_endereco/<int:endereco_id>/', deletar_endereco, name='deletar_endereco'),
    
    path('inserir_cargo/', inserir_cargo, name='inserir_cargo'),
    path('editar_cargo/<int:id>/', editar_cargo, name='editar_cargo'),
    path('cargos_vieww/', cargos_vieww, name='cargos_vieww'),
    path('buscar_cargo/', buscar_cargo, name='buscar_cargo'),
    path('detalhes_cargo/<int:id>/', detalhes_cargo, name='detalhes_cargo'),
    path('deletar_cargo/<int:cargo_id>/', deletar_cargo, name='deletar_cargo'),
    path('verificar_cpf/', verificar_cpf, name='verificar_cpf'),
    
    path('inserir_mao_de_obra/', inserir_mao_de_obra, name='inserir_mao_de_obra'),
    path('colaboradores_view/',colaboradores_view,name='colaboradores_view'),
    path('editar_colaborador/<int:id>/', editar_colaborador, name='editar_colaborador'),
    path('buscar_colaborador/', buscar_colaborador, name='buscar_colaborador'),
    path('detalhes_colaborador/<int:id>/', detalhes_colaborador, name='detalhes_colaborador'),
    path('deletar_colaborador/<int:colaborador_id>/', deletar_colaborador, name='deletar_colaborador'),
    
    path('inserir_calendario/',inserir_calendario,name='inserir_calendario'),
    path('editar_calendario/<int:id>/', editar_calendario, name='editar_calendario'),
    path('calendario_view/', calendario_view, name='calendario_view'),
    path('buscar_calendario/', buscar_calendario, name='buscar_calendario'),
    path('detalhes_calendario/<int:id>/', detalhes_calendario, name='detalhes_calendario'),
    path('deletar_calendario/<int:calendario_id>/', deletar_calendario, name='deletar_calendario'),    
    
    path('inserir_gasto_fixo/', inserir_gasto_fixo, name='inserir_gasto_fixo'),
    path('editar_gasto_fixo/<int:id>/', editar_gasto_fixo, name='editar_gasto_fixo'),
    path('gasto_fixo_view/', gasto_fixo_view, name='gasto_fixo_view'),
    path('buscar_gasto_fixo/', buscar_gasto_fixo, name='buscar_gasto_fixo'),
    path('detalhes_gasto_fixo/<int:id>/', detalhes_gasto_fixo, name='detalhes_gasto_fixo'),
    path('deletar_gasto_fixo/<int:gasto_fixo_id>/', deletar_gasto_fixo, name='deletar_gasto_fixo'),      
    
    path('inserir_encargo/', inserir_encargo, name='inserir_encargo'),  
    path('buscar_encargo/', buscar_encargo, name='buscar_encargo'),
    path('encargo_view/', encargo_view, name='encargo_view'),
    path('deletar_encargo/<int:deletar_encargo_id>/', deletar_encargo, name='deletar_encargo'),  
    
    path('inserir_beneficio/', inserir_beneficio, name='inserir_beneficio'),
    path('buscar_beneficio/', buscar_beneficio, name='buscar_beneficio'),
    path('beneficio_view/', beneficio_view, name='beneficio_view'),
    path('deletar_beneficio/<int:deletar_beneficio_id>/', deletar_beneficio, name='deletar_beneficio'),  
    
    path('inserir_data/', inserir_data, name='inserir_data'),
    path('inserir_jornada/', inserir_jornada, name='inserir_jornada'),
    path('inserir_horas/', inserir_horas, name='inserir_horas'),      
    path('lista_salarios_view/', lista_salarios_view, name='lista_salarios_view'),
    path('lista_horas_condiminio_view/', lista_horas_condiminio_view, name='lista_horas_condiminio_view'),
    path('atualizar_dados_banco/', atualizar_dados_banco, name='atualizar_dados_banco'),
    path('export_csv/',export_csv, name='export_csv'),
    path('export_pdf/', export_pdf, name='export_pdf'),
]