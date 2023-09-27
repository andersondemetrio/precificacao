$(document).ready(function () {
    $('#matriculaInput').on('blur', function () {
        var matricula = $(this).val();

        if (matricula.trim() !== '') {
            $.get('/dashboard/verificar_matricula/', {matricula: matricula }, function(data) {
                if (data.matricula_existe) {
                    console.log("Valor da Matricula : "+ matricula)
                    alert('A matricula já existe no banco de dados. Por favor, insira um número diferente.');
                    $('#matriculaInput').val(''); 
                }
            });
        }
    });
});
