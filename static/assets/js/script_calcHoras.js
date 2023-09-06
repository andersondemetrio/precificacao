$(document).ready(function() {
    $('#calcularGastosBtn').click(function(event) {
        event.preventDefault();  // Evita que o link seja seguido

        var url = $(this).data('url'); // Obtém a URL completa do atributo data-url

        $.ajax({
            url: url,
            type: 'GET',
            success: function(data) {
                // Atualize o valor diretamente no HTML
                $('#total_gastos_12_meses').text(data.total_gastos_12_meses);
            },
            error: function(error) {
                console.error(error);
            }
        });
    });
});