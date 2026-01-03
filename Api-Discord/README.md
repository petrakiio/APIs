# 🚀 APIs & Sistema de Delivery - Thrownlift

Este projeto é uma aplicação web robusta desenvolvida com **Flask**, focada na integração entre sistemas de banco de dados e comunicação em tempo real. O sistema gerencia o fluxo completo desde o cadastro de utilizadores até a notificação de pedidos via **Discord**.

## 🛡️ Segurança de Dados (Destaque)
A segurança é o pilar deste projeto. Diferente de sistemas básicos, aqui utilizamos:
* **Bcrypt:** Para o hashing de senhas. Cada senha é protegida com um *salt* único e um fator de custo computacional, tornando-a resistente a ataques de força bruta e *rainbow tables*.
* **Sessões Seguras:** Gestão de login via Flask-Session para manter a persistência do utilizador de forma segura.

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3 + Flask
* **Segurança:** Bcrypt (Criptografia)
* **Banco de Dados:** MySQL
* **Integração:** Discord Webhooks (API Requests)
* **Ambiente:** Python-dotenv (Gestão de chaves sensíveis)

## 📋 Funcionalidades

* ✅ **Cadastro Inteligente:** Validação de e-mail único e armazenamento de senha criptografada.
* ✅ **Login por E-mail:** Autenticação moderna e segura.
* ✅ **Fluxo de Pedidos:** Sistema de formulário que dispara dados estruturados para um canal do Discord.
* ✅ **Interface Dinâmica:** Navbar que se adapta se o utilizador está logado ou não, utilizando Jinja2.

## ⚙️ Configuração Local

### 1. Preparar o Banco de Dados (MySQL)
Certifique-se de que a coluna de senha suporta o hash do Bcrypt:
```sql
CREATE TABLE clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario VARCHAR(50) NOT NULL,
    senha VARCHAR(255) NOT NULL, -- Tamanho ideal para Bcrypt
    email VARCHAR(100) UNIQUE NOT NULL,
    data_nascimento DATE
);