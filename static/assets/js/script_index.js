document.addEventListener('DOMContentLoaded', function () {

    // Requisição Fetch para cargos
    fetch(cargosUrl)
        .then(response => response.json())
        .then(data => {
            const selectElement = document.querySelector('select[name="cargo"]');
            data.cargos.forEach(cargo => {
                const option = document.createElement('option');
                option.value = cargo.id;
                option.textContent = cargo.nome_cargo;
                selectElement.appendChild(option);
            });
        });

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

    // Requisição Fetch para endereços
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


    // script para adicionar mais campos de despesas fixas

    document.getElementById('maisDespesasFixas').addEventListener('click', function () {
        const despesaContainer = document.querySelector('.despesa-container');
        const clone = despesaContainer.cloneNode(true);
        const descricaoInput = clone.querySelector('input[name="descricao"]');
        const valorInput = clone.querySelector('input[name="valor"]');
        descricaoInput.value = '';
        valorInput.value = '';
        despesaContainer.parentNode.insertBefore(clone, despesaContainer.nextSibling);
    });

    // scritp para adicionar mais campos de mão de obra
    document.getElementById('maisMaoDeObra').addEventListener('click', function () {
        const maoDeObraContainer = document.querySelector('.mao-de-obra-container');
        const clone = maoDeObraContainer.cloneNode(true);
        const matriculaInput = clone.querySelector('input[name="matricula"]');
        const nomeInput = clone.querySelector('input[name="nome"]');
        const cpfInput = clone.querySelector('input[name="cpf"]');
        const salarioInput = clone.querySelector('input[name="salario"]');
        const beneficiosInput = clone.querySelector('input[name="beneficios"]');
        const encargosInput = clone.querySelector('input[name="encargos"]');
        matriculaInput.value = '';
        nomeInput.value = '';
        cpfInput.value = '';
        salarioInput.value = '';
        beneficiosInput.value = '';
        encargosInput.value = '';
        maoDeObraContainer.parentNode.insertBefore(clone, maoDeObraContainer.nextSibling);
    });

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
        // Exibe o modal
        $('#modalSenha').modal('show');
    }
});

// Função para buscar e preencher os campos do endereço a partir do CEP
$(document).ready(function () {
    // Capturando o evento de clique no botão de buscar CEP
    $("#btnBuscarCEP").click(function () {
        // Capturando o valor do campo de entrada do CEP
        var cep = $("#cepInput").val();

        // Construindo a URL da API ViaCEP com o CEP inserido
        var url = "https://viacep.com.br/ws/" + cep + "/json/";

        // Fazendo a requisição AJAX para a API ViaCEP
        $.get(url, function (data) {
            // Preenchendo os campos do formulário com os dados retornados pela API
            $("#logradouro").val(data.logradouro);
            $("#endereco").val(data.endereco);
            $("#bairro").val(data.bairro);
            $("#cidade").val(data.localidade);
            $("#estado").val(data.uf);
        });
    });
});

console.log(colaboradoresUrl)
document.addEventListener('DOMContentLoaded', function () {
    const funcionarioSelect = document.getElementById('funcionario');

    fetch(colaboradoresUrl)
        .then(response => response.json())
        .then(data => {
            data.colaboradores.forEach(colaborador => {
                const option = document.createElement('option');
                option.value = colaborador.id;
                option.textContent = colaborador.nome;
                funcionarioSelect.appendChild(option);
            });
        });
});

function calcularDiasUteis(ano, mes) {
    const inicioMes = new Date(ano, mes - 1, 1);
    const fimMes = new Date(ano, mes, 0);
    let diasUteis = 0;

    for (let dia = inicioMes; dia <= fimMes; dia.setDate(dia.getDate() + 1)) {
        if (dia.getDay() !== 0 && dia.getDay() !== 6) {
            diasUteis++;
        }
    }

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

        if (isNaN(mes) || isNaN(ano) || jornadaDiariaValue === "" || funcionario === "") {
            alert("Preencha todos os campos obrigatórios corretamente.");
            return;
        }

        const jornadaDiaria = parseFloat(jornadaDiariaValue);

        const diasUteis = calcularDiasUteis(ano, mes);
        const horasProdutivas = diasUteis * jornadaDiaria;

        // Preencher os valores calculados nos campos de horas_produtivas e dias_uteis
        document.querySelector("#horas_produtivas").value = horasProdutivas;
        document.querySelector("#dias_uteis").value = diasUteis;

        // Enviar o formulário
        form.submit();
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

// Função para abrir modal personalizado Empresa
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

fetch(colaboradoresUrl)
    .then(response => response.json())
    .then(data => {
        const colaboradoresSelect = document.querySelector('select[name="funcionario"]');
        data.colaboradores.forEach(colaborador => {
            const option = document.createElement('option');
            option.value = colaborador.id;
            option.textContent = colaborador.nome;
            colaboradoresSelect.appendChild(option);
        });
    });

// Função para calcular horas produtivas do funcionario

// Cadastro OK Mão de obra, mesma função no .html trocar 
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
});