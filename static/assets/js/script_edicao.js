document.addEventListener('DOMContentLoaded', function () {
    //Confirma edição de cargos
    document.getElementById('alterar-btnca').addEventListener('click', function () {
        document.getElementById('editar-form-cargo').submit();
    });



    //Confirma edição de colaborador
    document.getElementById('alterar-btnco').addEventListener('click', function () {
        document.getElementById('editar-form-colaborador').submit();
    });



    //Confirma edição de endereço
    document.getElementById('alterar-btnen').addEventListener('click', function () {
        document.getElementById('editar-form-endereco').submit();
    });



    //Confirma edição de empresa
    document.getElementById('alterar-btnem').addEventListener('click', function () {
        document.getElementById('editar-form-empresa').submit();
    });


    //Confirma edição de calendário
    document.getElementById('alterar-btncal').addEventListener('click', function () {
        document.getElementById('editar-form-calendario').submit();
    });



    //Confirma edição de Gasto Fixo
    document.getElementById('alterar-btncal').addEventListener('click', function () {
        document.getElementById('editar-form-gasto-fixo').submit();
    });

    document.addEventListener("DOMContentLoaded", function () {
        const form = document.getElementById("novo-form-orcamento");
    
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            window.location.href = "/dashboard/";
        });
    });
});