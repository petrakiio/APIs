from flask import Flask, jsonify,request

app = Flask(__name__)
livros = [
    {
        "id":1,
        "titulo":"A coisa",
        "autor":"Stephen king"
    },
    {
        "id":2,
        "titulo":"O homem de palha",
        "autor":"Pablo Zorti"
    },
    {
        "id":3,
        "titulo":"Harry Potter",
        "autor":"J.K Howling"
    }
]
#consultar(todos)
@app.route('/livros',methods=['GET'])
def obter_livro():
    return jsonify(livros)

#consultar(por id)
@app.route('/livros/<int:id>', methods=['GET'])
def obter_id(id):
    for livro in livros:
        if livro.get('id') == id:
            return jsonify(livro)

#editar
@app.route('/livros/<int:id>', methods=['GET'])
def editar_livros(id):
    livro_alterado = request.get_json()
    for indece,livro in enumarete(livros):
        if livro.get('id') == id:
            livros[indece].update(livro_alterado)
            return jsonify(livros[indece])

#Incluir
@app.route('/livros',methods=['POST'])
def Incluir():
    nome_livro = request.get_json()
    livros.append(nome_livro)
    return jsonify(livros)

#Excluir
@app.route('/livros/<int:id>',methods=['DELETE'])
def Excluir(id):
    for indice,livro in enumerate(livros):
        if livro.get('id') == id:
            del livros[indice]
        return jsonify(livros)
app.run(port=5000,host='localhost',debug=True)