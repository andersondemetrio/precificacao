// Função para formatar o valor
function formatarValores() {
    var elementos = document.getElementsByClassName("formatarValor");

    for (var i = 0; i < elementos.length; i++) {
        var valorElement = elementos[i];
        var valorAtual = valorElement.textContent;
        var numero = parseFloat(valorAtual.replace(",", "."));
        var valorFormatado = "R$ " + numero.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

        valorElement.textContent = valorFormatado;
    }
}

window.onload = function() {
    formatarValores();
};