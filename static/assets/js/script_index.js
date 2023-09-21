document.addEventListener('DOMContentLoaded', function () {
    // Recarrega a página ao clicar no botão Home
    document.getElementById("botaoHome").addEventListener("click", function(event) {
        event.preventDefault(); // Impede o comportamento padrão do link
        location.reload(); // Recarrega a página
      });  
    
    // Recarrega a página ao clicar no botão Home
    var closeButtons = document.getElementsByClassName("close");
    for (var i = 0; i < closeButtons.length; i++) {
        closeButtons[i].addEventListener("click", function(event) {
            event.preventDefault(); // Impede o comportamento padrão do link
            location.reload(); // Recarrega a página
        });
    } 

    // Requisição Fetch para endereços
    fetch(enderecoUrl)
        .then(response => response.json())
        .then(data => {
            const selectElements = document.querySelectorAll('select[name="endereco"]');
            selectElements.forEach(selectElement => {
                data.enderecos.forEach(endereco => {
                    const option = document.createElement('option');
                    option.value = endereco.id;
                    option.textContent = endereco.endereco;
                    selectElement.appendChild(option);
                });
            });
        });

    // Requisição Fetch para empresa
    fetch(empresaUrl)
        .then(response => response.json())
        .then(data => {
            const selectElements = document.querySelectorAll('select[name="empresa"]');
            selectElements.forEach(selectElement => {
                data.empresa.forEach(empresa => {
                    const option = document.createElement('option');
                    option.value = empresa.id;
                    option.textContent = empresa.empresa;
                    selectElement.appendChild(option);
                });
            });
        });  

    // Requisição Fetch para Calendário
    fetch(calendarioUrl)
        .then(response => response.json())
        .then(data => {
            const selectElements = document.querySelectorAll('select[name="calendario"]');
            selectElements.forEach(selectElement => {
                data.calendario.forEach(calendario => {
                    const option = document.createElement('option');
                    option.value = calendario.id;
                    option.textContent = calendario.calendario;
                    selectElement.appendChild(option);
                });
            });
        });

    // Requisição Fetch para GastoFixo/Condominio
    fetch(gastosFixosUrl)
        .then(response => response.json())
        .then(data => {
            const selectElements = document.querySelectorAll('select[name="gastosFixos"]');
            selectElements.forEach(selectElement => {
                data.gastosFixos.forEach(gastosFixos => {
                    const option = document.createElement('option');
                    option.value = gastosFixos.id;
                    option.textContent = gastosFixos.gastosFixos;
                    selectElement.appendChild(option);
                });
            });
        });

    // Requisição Fetch para Encargos
    fetch(encargosUrl)
        .then(response => response.json())
        .then(data => {
            const selectElements = document.querySelectorAll('select[name="encargo"]');
            selectElements.forEach(selectElement => {
                data.encargo.forEach(encargo => {
                    const option = document.createElement('option');
                    option.value = encargo.id;
                    option.textContent = encargo.encargo;
                    selectElement.appendChild(option);
                });
            });
        });

    // Requisição Fetch para Beneficios
    fetch(beneficiosUrl)
        .then(response => response.json())
        .then(data => {
            const selectElements = document.querySelectorAll('select[name="beneficio"]');
            selectElements.forEach(selectElement => {
                data.beneficio.forEach(beneficio => {
                    const option = document.createElement('option');
                    option.value = beneficio.id;
                    option.textContent = beneficio.beneficio;
                    selectElement.appendChild(option);
                });
            });
        });


    // scritp para adicionar mais campos de mão de obra
    // document.getElementById('maisMaoDeObra').addEventListener('click', function () {
    //     const maoDeObraContainer = document.querySelector('.mao-de-obra-container');
    //     const clone = maoDeObraContainer.cloneNode(true);
    //     const matriculaInput = clone.querySelector('input[name="matricula"]');
    //     const nomeInput = clone.querySelector('input[name="nome"]');
    //     const cpfInput = clone.querySelector('input[name="cpf"]');
    //     const salarioInput = clone.querySelector('input[name="salario"]');
    //     const beneficiosInput = clone.querySelector('input[name="beneficios"]');
    //     const encargosInput = clone.querySelector('input[name="encargos"]');
    //     matriculaInput.value = '';
    //     nomeInput.value = '';
    //     cpfInput.value = '';
    //     salarioInput.value = '';
    //     beneficiosInput.value = '';
    //     encargosInput.value = '';
    //     maoDeObraContainer.parentNode.insertBefore(clone, maoDeObraContainer.nextSibling);
    // });

    // Alerta da empresas cadastrada, ainda não funcionando
    const urlParams = new URLSearchParams(window.location.search);
    const success = urlParams.get('success');

    if (success === 'true') {
        alert('Empresa cadastrada com sucesso!');
    }

    // Validação do número da empresa
    document.addEventListener('DOMContentLoaded', function () {
        const numeroEmpresaInput = document.querySelector('input[name="numero_empresa"]');

        numeroEmpresaInput.addEventListener('input', function () {
            const maxDigits = 4;
            if (this.value.length > maxDigits) {
                alert(`Digite no máximo ${maxDigits} dígitos.`);
                this.value = this.value.slice(0, maxDigits);
            }
        });
    });

    // Ative todos os checkboxes de switch na página
    document.addEventListener('DOMContentLoaded', function () {
        var switchCheckboxes = document.querySelectorAll('.form-switch input[type="checkbox"]');
        switchCheckboxes.forEach(function (checkbox) {
            new bootstrap.Switch(checkbox);
        });
    });

});

// Verifica se o modal deve ser mantido aberto e se há mensagens de erro
document.addEventListener("DOMContentLoaded", function () {
    if (keepModalOpen && messagesExist) {

        $('#modalSenha').modal('show');
    }
});

// Função para buscar e preencher os campos do endereço a partir do CEP
$(document).ready(function () {
    $("#btnBuscarCEP").click(function () {
        var cep = $("#cepInput").val();

        var url = "https://viacep.com.br/ws/" + cep + "/json/";

        // Fazendo a requisição AJAX para a API ViaCEP
        $.get(url, function (data) {
            $("#logradouro").val(data.logradouro);
            $("#endereco").val(data.endereco);
            $("#bairro").val(data.bairro);
            $("#cidade").val(data.localidade);
            $("#estado").val(data.uf);
        });
    });
});

// Função para buscar a lista de Funcionários
function popularSelectFuncionarioPorClasse(classeSelect) {
    const selects = document.querySelectorAll('.' + classeSelect);

    selects.forEach(funcionarioSelect => {
        // Adicione a primeira opção "Selecione um Funcionário..."
        const firstOption = document.createElement('option');
        firstOption.value = '';
        firstOption.textContent = 'Selecione um Funcionário...';
        funcionarioSelect.appendChild(firstOption);

        fetch(colaboradoresUrl)
            .then(response => response.json())
            .then(data => {
                const options = []; // Array para armazenar as opções de funcionários

                data.colaboradores.forEach(colaborador => {
                    const option = document.createElement('option');
                    option.value = colaborador.id;
                    option.textContent = colaborador.nome;
                    options.push(option); // Adicione a opção ao array
                });

                // Remova todas as opções existentes no select
                while (funcionarioSelect.options.length > 1) {
                    funcionarioSelect.remove(1);
                }

                // Ordene as opções em ordem alfabética com base no texto
                options.sort((a, b) => a.textContent.localeCompare(b.textContent));

                // Adicione as opções ordenadas de volta ao select
                options.forEach(option => {
                    funcionarioSelect.appendChild(option);
                });
            });
    });
}


document.addEventListener('DOMContentLoaded', function () {
    popularSelectFuncionarioPorClasse('funcionarioInputS');
});

//Função para buscar a lista de Funcionários só Prestadores
const colaboradoresUrlFilter = 'colaboradores_view_filter/';

function popularSelectFuncionarioPorClasseC(classeSelect) {
    const selects = document.querySelectorAll('.' + classeSelect);

    selects.forEach(funcionariosSelect => {
        fetch(colaboradoresUrlFilter)
            .then(response => response.json())
            .then(data => {
                const options = []; // Array para armazenar as opções de funcionários

                data.colaboradores.forEach(colaborador => {
                    const option = document.createElement('option');
                    option.value = colaborador.id;
                    option.textContent = colaborador.nome;
                    options.push(option); // Adicione a opção ao array
                });

                // Remova todas as opções existentes no select
                while (funcionariosSelect.options.length > 0) {
                    funcionariosSelect.remove(0);
                }

                // Ordene as opções em ordem alfabética com base no texto
                options.sort((a, b) => a.textContent.localeCompare(b.textContent));

                // Adicione as opções ordenadas de volta ao select
                options.forEach(option => {
                    funcionariosSelect.appendChild(option);
                });
            });
    });
}


document.addEventListener('DOMContentLoaded', function () {
    popularSelectFuncionarioPorClasseC('funcionarioInputC');
});

// Função para buscar a lista de Cargos
function popularSelectCargoPorClasse(classeSelect) {
    const selects = document.querySelectorAll('.' + classeSelect);

    selects.forEach(cargoSelect => {
        // Adicione a primeira opção "Selecione um Cargo..."
        const firstOption = document.createElement('option');
        firstOption.value = '';
        firstOption.textContent = 'Selecione um Cargo...';
        cargoSelect.appendChild(firstOption);

        fetch(cargosUrl)
            .then(response => response.json())
            .then(data => {
                const options = []; // Array para armazenar as opções de cargos

                data.cargos.forEach(cargo => {
                    const option = document.createElement('option');
                    option.value = cargo.id;
                    option.textContent = cargo.nome_cargo;
                    options.push(option); // Adicione a opção ao array
                });

                // Remova todas as opções existentes no select
                while (cargoSelect.options.length > 1) {
                    cargoSelect.remove(1);
                }

                // Ordene as opções em ordem alfabética com base no texto
                options.sort((a, b) => a.textContent.localeCompare(b.textContent));

                // Adicione as opções ordenadas de volta ao select
                options.forEach(option => {
                    cargoSelect.appendChild(option);
                });
            });
    });
}

    
document.addEventListener('DOMContentLoaded', function () {
    popularSelectCargoPorClasse('inputCargoS');
});

//Função para calcular dias úteis na modal do Calendário
function calcularDiasUteis(ano, mes) {
    const inicioMes = new Date(ano, mes - 1, 1);
    const fimMes = new Date(ano, mes, 0);
    let diasUteis = 0;

    for (let dia = inicioMes; dia <= fimMes; dia.setDate(dia.getDate() + 1)) {
        if (dia.getDay() !== 0 && dia.getDay() !== 6) {
            diasUteis++;
        }
    }
    console.log(diasUteis);

    // Crie uma cópia de inicioMes para contar os sábados
    const inicioMesCopia = new Date(ano, mes - 1, 1);
    let numSabados = 0;
    while (inicioMesCopia.getMonth() === mes - 1) {
        if (inicioMesCopia.getDay() === 6) {
            numSabados++;
        }
        inicioMesCopia.setDate(inicioMesCopia.getDate() + 1);
    }
    console.log(numSabados);

    // Adicione metade de um dia útil para cada sábado
    diasUteis += numSabados * 0.5;
    console.log(diasUteis);

    return diasUteis;
}


// função para calcular horas produtivas do funcionario
document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("#calendarioForm");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const mes = parseInt(document.querySelector("#mes").value);
        const ano = parseInt(document.querySelector("#ano").value);
        const jornadaDiariaValue = document.querySelector("#jornada_diaria").value;
        const funcionario = document.querySelector("#funcionario").value;        
        const feriadoValue = document.querySelector("#feriados").value;

        if (isNaN(mes) || isNaN(ano) || jornadaDiariaValue === "" || funcionario === "") {
            alert("Preencha todos os campos obrigatórios corretamente.");
            return;
        }

        const jornadaDiaria = parseFloat(jornadaDiariaValue);
        const feriado = (feriadoValue);

        const diasUteis = calcularDiasUteis(ano, mes);
        const horasProdutivas = (diasUteis - feriado) * jornadaDiaria;

        // Preencher os valores calculados nos campos de horas_produtivas e dias_uteis
        document.querySelector("#horas_produtivas").value = horasProdutivas;
        document.querySelector("#dias_uteis").value = diasUteis;

        $.ajax({
            type: "POST",
            url: "inserir_calendario/",
            data: $(form).serialize(), // Use $(form) para serializar o formulário
            success: function(response) {
                // Aqui você pode adicionar qualquer ação adicional após o sucesso da requisição
                form.reset();
                $("#successMessageCalendario").show();
            }
        });
    });
});

// Função para abrir modal personalizado Empresa
const openModalButtonEmpresa = document.getElementById("openModalButtonEmpresa");
const modalEmpresa = document.getElementById("myModalEmpresa");
const closeButtonsEmpresa = document.getElementsByClassName("close");

openModalButtonEmpresa.addEventListener("click", () => {
    modalEmpresa.style.display = "block";
});

for (const closeButtonsEmp of closeButtonsEmpresa) {
    closeButtonsEmp.addEventListener("click", () => {
        modalEmpresa.style.display = "none";
    });
}

// Função para abrir modal personalizado Colaboradores
const openModalButtonColaboradores = document.getElementById("openModalButtonColaboradores");
const modalColaboradores = document.getElementById("myModalColaboradores");
const closeButtonsColaboradores = document.getElementsByClassName("close");

openModalButtonColaboradores.addEventListener("click", () => {
    modalColaboradores.style.display = "block";
});

for (const closeButtonsCol of closeButtonsColaboradores) {
    closeButtonsCol.addEventListener("click", () => {
        modalColaboradores.style.display = "none";
    });
}

// Função para abrir modal personalizado Endereço
const openModalButtonEndereco = document.getElementById("openModalButtonEndereco");
const modalEndereco = document.getElementById("myModalEndereco");
const closeButtonsEndereco = document.getElementsByClassName("close");

openModalButtonEndereco.addEventListener("click", () => {
    modalEndereco.style.display = "block";
});

for (const closeButtonsEnd of closeButtonsEndereco) {
    closeButtonsEnd.addEventListener("click", () => {
        modalEndereco.style.display = "none";
    });
}

// Função para abrir modal personalizado Cargo
const openModalButtonCargo = document.getElementById("openModalButtonCargo");
const modalCargo = document.getElementById("myModalCargo");
const closeButtonsCargo = document.getElementsByClassName("close");

openModalButtonCargo.addEventListener("click", () => {
    modalCargo.style.display = "block";
});

for (const closeButtonCa of closeButtonsCargo) {
    closeButtonCa.addEventListener("click", () => {
        modalCargo.style.display = "none";
    });
}

// Função para abrir modal personalizado Calendário
const openModalButtonCalendario = document.getElementById("openModalButtonCalendario");
const modalCalendario = document.getElementById("myModalCalendario");
const closeButtonsCalendario = document.getElementsByClassName("close");

openModalButtonCalendario.addEventListener("click", () => {
    modalCalendario.style.display = "block";
});

for (const closeButtonCal of closeButtonsCalendario) {
    closeButtonCal.addEventListener("click", () => {
        modalCalendario.style.display = "none";
    });
}

// Função para abrir modal personalizado Condominio
const openModalButtonCondominio = document.getElementById("openModalButtonCondominio");
const modalCondominio = document.getElementById("myModalCondominio");
const closeButtonsCondominio = document.getElementsByClassName("close");

openModalButtonCondominio.addEventListener("click", () => {
    modalCondominio.style.display = "block";
});

for (const closeButtonCon of closeButtonsCondominio) {
    closeButtonCon.addEventListener("click", () => {
        modalCondominio.style.display = "none";
    });
}

// Função para abrir modal personalizado Encargos
const openModalButtonEncargos = document.getElementById("openModalButtonEncargos");
const modalEncargos = document.getElementById("myModalEncargos");
const closeButtonsEncargos = document.getElementsByClassName("close");

openModalButtonEncargos.addEventListener("click", () => {
    modalEncargos.style.display = "block";
});

for (const closeButtonEnc of closeButtonsEncargos) {
    closeButtonEnc.addEventListener("click", () => {
        modalEncargos.style.display = "none";
    });
}

// Função para abrir modal personalizado Beneficios
const openModalButtonBeneficios = document.getElementById("openModalButtonBeneficios");
const modalBeneficios = document.getElementById("myModalBeneficios");
const closeButtonsBeneficios = document.getElementsByClassName("close");

openModalButtonBeneficios.addEventListener("click", () => {
    modalBeneficios.style.display = "block";
});

for (const closeButtonBen of closeButtonsBeneficios) {
    closeButtonBen.addEventListener("click", () => {
        modalBeneficios.style.display = "none";
    });
}

// Função para abrir modal personalizado Vincular Cargos
const openModalButtonVincularCargos = document.getElementById("openModalButtonVincularCargos");
const modalVincularCargos = document.getElementById("myModalVincularCargos");
const closeButtonsVincularCargos = document.getElementsByClassName("close");

openModalButtonVincularCargos.addEventListener("click", () => {
    modalVincularCargos.style.display = "block";
});

for (const closeButtonVinc of closeButtonsVincularCargos) {
    closeButtonVinc.addEventListener("click", () => {
        modalVincularCargos.style.display = "none";
    });
}

// Função para abrir modal personalizado Orçamento
const openModalButtonOrcamento = document.getElementById("openModalButtonOrcamento");
const modalOrcamento = document.getElementById("myModalOrcamento");
const closeButtonsOrcamento = document.getElementsByClassName("close");

openModalButtonOrcamento.addEventListener("click", () => {
    modalOrcamento.style.display = "block";
});

for (const closeButtonOrc of closeButtonsOrcamento) {
    closeButtonOrc.addEventListener("click", () => {
        modalOrcamento.style.display = "none";
    });
}

// Cadastro OK Mão de obra (msg em tela e não fecha modal) 
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('maoDeObraForm');
    const successMessage = document.getElementById('successMessage');
    const submitBtn = document.getElementById('submitBtn');

    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        submitBtn.disabled = true;

        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                successMessage.style.display = 'block';
                form.reset();
            } else {
                alert('Ocorreu um erro ao cadastrar a mão de obra.');
            }
        } catch (error) {
            console.error('Erro:', error);
            alert('Ocorreu um erro ao cadastrar a mão de obra.');
        } finally {
            submitBtn.disabled = false;
        }
    });

    // Cadastro Condominio Lista (msg em tela e não fecha modal)
    $(document).ready(function() {
        $("#formDespesasLista").submit(function(event) {
            event.preventDefault();
            // Fazer uma requisição AJAX para enviar os dados do formulário
            $.ajax({
                type: "POST",
                url: "inserir_gasto_fixo/",
                data: $(this).serialize(),
                success: function(response) {
                    $("#formDespesasLista input[type=text], #formDespesasLista input[type=number]").val("");
                    $("#successMessageLista").show();
                }
            });
        });
    });

    // Cadastro Condominio Total (msg em tela e não fecha modal)
    $(document).ready(function() {
        $("#formDespesasTotal").submit(function(event) {
            event.preventDefault();
            // Fazer uma requisição AJAX para enviar os dados do formulário
            $.ajax({
                type: "POST",
                url: "inserir_gasto_fixo/",
                data: $(this).serialize(),
                success: function(response) {
                    $("#formDespesasTotal input[type=text], #formDespesasTotal input[type=number]").val("");
                    $("#successMessageTotal").show();
                }
            });
        });
    });

    // Cadastro Beneficio (msg em tela e não fecha modal)
    $(document).ready(function() {
        $("#formBeneficio").submit(function(event) {
            event.preventDefault();
            // Fazer uma requisição AJAX para enviar os dados do formulário
            $.ajax({
                type: "POST",
                url: "inserir_beneficio/",
                data: $(this).serialize(),
                success: function(response) {
                    $("#formBeneficio input[type=text], #formBeneficio input[type=number]").val("");
                    $("#successMessageBeneficio").show();
                }
            });
        });
    });

    // Cadastro Cargo (msg em tela e não fecha modal)
    $(document).ready(function() {
        $("#formCargo").submit(function(event) {
            event.preventDefault();
            // Fazer uma requisição AJAX para enviar os dados do formulário
            $.ajax({
                type: "POST",
                url: "inserir_cargo/",
                data: $(this).serialize(),
                success: function(response) {
                    $("#formCargo input[type=text], #formCargo input[type=number]").val("");
                    $("#successMessageCargo").show();
                }
            });
        });
    });

    // Cadastro de Vinculos (msg em tela e não fecha modal)
    $(document).ready(function() {
        $("#FormVincularCargos").submit(function(event) {
            event.preventDefault();
            // Fazer uma requisição AJAX para enviar os dados do formulário
            $.ajax({
                type: "POST",
                url: "inserir_vinculo/",
                data: $(this).serialize(),
                success: function(response) {
                    $("#FormVincularCargos input[type=text], #FormVincularCargos input[type=number]").val("");
                    $("#successMessageVinculo").show();
                    $(".inputCargoS").val("");
                }
            });
        });
    });

    // Cadastro Encargo (msg em tela e não fecha modal)
    $(document).ready(function() {
        $("#formEncargo").submit(function(event) {
            // event.preventDefault();
            // Obtenha os valores dos campos do formulário
            const colaboradorId = $("#funcionario").val();
            const cargoId = $("#cargos").val();
            const setor = $("#setor").val();
    
            // Fazer uma requisição AJAX para verificar se o encargo já existe no banco
            $.ajax({
                type: "GET",
                url: "encargo_view/",
                data: {
                    colaborador_id: colaboradorId,
                    cargo_id: cargoId,
                    setor: setor
                },
                success: function(response) {
                    if (response.exists) {
                        window.location.href = "/encargo_duplicado.html";
                        console.log(window.location.href)
                    } else {
                        // Continuar com a submissão do formulário se não existir
                        $.ajax({
                            type: "POST",
                            url: "inserir_encargo/",
                            data: $("#formEncargo").serialize(),
                            success: function(response) {
                                // Limpar os campos do formulário após o envio bem-sucedido
                                $("#formEncargo input[type=text], #formEncargo input[type=number]").val("");
                                $(".inputCargoS").val("");
                                $(".funcionarioInputS").val("");
                                
                                // Exibir a mensagem de sucesso
                                $("#successMessageEncargo").show();
    
                                // Fechar o modal manualmente (substitua "#seuModal" pelo seletor correto)
                                $("#seuModal").modal("hide");
                            },
                            error: function(xhr, status, error) {
                                alert("Erro ao enviar o formulário. Por favor, tente novamente mais tarde.");
                                console.error(error);
                            }
                        });
                    }
                },
                error: function(xhr, status, error) {
                    alert("Erro ao verificar o encargo. Por favor, tente novamente mais tarde.");
                    console.error(error);
                }
            });
        });
    });
});


    //Recupera valores do Banco de Dados para Usar no Rateio da Estrutura do RH
    $(document).ready(function() {
        $(".nav-sub").on("click", function(e) {
            e.preventDefault();
    
            // Recupera a URL da view a partir do atributo de dados
            var url = $(this).data("url");
            
            // Realiza uma requisição AJAX para a URL da view que executa a função
            $.ajax({
                type: "GET",
                url: url,
                success: function(response) {
                    console.log("Dados atualizados com sucesso!");
                },
                error: function(error) {
                    console.error("Erro ao atualizar dados:", error);
                }
            });
        });
    });