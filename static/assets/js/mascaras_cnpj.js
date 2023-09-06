$(document).ready(function () {
    // Aplicar a máscara de CNPJ
    $('#cnpjfInput').mask('00.000.000/0000-00');

    // Adicionar um evento blur para verificar o CNPJ após a entrada do usuário
    $('#cnpjfInput').on('blur', function () {
        var cnpj = $(this).val();

        // Realizar a verificação apenas se o CNPJ não estiver vazio
        if (cnpj.trim() !== '') {
            $.get('/dashboard/calcular_gasto_fixo/', { cnpj: cnpj }, function(data) {
                if (data.cnpj_existe) {
                    console.log("Valor do CNPJ: " + cnpj);
                    alert('CNPJ já existe no banco de dados. Por favor, insira um CNPJ diferente.');
                    $('#cnpjfInput').val(''); // Limpar o campo
                }
            });
        }
    });
});

