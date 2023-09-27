// Função para atualizar a data e hora no formato desejado
function atualizarDataHora() {
    var dataHoraElement = document.getElementById('data-hora');
    var dataHora = new Date();
    var dataFormatada = dataHora.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
    var horaFormatada = dataHora.toLocaleTimeString('pt-BR', {
        hour: '2-digit',
        minute: '2-digit'
    });
    var dataHoraFormatada = `${dataFormatada} ${horaFormatada}`;
    dataHoraElement.textContent = dataHoraFormatada;
}

document.addEventListener("DOMContentLoaded", function () {
    atualizarDataHora();
    setInterval(atualizarDataHora, 1000);
});
