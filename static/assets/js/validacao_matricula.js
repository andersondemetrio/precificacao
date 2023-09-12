$(document).ready(function () {
   
    // Adicionar um evento blur para verificar o numero após a entrada do usuário
    $('#matriculaInput').on('blur', function () {
        var matricula = $(this).val();

        // Realizar a verificação apenas se a matricula não estiver vazio
        if (matricula.trim() !== '') {
            $.get('/dashboard/verificar_matricula/', {matricula: matricula }, function(data) {
                if (data.matricula_existe) {
                    console.log("Valor da Matricula : "+ matricula)
                    alert('A matricula já existe no banco de dados. Por favor, insira um número diferente.');
                    $('#matriculaInput').val(''); // Limpar o campo
                }
            });
        }
    });
});
