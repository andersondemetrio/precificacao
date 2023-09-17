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

// Busca dinâmica de dados nas Tabelas Empresa
document.addEventListener("DOMContentLoaded", function () {
    const searchFormEmpresa = document.getElementById("searchFormEmpresa");
    const modal = document.getElementById("myModal");

    searchFormEmpresa.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(searchFormEmpresa);

        fetch(searchFormEmpresa.action + '?' + new URLSearchParams(formData), {
            method: 'GET'
        })
            .then(response => response.text())
            .then(data => {
                const searchResultsTableEmpresa = document.getElementById("searchResultsTableEmpresa");
                searchResultsTableEmpresa.innerHTML = data; // Atualiza a tabela de resultados
            })
            .catch(error => {
                console.error('Erro na busca:', error);
            });
    });
});

// Busca dinâmica de dados nas tabelas Calendário
document.addEventListener("DOMContentLoaded", function () {
    const searchFormCalendario = document.getElementById("searchFormCalendario");
    const modal = document.getElementById("myModal");

    searchFormCalendario.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(searchFormCalendario);

        fetch(searchFormCalendario.action + '?' + new URLSearchParams(formData), {
            method: 'GET'
        })
            .then(response => response.text())
            .then(data => {
                const searchResultsTableCalendario = document.getElementById("searchResultsTableCalendario");
                searchResultsTableCalendario.innerHTML = data; // Atualiza a tabela de resultados
            })
            .catch(error => {
                console.error('Erro na busca:', error);
            });
    });
});

// Busca dinâmica de dados nas tabelas Gasto Fixo Condomínio
document.addEventListener("DOMContentLoaded", function () {
    const searchFormCondominio = document.getElementById("searchFormCondominio");
    const modal = document.getElementById("myModal");

    searchFormCondominio.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(searchFormCondominio);

        fetch(searchFormCondominio.action + '?' + new URLSearchParams(formData), {
            method: 'GET'
        })
            .then(response => response.text())
            .then(data => {
                const searchResultsTableCondominio = document.getElementById("searchResultsTableCondominio");
                searchResultsTableCondominio.innerHTML = data; // Atualiza a tabela de resultados
            })
            .catch(error => {
                console.error('Erro na busca:', error);
            });
    });
});

// Busca dinâmica de dados nas tabelas Gasto Fixo Condomínio
document.addEventListener("DOMContentLoaded", function () {
    const searchFormEncargos = document.getElementById("searchFormEncargos");
    const modal = document.getElementById("myModal");

    searchFormEncargos.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(searchFormEncargos);

        fetch(searchFormEncargos.action + '?' + new URLSearchParams(formData), {
            method: 'GET'
        })
            .then(response => response.text())
            .then(data => {
                const searchResultsTableEncargos = document.getElementById("searchResultsTableEncargos");
                searchResultsTableEncargos.innerHTML = data; // Atualiza a tabela de resultados
            })
            .catch(error => {
                console.error('Erro na busca:', error);
            });
    });
});

// Busca dinâmica de dados na tabela Benefícios
document.addEventListener("DOMContentLoaded", function () {
    const searchFormBeneficios = document.getElementById("searchFormBeneficios");
    const modal = document.getElementById("myModal");

    searchFormBeneficios.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(searchFormBeneficios);

        fetch(searchFormBeneficios.action + '?' + new URLSearchParams(formData), {
            method: 'GET'
        })
            .then(response => response.text())
            .then(data => {
                const searchResultsTableBeneficios = document.getElementById("searchResultsTableBeneficios");
                searchResultsTableBeneficios.innerHTML = data; // Atualiza a tabela de resultados
            })
            .catch(error => {
                console.error('Erro na busca:', error);
            });
    });
});

// Busca dinâmica de dados na tabela Benefícios
document.addEventListener("DOMContentLoaded", function () {
    const searchFormVincularCargos = document.getElementById("searchFormVincularCargos");
    const modal = document.getElementById("myModal");

    searchFormVincularCargos.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(searchFormVincularCargos);

        fetch(searchFormVincularCargos.action + '?' + new URLSearchParams(formData), {
            method: 'GET'
        })
            .then(response => response.text())
            .then(data => {
                const searchResultsTableVincularCargos = document.getElementById("searchResultsTableVincularCargos");
                searchResultsTableVincularCargos.innerHTML = data; // Atualiza a tabela de resultados
                console.log(data);
            })
            .catch(error => {
                console.error('Erro na busca:', error);
            });
    });
});

// Busca dinâmica de dados na tabela Rubricas
document.addEventListener("DOMContentLoaded", function () {
    const searchFormOrcamento = document.getElementById("searchFormOrcamento");
    const modal = document.getElementById("myModal");

    searchFormOrcamento.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(searchFormOrcamento);

        fetch(searchFormOrcamento.action + '?' + new URLSearchParams(formData), {
            method: 'GET'
        })
            .then(response => response.text())
            .then(data => {
                const searchResultsTableOrcamento = document.getElementById("searchResultsTableOrcamento");
                searchResultsTableOrcamento.innerHTML = data; // Atualiza a tabela de resultados
            })
            .catch(error => {
                console.error('Erro na busca:', error);
            });
    });
});
// lista os encargos 

document.addEventListener("DOMContentLoaded", function () {
    const searchFormEncargosRelatorios = document.getElementById("searchFormEncargosRelatorios");

    searchFormEncargosRelatorios.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(searchFormEncargosRelatorios);

        fetch(searchFormEncargosRelatorios.action + '?' + new URLSearchParams(formData), {
            method: 'GET'
        })
        .then(response => response.text())
        .then(data => {
            const searchResultsTableEncargosRelatorios = document.getElementById("searchResultsTableEncargosRelatorios");
            searchResultsTableEncargosRelatorios.innerHTML = data; // Atualiza a tabela de resultados
        })
        .catch(error => {
            console.error('Erro na busca:', error);
        });
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const searchFormEncargosRelatorios = document.getElementById("searchFormEncargosRelatorios");

    searchFormEncargosRelatorios.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(searchFormEncargosRelatorios);

        fetch(searchFormEncargosRelatorios.action + '?' + new URLSearchParams(formData), {
            method: 'GET'
        })
        .then(response => response.text())
        .then(data => {
            const searchResultsTableEncargosRelatorios = document.getElementById("searchResultsTableEncargosRelatorios");
            searchResultsTableEncargosRelatorios.innerHTML = data; // Atualiza a tabela de resultados
        })
        .catch(error => {
            console.error('Erro na busca:', error);
        });
    });
});