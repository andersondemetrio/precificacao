// Busca dinâmica de dados nas tabelas Colaboradores
document.addEventListener("DOMContentLoaded", function () {
    const searchFormColaboradores = document.getElementById("searchFormColaboradores");
    const modal = document.getElementById("myModal");

    searchFormColaboradores.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(searchFormColaboradores);

        fetch(searchFormColaboradores.action + '?' + new URLSearchParams(formData), {
            method: 'GET'
        })
            .then(response => response.text())
            .then(data => {
                const searchResultsTableColaboradores = document.getElementById("searchResultsTableColaboradores");
                searchResultsTableColaboradores.innerHTML = data; // Atualiza a tabela de resultados
            })
            .catch(error => {
                console.error('Erro na busca:', error);
            });
    });
});

// Busca dinâmica de dados nas tabelas Cargos
document.addEventListener("DOMContentLoaded", function () {
    const searchFormCargo = document.getElementById("searchFormCargo");
    const modal = document.getElementById("myModal");

    // modal.addEventListener("click", function (event) {
    //     if (event.target === modal) {
    //         event.preventDefault();
    //         event.stopPropagation();
    //     }
    // });

    searchFormCargo.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(searchFormCargo);

        fetch(searchFormCargo.action + '?' + new URLSearchParams(formData), {
            method: 'GET'
        })
            .then(response => response.text())
            .then(data => {
                const searchResultsTable = document.getElementById("searchResultsTable");
                searchResultsTable.innerHTML = data; // Atualiza a tabela de resultados
            })
            .catch(error => {
                console.error('Erro na busca:', error);
            });
    });
});

// Busca dinâmica de dados nas tabelas Endereços
document.addEventListener("DOMContentLoaded", function () {
    const searchFormEndereco = document.getElementById("searchFormEndereco");
    const modal = document.getElementById("myModal");

    searchFormEndereco.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(searchFormEndereco);

        fetch(searchFormEndereco.action + '?' + new URLSearchParams(formData), {
            method: 'GET'
        })
            .then(response => response.text())
            .then(data => {
                const searchResultsTableEndereco = document.getElementById("searchResultsTableEndereco");
                searchResultsTableEndereco.innerHTML = data; // Atualiza a tabela de resultados
            })
            .catch(error => {
                console.error('Erro na busca:', error);
            });
    });
});