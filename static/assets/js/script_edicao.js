document.addEventListener('DOMContentLoaded', function () {
    //Confirma edição de cargos
    document.getElementById('alterar-btnca').addEventListener('click', function () {
        document.getElementById('editar-form-cargo').submit();
    });
});

document.addEventListener('DOMContentLoaded', function () {
    //Confirma edição de colaborador
    document.getElementById('alterar-btnco').addEventListener('click', function () {
        document.getElementById('editar-form-colaborador').submit();
    });
});

document.addEventListener('DOMContentLoaded', function () {
    //Confirma edição de endereço
    document.getElementById('alterar-btnen').addEventListener('click', function () {
        document.getElementById('editar-form-endereco').submit();
    });
});