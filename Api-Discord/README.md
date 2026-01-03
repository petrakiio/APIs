# 🚀 Sistema de Delivery & Autenticação — Thrownlift

Este projeto é uma aplicação web desenvolvida com **Flask**, focada em autenticação segura, envio de pedidos e boas práticas de backend.  
O sistema gerencia cadastro, login, controle de sessão e envio de pedidos em tempo real via **Discord Webhook**.

O projeto foi desenvolvido com atenção especial à **segurança**, **organização de código** e **proteção contra abusos comuns** (spam e brute force).

---

## 🛡️ Segurança (Ponto Forte do Projeto)

Este projeto vai além do básico e implementa medidas reais de segurança:

- 🔐 **Hash de Senhas com Argon2**  
  As senhas nunca são armazenadas em texto puro. O algoritmo **Argon2** é utilizado por ser resistente a ataques de força bruta e considerado padrão moderno de segurança.

- 🔑 **Autenticação por Sessão**  
  O login é gerenciado via sessões do Flask, protegendo rotas sensíveis contra acesso não autorizado.

- 🚫 **Proteção contra Brute Force**  
  Limite de tentativas de login por IP, com bloqueio temporário após múltiplas falhas.

- 🛑 **Proteção contra Spam de Pedidos**  
  Controle de tempo mínimo entre pedidos por IP, evitando flood e abuso do sistema.

- 🔒 **Variáveis Sensíveis com `.env`**  
  Tokens e chaves privadas não ficam no código-fonte.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3 + Flask
- **Banco de Dados:** MySQL
- **Segurança:** Argon2 (hash de senhas)
- **Sessões:** Flask Sessions
- **Integração Externa:** Discord Webhooks
- **Ambiente:** python-dotenv
- **Templates:** Jinja2

---

## 📋 Funcionalidades

- ✅ Cadastro de usuários com validações no backend
- ✅ Login seguro com verificação de hash
- ✅ Controle de sessão (login / logout)
- ✅ Proteção de rotas privadas
- ✅ Sistema de pedidos aberto (não requer login)
- ✅ Envio automático de pedidos para um canal do Discord
- ✅ Navbar dinâmica baseada no estado de autenticação
- ✅ Proteções contra SQL Injection, brute force e spam

---

## ⚙️ Configuração Local

### 1️⃣ Banco de Dados (MySQL)

Estrutura da tabela de usuários:

```sql
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    data_nascimento DATE
);
