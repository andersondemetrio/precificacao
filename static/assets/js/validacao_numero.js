$(document).ready(function () {
   
    // Adicionar um evento blur para verificar o numero após a entrada do usuário
    $('#numeroInput').on('blur', function () {
        var numero_empresa = $(this).val();

        // Realizar a verificação apenas se o numero não estiver vazio
        if (numero_empresa.trim() !== '') {
            $.get('/dashboard/verificar_numero/', {numero_empresa: numero_empresa }, function(data) {
                if (data.numero_existe) {
                    console.log("Valor do Numero : "+ numero_empresa)
                    alert('O numero já existe no banco de dados. Por favor, insira um número diferente.');
                    $('#numeroInput').val(''); // Limpar o campo
                }
            });
        }
    });
});





