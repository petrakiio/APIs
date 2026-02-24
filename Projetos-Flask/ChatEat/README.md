<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Security-Shield-green?style=for-the-badge" alt="Security">
</div>

<h1 align="center">🚀 Thrownlift - Delivery & Auth System</h1>

<p align="center">
  <strong>Sistema de autenticação robusto e gestão de pedidos com foco em segurança cibernética e boas práticas de Back-end.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/github/last-commit/petrakiio/NOME_DO_REPOSITORIO?style=flat-square" alt="Last Commit">
  <img src="https://img.shields.io/badge/Auth-Argon2-blue?style=flat-square" alt="Argon2">
  <img src="https://img.shields.io/badge/Proteções-Brute_Force_%7C_Spam-red?style=flat-square" alt="Protections">
</p>

---

### 🛡️ O Diferencial: Foco em Segurança
Diferente de sistemas simples, o **Thrownlift** foi projetado para mitigar ataques comuns e proteger os dados dos usuários:

* **Argon2 Hashing:** Utilização do algoritmo vencedor da *Password Hashing Competition* para garantir que senhas nunca sejam expostas.
* **Rate Limiting:** Proteção ativa contra **Brute Force** (limite de tentativas de login) e **Spam** de pedidos por IP.
* **Gestão de Sessão Segura:** Controle rigoroso de rotas privadas e persistência de login via Flask Sessions.
* **Segurança de Dados:** Uso de variáveis de ambiente (`.env`) e proteção contra SQL Injection.

---

### 🛠️ Stack Tecnológica
* **Core:** Python 3 & Flask.
* **Database:** MySQL (Relacional).
* **Template Engine:** Jinja2 (Renderização dinâmica de Front-end).
* **Webhooks:** Integração com Discord para notificações de pedidos em tempo real.

### 📋 Funcionalidades Principais
- [x] **Auth System:** Cadastro e Login com validações complexas no servidor.
- [x] **Dynamic UI:** Navbar que se adapta automaticamente se o usuário está logado ou não.
- [x] **Order Management:** Sistema de envio de pedidos integrado ao Banco de Dados.
- [x] **Private Routes:** Bloqueio de acesso a páginas restritas para usuários não autenticados.

---

### ⚙️ Configuração e Instalação

#### 1. Banco de Dados (MySQL)
```sql
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    data_nascimento DATE
);
