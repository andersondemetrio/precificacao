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

document.addEventListener("DOMContentLoaded", function () {
    // Função para calcular o valor total sugerido
    function calcularTotalSugerido() {
        // Obtenha os valores dos campos relevantes
        const compraMateriais = parseFloat(document.getElementById("orcamentoCompraMateriais").value) || 0;
        const materiaisDvs = parseFloat(document.getElementById("orcamentoMateriaisDvs").value) || 0;
        const dvsSocios = parseFloat(document.getElementById("orcamentoDvsSocios").value) || 0;
        const custoHora = parseFloat(document.getElementById("orcamentoCustoHora").value.replace(',', '.')) || 0;
        const beneficios = parseFloat(document.getElementById("orcamentoBeneficios").value.replace(',', '.')) || 0;
        const telefonia = parseFloat(document.getElementById("orcamentoTelefonia").value) || 0;
        const segEquipamento = parseFloat(document.getElementById("orcamentoSeguroEquipamentos").value) || 0;
        const manutencao = parseFloat(document.getElementById("orcamentoManutencao").value) || 0;
        const dvsOperacao = parseFloat(document.getElementById("orcamentoDvsOperacao").value) || 0;
        const bonusResultado = parseFloat(document.getElementById("orcamentoBonus").value) || 0;
        const plr = parseFloat(document.getElementById("orcamentoPlr").value) || 0;
        const horasExtras = parseFloat(document.getElementById("orcamentoHorasExtras").value) || 0;
        const exame = parseFloat(document.getElementById("orcamentoExame").value) || 0;
        const terceirizados = parseFloat(document.getElementById("orcamentoTerceirizados").value) || 0;
        const alimentacao = parseFloat(document.getElementById("orcamentoAlimentacao").value) || 0;
        const hospedagem = parseFloat(document.getElementById("orcamentoHospedagem").value) || 0;
        const quilometragem = parseFloat(document.getElementById("orcamentoQuilometragem").value) || 0;
        const deslocamento = parseFloat(document.getElementById("orcamentoDeslocamento").value) || 0;
        const combustivel = parseFloat(document.getElementById("orcamentoCombustivel").value) || 0;
        const estacionamento = parseFloat(document.getElementById("orcamentoEstacionamento").value) || 0;
        const comissoes = parseFloat(document.getElementById("orcamentoComissoes").value) || 0;
        const segObra = parseFloat(document.getElementById("orcamentoSeguroObra").value) || 0;
        const insumos = parseFloat(document.getElementById("orcamentoInsumos").value) || 0;
        const manutencaoECons = parseFloat(document.getElementById("orcamentoManutencaoECons").value) || 0;
        const distrato = parseFloat(document.getElementById("orcamentoDistrato").value) || 0;
        const condominio = parseFloat(document.getElementById("orcamentoCondominio").value.replace(',', '.')) || 0;
        const tributos = parseFloat(document.getElementById("orcamentoImpostos").value) || 0;
        const lucro = parseFloat(document.getElementById("orcamentoLucro").value) || 0;

        // Calcule o valor total sugerido
        const totalSugerido = compraMateriais + materiaisDvs + dvsSocios +  parseFloat(custoHora) + beneficios +
            telefonia + segEquipamento + manutencao + dvsOperacao + bonusResultado + plr + horasExtras +
            exame + terceirizados + alimentacao + hospedagem + quilometragem + deslocamento + combustivel +
            estacionamento + comissoes + segObra + insumos + manutencaoECons + distrato + condominio;
        
        // Calcule a soma do tributo e lucro
        const somaTributoLucro = tributos + lucro;

         // Calcule o valor final dividindo o total sugerido pela diferença entre 1 e a soma do tributo e lucro
        const valorFinal = totalSugerido / (1 - somaTributoLucro / 100); // Atribuí 100 pois os valores do tributo e lucro estão em porcentagem (%)

        // Exiba o valor total sugerido no elemento span
        document.getElementById("totalSugeridoDisplay").textContent = valorFinal.toFixed(2);

        // Atualize o campo de entrada "orcamentoSugerido" com o valor calculado
        document.getElementById("orcamentoSugerido").value = valorFinal.toFixed(2);
    }

    // Adicione listeners de evento para os campos relevantes para chamar a função de cálculo quando os valores forem alterados
    document.getElementById("orcamentoCompraMateriais").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoMateriaisDvs").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoDvsSocios").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoCustoHora").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoBeneficios").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoTelefonia").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoSeguroEquipamentos").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoManutencao").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoDvsOperacao").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoBonus").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoPlr").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoHorasExtras").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoExame").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoTerceirizados").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoAlimentacao").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoHospedagem").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoQuilometragem").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoDeslocamento").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoCombustivel").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoEstacionamento").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoComissoes").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoSeguroObra").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoInsumos").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoManutencaoECons").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoDistrato").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoCondominio").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoImpostos").addEventListener("input", calcularTotalSugerido);
    document.getElementById("orcamentoLucro").addEventListener("input", calcularTotalSugerido);
    // document.getElementById("orcamentoSugerido").addEventListener("input", calcularTotalSugerido);
    // Adicione outros campos relevantes aqui

    // Pegue o valor do span

    // var valorSugerido = 0;
    // document.getElementById("orcamentoSugerido").value = valorSugerido;

    // // Em seguida, envie o formulário
    // document.getElementById("novo-form-orcamento").submit();

});

const valorSpan = document.getElementById("totalSugeridoDisplay").textContent;

// Defina o valor no input
document.getElementById("orcamentoSugerido").value = valorSpan;