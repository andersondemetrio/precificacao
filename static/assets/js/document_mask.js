$(document).ready(function () {
    // Aplicar a máscara de CPF
    $('#cpfInput').mask('000.000.000-00');

    // Adicionar um evento blur para verificar o CPF após a entrada do usuário
    $('#cpfInput').on('blur', function () {
        var cpf = $(this).val();

        // Remover a máscara antes de verificar
        cpf = cpf.replace(/\D/g, ''); // Remove todos os caracteres não numéricos

        // Realizar a verificação apenas se o CPF não estiver vazio
        if (cpf.trim() !== '') {
            $.get('/dashboard/verificar_cpf/', { cpf: cpf }, function(data) {
                if (data.cpf_existe) {
                    console.log("Valor do CPF: " + cpf);
                    alert('CPF já existe no banco de dados. Por favor, insira um CPF diferente.');
                    $('#cpfInput').val(''); // Limpar o campo
                }
            });
        }
    });

    // aplicr para o CNPJ

      // Aplicar a máscara de CNPJ
      $('#cnpjfInput').mask('00.000.000/0000-00');

      // Adicionar um evento blur para verificar o CNPJ após a entrada do usuário
      $('#cnpjfInput').on('blur', function () {
          var cnpj = $(this).val();
  
          // Realizar a verificação apenas se o CNPJ não estiver vazio
          if (cnpj.trim() !== '') {
              $.get('/dashboard/verificar_cnpj/', { cnpj: cnpj }, function(data) {
                  if (data.cnpj_existe) {
                      console.log("Valor do CNPJ: " + cnpj);
                      alert('CNPJ já existe no banco de dados. Por favor, insira um CNPJ diferente.');
                      $('#cnpjfInput').val(''); // Limpar o campo
                  }
              });
          }
      });

      $('#emailInput').mask("A", {
        translation: {
            "A": { pattern: /[\w@\-.+]/, recursive: true }
        }
    });
// Máscara e-mail
    $('#emailInput').on('blur', function() {
        // Realizar a verificação apenas se o email não estiver vazio
        var email = $('#emailInput').val().trim();
        if (email !== '') {
            $.get('/dashboard/verificar_email/', { email: email }, function(data) {
                if (data.email_existe) {
                    console.log("passei aqui");
                    alert('O Email já existe no banco de dados. Por favor, insira um Email diferente.');
                    $('#emailInput').val(''); // Limpar o campo
                }
            });
        }
    });

//aplicação máscara Telefone    // Fim máscara e-mail
$('#telefoneInput').mask('(00)0000-0000');

// Adicionar mais máscaras aqui

// Não mexer nessa linha
});
