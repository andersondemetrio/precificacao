// todos os códigos estão em document.js
// $(document).ready(function () {
//     $('#emailInput').mask("A", {
//         translation: {
//             "A": { pattern: /[\w@\-.+]/, recursive: true }
//         }
//     });

//     $('#emailInput').on('blur', function() {
//         // Realizar a verificação apenas se o email não estiver vazio
//         var email = $('#emailInput').val().trim();
//         if (email !== '') {
//             $.get('/dashboard/verificar_email/', { email: email }, function(data) {
//                 if (data.email_existe) {
//                     console.log("passei aqui");
//                     alert('O Email já existe no banco de dados. Por favor, insira um Email diferente.');
//                     $('#emailInput').val(''); // Limpar o campo
//                 }
//             });
//         }
//     });
// });
