# ValeLer

Sistema simples de biblioteca com cadastro de livros e controle de empréstimos.

## Stack

- Flask
- MySQL
- POO

## Funcionalidades

- Listagem de livros cadastrados.
- Cadastro de novos livros.
- Registro de empréstimos e atualização automática das unidades disponíveis.

## Estrutura do Projeto

```
ValeLer/
├─ app.py
├─ connection/
│  └─ conn.py
├─ models/
│  ├─ administração.py
│  └─ emprestimos.py
├─ routes/
│  ├─ admin_routes.py
│  └─ home_routes.py
├─ templates/
│  ├─ index.html
│  ├─ adicionar_livros.html
│  ├─ emprestar_livros.html
│  └─ deletar.html
└─ static/
   ├─ style.css
   ├─ add_livros.css
   ├─ emprestar.css
   └─ deletar.css
```

## Configuração

Crie um arquivo `.env` com as variáveis de conexão:

```
DB_HOST=localhost
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=seu_banco
DB_PORT=3306
```

## Rotas Principais

- `GET /` ou `/index` - lista livros e empréstimos.
- `GET /add_livros` - formulário de cadastro de livros.
- `POST /add_livros_form` - envia cadastro de livro.
- `GET /emprestimo` - formulário de empréstimo.
- `POST /emprestimo_method` - registra empréstimo.
- `GET /deletar` - tela de remoção de livros (rota de `POST` ainda não implementada).

## Observações

- A tabela usada para livros é `livros`.
- A tabela de empréstimos é `emprestado`.
- Existe um botão de devolução no template, mas a rota `/devolver` ainda não foi criada.

## Como Rodar

```
python app.py
```

O app sobe em `http://localhost:5000`.
