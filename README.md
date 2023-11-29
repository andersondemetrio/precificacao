## Projeto Final de Conclusão de Curso

### Criando as variaveis de ambiente (.env) na raiz do projeto:

```bash
touch .env

EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=usuario@gmail.com
EMAIL_HOST_PASSWORD=senha_usuario
DEFAULT_FROM_EMAIL=email_default.com
```

### Banco de dados
```
Roder o seguinte comando em docker
docker run --name teste -e POSTGRES_PASSWORD=teste -e POSTGRES_DB=teste -p 5432:5432 -d postgres
```

### Criando um ambiente virtual (virtual env)

```bash
# crie o env:
python -m venv venv .

# ative o ambiente no windows
venv\Scripts\activate

# faça a instalação das dependencias listadas no arquivo requirements.txt
pip  install -r requirements.txt

# Faça a migração da aplicação
python manage.py migrate

# inicie o serviço

# Imagem do código


python manage.py runserver

docker run --name teste -e POSTGRES_PASSWORD=teste -e POSTGRES_DB=teste -p 5432:5432 -d postgres
```
# Login do Sistema
![image](https://github.com/andersondemetrio/precificacao/assets/77970939/6c195095-82dd-4036-bd9d-232555a08b78)

# Colaboradores
![image](https://github.com/andersondemetrio/precificacao/assets/77970939/6d5e9251-2de1-412b-92c3-1383bfd62f23)
# Vinculo de cargos

![image](https://github.com/andersondemetrio/precificacao/assets/77970939/d768b144-804c-4643-8c49-2d548e185c3e)

#cadastro de Orçamento
![image](https://github.com/andersondemetrio/precificacao/assets/77970939/fe9a6ae3-752b-44ca-a5bb-3dcb8666fead)
![image](https://github.com/andersondemetrio/precificacao/assets/77970939/a7092dc7-aa5e-4cb3-ac33-dbe083b49d15)
![image](https://github.com/andersondemetrio/precificacao/assets/77970939/88656c6a-89c5-4854-9652-e1525b5b7d66)
![image](https://github.com/andersondemetrio/precificacao/assets/77970939/afdbffa8-8900-4861-ac89-1ecf9db5afc1)

# Relatórios
![image](https://github.com/andersondemetrio/precificacao/assets/77970939/a863a067-57ce-4bfb-a722-d32284028d3e)
![image](https://github.com/andersondemetrio/precificacao/assets/77970939/b2305102-7705-46fe-8eec-069d83ae2374)



