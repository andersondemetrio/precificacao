function validarFormulario() {
    var usuario = document.getElementById("usuario").value;
    var senha = document.getElementById("senha").value;

    if (usuario === "" || senha === "") {
        alert("Por favor, preencha todos os campos!");
        return false;
    }

    return true; 
}

// Esconder ou revelar senha da tela de login

document.addEventListener("DOMContentLoaded", function () {
    var togglePassword = document.getElementById("toggle-password");
    var passwordField = document.getElementById("password");

    togglePassword.addEventListener("click", function () {
        if (passwordField.type === "password") {
            passwordField.type = "text";
            togglePassword.classList.remove("fa-eye-slash");
            togglePassword.classList.add("fa-eye");
        } else {
            passwordField.type = "password";
            togglePassword.classList.remove("fa-eye");
            togglePassword.classList.add("fa-eye-slash");
        }
    });
});

// Verificar erros na redefinição de senhas
document.addEventListener('DOMContentLoaded', function() {
    const password1Input = document.querySelector('#id_new_password1');
    const password2Input = document.querySelector('#id_new_password2');
    const password1Error = document.querySelector('#password1Error');
    const password2Error = document.querySelector('#password2Error');

    if (password1Input) {
        password1Input.addEventListener('input', () => {
            const password = password1Input.value;

            if (password.length < 8) {
                password1Error.textContent = 'A senha deve ter pelo menos 8 caracteres.';
            } else if (!/\d/.test(password) || !/[a-zA-Z]/.test(password)) {
                password1Error.textContent = 'A senha deve conter letras e números.';
            } else {
                password1Error.textContent = '';
            }
        });
    }

    if (password2Input) {
        password2Input.addEventListener('input', () => {
            if (password2Input.value !== password1Input.value) {
                password2Error.textContent = 'As senhas não coincidem.';
            } else {
                password2Error.textContent = '';
            }
        });
    }
});


