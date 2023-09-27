// Validação do CPF, CNPJ e EMAIL
$(document).ready(function () {
    $('#cpfInput').mask('000.000.000-00');

    $('#cpfInput').on('blur', function () {
        var cpf = $(this).val();

        cpf = cpf.replace(/\D/g, ''); 

        if (cpf.trim() !== '') {
            $.get('/dashboard/verificar_cpf/', { cpf: cpf }, function(data) {
                if (data.cpf_existe) {
                    console.log("Valor do CPF: " + cpf);
                    alert('CPF já existe no banco de dados. Por favor, insira um CPF diferente.');
                    $('#cpfInput').val(''); 
                }
            });
        }
    });

    $('#cnpjfInput').mask('00.000.000/0000-00');

    $('#cnpjfInput').on('blur', function () {
        var cnpj = $(this).val();

        if (cnpj.trim() !== '') {
            $.get('/dashboard/verificar_cnpj/', { cnpj: cnpj }, function(data) {
                if (data.cnpj_existe) {
                    console.log("Valor do CNPJ: " + cnpj);
                    alert('CNPJ já existe no banco de dados. Por favor, insira um CNPJ diferente.');
                    $('#cnpjfInput').val('');
                }
            });
        }
    });

    $('#emailInput').mask("A", {
        translation: {
            "A": { pattern: /[\w@\-.+]/, recursive: true }
        }
    });

    $('#emailInput').on('blur', function() {
        var email = $('#emailInput').val().trim();
        if (email !== '') {
            $.get('/dashboard/verificar_email/', { email: email }, function(data) {
                if (data.email_existe) {
                    console.log("passei aqui");
                    alert('O Email já existe no banco de dados. Por favor, insira um Email diferente.');
                    $('#emailInput').val(''); 
                }
            });
        }
    });


$('#telefoneInput').mask('(00)0000-0000');

});
