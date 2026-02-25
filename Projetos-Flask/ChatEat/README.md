<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Pagamentos-Mercado_Pago-00B1EA?style=for-the-badge" alt="Mercado Pago">
</div>

<h1 align="center">ChatEat - Delivery, Auth, Admin e Pagamentos</h1>

<p align="center">
  <strong>Aplicação Flask com autenticação, catálogo de produtos, carrinho, painel administrativo, gestão de entregadores e integração de pagamento.</strong>
</p>

---

## Visão geral
O `ChatEat` é um projeto web full-stack (back-end + templates) focado em:

- autenticação de usuários com hash de senha;
- catálogo e busca de produtos;
- carrinho e fluxo de compra;
- painel de administração de usuários/produtos/feedbacks;
- gestão de entregadores;
- integração com gateway de pagamento e webhook.

---

## Funcionalidades atuais do projeto

### Usuário
- [x] Cadastro com validações de dados e idade mínima.
- [x] Login com sessão Flask e controle de perfil (`session`).
- [x] Recuperação de senha por e-mail (fluxo interno no sistema).
- [x] Atualização de imagem de perfil por URL.
- [x] Exclusão da própria conta.

### Catálogo e compra
- [x] Listagem de produtos na home.
- [x] Busca por nome/descrição.
- [x] Página de detalhe/compra por produto.
- [x] Adição e remoção de itens do carrinho.
- [x] Fluxo de pagamento via gateway + páginas de status (sucesso/falha/pendente).
- [x] Simulação de pagamento direto ao entregador com página de rota.

### Admin
- [x] Rotas protegidas por `admin_required`.
- [x] Gestão de produtos (criar, editar, remover).
- [x] Gestão de usuários (listar, deletar, promover/rebaixar admin).
- [x] Moderação de feedbacks.

### Entregadores
- [x] Painel de entregador (`entregador_required`).
- [x] CRUD parcial de entregadores pelo admin (adicionar, visualizar, remover).
- [x] Registro de motivo ao remover entregador.

### Segurança e boas práticas
- [x] Senhas com Argon2 (`argon2-cffi`).
- [x] Consultas SQL parametrizadas (reduz risco de SQL Injection).
- [x] Proteção de rotas privadas com decorators.
- [x] Configuração sensível via variáveis de ambiente (`.env`).
- [x] Estrutura de limitação por IP para login existe em `routes/tools.py` (parcialmente integrada).

---

## Stack
- Python 3
- Flask
- Jinja2
- MySQL + PyMySQL
- Argon2
- Mercado Pago (checkout e webhook)
- qrcode[pil]

---

## Estrutura principal

```text
ChatEat/
  app.py
  requirements.txt
  controllers/
  routes/
  models/
  connection/
  templates/
  static/
```

---

## Tutorial: como rodar o projeto

## 1) Pré-requisitos
- Python 3.10+ instalado
- MySQL 8+ rodando
- `pip` atualizado

## 2) Entrar na pasta do projeto
```bash
cd ChatEat
```

## 3) Criar e ativar ambiente virtual
Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 4) Instalar dependências
```bash
pip install -r requirements.txt
```

Observação: o código usa `import mercadopago`. Se o pacote não vier no seu ambiente, instale também:
```bash
pip install mercadopago
```

## 5) Criar banco e tabelas
No MySQL, execute:

```sql
CREATE DATABASE IF NOT EXISTS chateat CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE chateat;

CREATE TABLE IF NOT EXISTS clientes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario VARCHAR(50) NOT NULL UNIQUE,
  senha TEXT NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  data_nascimento DATE,
  foto_perfil TEXT DEFAULT 'https://i.ibb.co/4pDNDk1/avatar.png',
  is_admin TINYINT(1) DEFAULT 0,
  is_motoboy TINYINT(1) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  descricao TEXT,
  preco DECIMAL(10,2) NOT NULL,
  img TEXT
);

CREATE TABLE IF NOT EXISTS carrinho (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT NOT NULL,
  produto_id INT NOT NULL,
  quantidade INT NOT NULL DEFAULT 1,
  FOREIGN KEY (usuario_id) REFERENCES clientes(id) ON DELETE CASCADE,
  FOREIGN KEY (produto_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS feedback (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT NOT NULL,
  comentario TEXT NOT NULL,
  nota INT NOT NULL,
  FOREIGN KEY (usuario_id) REFERENCES clientes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS entregadores (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  usuario VARCHAR(80) NOT NULL,
  email VARCHAR(120),
  telefone VARCHAR(30),
  veiculo VARCHAR(50),
  placa VARCHAR(20),
  ativo TINYINT(1) DEFAULT 1
);

CREATE TABLE IF NOT EXISTS registro (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  motivo VARCHAR(120) NOT NULL,
  observacao TEXT,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 6) Criar arquivo `.env`
Crie `ChatEat/.env` com:

```env
SECRET_KEY=sua_chave_secreta_aqui

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_mysql
DB_NAME=chateat
DB_PORT=3306

ACESS_TOKEN=seu_access_token_mercadopago
MERCADOPAGO_WEBHOOK_URL=
APP_BASE_URL=http://localhost:5000
```

Notas:
- O nome da variável está como `ACESS_TOKEN` no código (sem o segundo "C").
- Se não for usar webhook por enquanto, pode deixar `MERCADOPAGO_WEBHOOK_URL` vazio.

## 7) Rodar a aplicação
```bash
python app.py
```

Acesse:
- `http://localhost:5000`

---

## Fluxo rápido para testar
1. Cadastre um usuário.
2. Faça login.
3. Cadastre alguns produtos pelo banco ou via área admin.
4. Acesse a home e teste busca/carrinho.
5. Teste compra por gateway e telas de status.
6. Envie feedback e confira no painel admin.

---

## Rotas importantes
- Públicas: `/`, `/index`, `/login`, `/cadastro`
- Usuário logado: `/perfil`, `/carinho`, `/feedback`, `/pagar_entregador/<id>`
- Admin: `/admin`, `/admin_user`, `/admin_produtos`, `/admin_entregador`
- Entregador: `/painel_entregador`
- Webhook pagamento: `/webhook/mercadopago`

---

## Melhorias recomendadas (próximos passos)
- Integrar completamente o controle de tentativas de login (`registrar_erro_login` / `resetar_tentativas`).
- Adicionar migrações (ex.: Flask-Migrate) para versionar schema.
- Criar testes automatizados (rotas, serviços e integração com DB).
- Padronizar naming (`carinho` -> `carrinho`, `gatway` -> `gateway`) para manutenção.
