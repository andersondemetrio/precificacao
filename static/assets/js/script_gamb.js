document.addEventListener('DOMContentLoaded', function () {

    // Requisição Fetch para cargos
    fetch(cargosUrl)
        .then(response => response.json())
        .then(data => {
            const selectElement = document.querySelector('select[name="cargos"]');
            data.cargos.forEach(cargo => {
                const option = document.createElement('option');
                option.value = cargo.id;
                option.textContent = cargo.nome_cargo;
                selectElement.appendChild(option);
            });
        });
    });