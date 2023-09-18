// data-hora.js

// Função para atualizar a data e hora no formato desejado
function atualizarDataHora() {
    var dataHoraElement = document.getElementById('data-hora');
    var dataHora = new Date(); // Obtém a data e hora atual
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

// Adicione o evento DOMContentLoaded para garantir que o código seja executado no momento certo
document.addEventListener("DOMContentLoaded", function () {
    // Chame a função uma vez para exibir a data e hora imediatamente
    atualizarDataHora();

    // Agende a função para ser chamada a cada segundo
    setInterval(atualizarDataHora, 1000);
});
