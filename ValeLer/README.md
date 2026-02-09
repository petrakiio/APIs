# 📚 ValeLer

> Sistema de biblioteca inteligente com controle de estoque, perfis de usuário e gestão de empréstimos.

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
* [x] Listagem dinâmica de livros.
* [x] Gestão de usuários (Admin e Cliente) com fotos de perfil.
* [x] Registro de empréstimos com atualização automática de estoque.
* [x] Sistema de Feedback e Devoluções.

## 📂 Estrutura do Projeto
```text
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
│  ├─ perfil.html
│  ├─ feedback.html
│  └─ ...
└─ static/
   ├─ style.css
   └─ script/