📚 Book API - RESTful CRUD com Flask
Este projeto é uma API RESTful desenvolvida em Python utilizando o framework Flask. Ela permite o gerenciamento completo de um catálogo de livros, aplicando os principais métodos HTTP para manipulação de dados em memória.

Funcionalidades
Listar Catálogo: Consulta todos os livros cadastrados.

Busca Refinada: Localização de títulos específicos através de ID.

Cadastro Dinâmico: Inclusão de novos títulos ao acervo.

Edição: Atualização de informações de livros existentes.

Remoção: Exclusão de registros do sistema.

🛠️ Tecnologias Utilizadas
Python 3.x

Flask (Micro-framework web)

JSON (Formato de intercâmbio de dados)

Método	|Endpoint|	  |Descrição
GET	    |/livros |    |Retorna todos os livros
GET	    |/livros/<id>|	  |Retorna um livro por ID
POST	  |/livros|	      |Cadastra um novo livro
PUT     |/livros/<id>|	  |Atualiza um livro existente
DELETE  |/livros/<id>| |Remove um livro do catálogo
