# 📚 ValeLer

> Sistema simples de biblioteca com cadastro de livros e controle de empréstimos.

<p align="left">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
</p>

---

## 🚀 Stack
* **Framework:** Flask
* **Banco de Dados:** MySQL
* **Arquitetura:** Programação Orientada a Objetos (POO)

## ✨ Funcionalidades
* [x] Listagem de livros cadastrados.
* [x] Cadastro de novos livros.
* [x] Registro de empréstimos com atualização automática de estoque.

## 📂 Estrutura do Projeto
```text
ValeLer/
├─ app.py
├─ connection/
│  └─ conn.py
├─ models/
│  ├─ administração.py
│  └─ emprestimos.py
├─ routes/
│  ├─ admin_routes.py
│  └─ home_routes.py
├─ templates/
│  ├─ index.html
│  ├─ adicionar_livros.html
│  ├─ emprestar_livros.html
│  └─ deletar.html
└─ static/
   ├─ style.css
   ├─ add_livros.css
   ├─ emprestar.css
   └─ deletar.css
