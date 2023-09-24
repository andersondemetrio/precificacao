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
        // Obtenha os valores dos campos relevantes
        const custoHora = parseFloat(document.getElementById("orcamentoCustoHora").value.replace(',', '.')) || 0;
        const beneficios = parseFloat(document.getElementById("orcamentoBeneficios").value.replace(',', '.')) || 0;
        const condominio = parseFloat(document.getElementById("orcamentoCondominio").value.replace(',', '.')) || 0;
        const outros = parseFloat(document.getElementById("orcamentoOutros").value) || 0;
        const tributos = parseFloat(document.getElementById("orcamentoImpostos").value) || 0;
        const lucro = parseFloat(document.getElementById("orcamentoLucro").value) || 0;

        // Calcule o valor total sugerido
        const totalSugerido = parseFloat(custoHora) + beneficios + condominio;
        
        // Calcule a soma do tributo e lucro
        const somaTributoLucro = outros + tributos + lucro;

        // Obtenha todos os elementos com a classe 'valorOrcNovo'
        const elementosValorOrcNovo = document.getElementsByClassName("valorOrcNovo");

        // Calcule o valor total dos campos dinâmicos
        let totalCamposDinamicos = 0;
        for (const elemento of elementosValorOrcNovo) {
            totalCamposDinamicos += parseFloat(elemento.value) || 0;
        }

        // Adicione o valor dos campos dinâmicos ao total sugerido
        const totalFinal = totalSugerido + totalCamposDinamicos;

         // Calcule o valor final dividindo o total sugerido pela diferença entre 1 e a soma do tributo e lucro
        const valorFinal = totalFinal / (1 - somaTributoLucro / 100); // Atribuí 100 pois os valores do tributo e lucro estão em porcentagem (%)

        // Exiba o valor total sugerido no elemento span
        document.getElementById("totalSugeridoDisplay").textContent = valorFinal.toFixed(2);

        // Atualize o campo de entrada "orcamentoSugerido" com o valor calculado
        document.getElementById("orcamentoSugerido").value = valorFinal.toFixed(2);
    }

    // Adicione listeners de evento para os campos relevantes para chamar a função de cálculo quando os valores forem alterados
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

         // Adicione um ouvinte de evento "input" ao novo campo dinâmico
         const novoCampoDinamico = div.querySelector(".valorOrcNovo");
         novoCampoDinamico.addEventListener("input", calcularTotalSugerido);
 
         // Adicione um ouvinte de evento ao botão "Remover Campo" para remover o campo
         const botaoRemoverCampo = div.querySelector(".removerCampo");
         botaoRemoverCampo.addEventListener("click", function () {
             inputForm.removeChild(div); // Remove o campo
             calcularTotalSugerido(); // Recalcula o total
         });

        // Recalcule o total quando um novo campo é adicionado
        calcularTotalSugerido();
    });

});

const valorSpan = document.getElementById("totalSugeridoDisplay").textContent;

// Defina o valor no input
document.getElementById("orcamentoSugerido").value = valorSpan;

