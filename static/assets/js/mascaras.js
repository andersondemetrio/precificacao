$(document).ready(function () {
    // Aplicar a máscara de CPF
    $('#cpfInput').mask('000.000.000-00');

    // Adicionar um evento blur para verificar o CPF após a entrada do usuário
    $('#cpfInput').on('blur', function () {
        var cpf = $(this).val();

        // Realizar a verificação apenas se o CPF não estiver vazio
        if (cpf.trim() !== '') {
            $.get('/dashboard/verificar_cpf/', { cpf: cpf }, function(data) {
                if (data.cpf_existe) {
                    console.log("Valor do CPF: "+cpf)
                    alert('CPF já existe no banco de dados. Por favor, insira um CPF diferente.');
                    $('#cpfInput').val(''); // Limpar o campo
                }
            });
        }
    });
});
