document.getElementById("orcamentoImpostos").addEventListener("input", function () {
    const value = parseInt(this.value);
    if (isNaN(value) || value < 1 || value > 100) {
        this.setCustomValidity("O valor deve estar entre 1 e 100.");
    } else {
        this.setCustomValidity("");
    }
});

document.getElementById("orcamentoLucro").addEventListener("input", function () {
    const value = parseInt(this.value);
    if (isNaN(value) || value < 1 || value > 100) {
        this.setCustomValidity("O valor deve estar entre 1 e 100.");
    } else {
        this.setCustomValidity("");
    }
});

function getCookie(name) {
    const cookieValue = document.cookie
        .split('; ')
        .find(cookie => cookie.startsWith(name + '='))
        .split('=')[1];
    
    return cookieValue ? decodeURIComponent(cookieValue) : null;
}

document.addEventListener("DOMContentLoaded", function () {
    // Função para calcular o valor total sugerido
    function calcularTotalSugerido() {
        const custoHora = parseFloat(document.getElementById("orcamentoCustoHora").value.replace(',', '.')) || 0;
        const beneficios = parseFloat(document.getElementById("orcamentoBeneficios").value.replace(',', '.')) || 0;
        const condominio = parseFloat(document.getElementById("orcamentoCondominio").value.replace(',', '.')) || 0;
        const outros = parseFloat(document.getElementById("orcamentoOutros").value) || 0;
        const tributos = parseFloat(document.getElementById("orcamentoImpostos").value) || 0;
        const lucro = parseFloat(document.getElementById("orcamentoLucro").value) || 0;

        var valores = document.querySelectorAll('[name^="valor_"]');
        var valoresAdicionais = 0;  // Inicializa com 0

        // Itera pelos elementos e soma seus valores convertidos para float
        valores.forEach(function(elemento) {
            valoresAdicionais += parseFloat(elemento.value) || 0;
        });

        const totalSugerido = parseFloat(custoHora) + beneficios + condominio;
        
        const somaTributoLucro = outros + tributos + lucro;

        const elementosValorOrcNovo = document.getElementsByClassName("valorOrcNovo");

        let totalCamposDinamicos = 0;
        for (const elemento of elementosValorOrcNovo) {
            totalCamposDinamicos += parseFloat(elemento.value) || 0;
        }

        const totalFinal = totalSugerido + totalCamposDinamicos + valoresAdicionais;
        const valorFinal = totalFinal / (1 - somaTributoLucro / 100); 

        document.getElementById("totalSugeridoDisplay").textContent = valorFinal.toFixed(2);
        document.getElementById("orcamentoSugerido").value = valorFinal.toFixed(2);
    }

    document.getElementById("orcamentoCustoHora").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoBeneficios").addEventListener("input", calcularTotalSugerido);;
    document.getElementById("orcamentoCondominio").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoOutros").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoImpostos").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoLucro").addEventListener("input", calcularTotalSugerido);
    const elementosValorOrcNovo = document.getElementsByClassName("valorOrcNovo");
    for (const elemento of elementosValorOrcNovo) {
        elemento.addEventListener("input", calcularTotalSugerido);
    }
    
    document.getElementById("addInput").addEventListener("click", function () {
        const inputForm = document.getElementById("inputForm");
        const div = document.createElement("div");
        div.classList.add("form-row", "d-flex", "flex-row", "justify-content-between", "align-items-center");
        div.style.gap = "10px";
        div.innerHTML = `
            <div class="form-group col-md-6">
                <label for="descricao">Descrição:</label>
                <input type="text" class="form-control" id="descricaoOrcNovo" name="descricao[]" required>
            </div>
            <div class="form-group col-md-4">
                <label for="valor">Valor:</label>
                <input type="number" class="form-control valorOrcNovo" id="valorOrcNovo" name="valor[]" required>
            </div>
            <div class="form-group col-md-2">
                <button type="button" class="btn btn-danger removerCampo div-button-remove">Remover</button>
            </div>
        `;
        inputForm.appendChild(div);

         const novoCampoDinamico = div.querySelector(".valorOrcNovo");
         novoCampoDinamico.addEventListener("input", calcularTotalSugerido);
 
         const botaoRemoverCampo = div.querySelector(".removerCampo");
         botaoRemoverCampo.addEventListener("click", function () {
             inputForm.removeChild(div); 
             calcularTotalSugerido(); 
         });

        calcularTotalSugerido();
    });

});

const valorSpan = document.getElementById("totalSugeridoDisplay").textContent;

document.getElementById("orcamentoSugerido").value = valorSpan;


function formatarNumeroComVirgula(numero) {
    return numero.toLocaleString('pt-BR', { minimumFractionDigits: 2 });
}

var camposValor = document.querySelectorAll('[name^="valor_"]');
camposValor.forEach(function(valorInput) {
    valorInput.value = formatarNumeroComVirgula(valorInput.value);
});


// Função para calcular o orçamento editado
function calcularValorSugerido() {
    var valores = document.querySelectorAll('[name^="valor_"]');
    var camposAdicionais = document.querySelectorAll('.calcular');

    var totalValorSugerido = 0;

    valores.forEach(function(valorInput) {
        var valor = parseFloat(valorInput.value.replace(',', '.')) || 0;
        totalValorSugerido += valor;
    });

    var camposAdicionais = document.querySelectorAll('.calcular');
    camposAdicionais.forEach(function(campoAdicional) {
        var valorCampo = parseFloat(campoAdicional.value.replace(',', '.')) || 0;
        totalValorSugerido += valorCampo;
    });

    document.getElementById('orcamentoSugerido').value = totalValorSugerido.toFixed(2);
}

var camposValor = document.querySelectorAll('[name^="valor_"]');
camposValor.forEach(function(valorInput) {
    valorInput.addEventListener('input', calcularValorSugerido);
});

var camposAdicionais = document.querySelectorAll('.calcular');
camposAdicionais.forEach(function(campoAdicional) {
    campoAdicional.addEventListener('input', calcularValorSugerido);
});

calcularValorSugerido();