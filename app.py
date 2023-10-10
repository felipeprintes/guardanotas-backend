from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId 
import logging
import json
import ast

logging.basicConfig(
    level=logging.DEBUG,  # Escolha o nível de registro desejado (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # Saída para um arquivo
        logging.StreamHandler()  # Saída para o console
    ]
)

app = Flask(__name__)

client = MongoClient(
    'localhost', 
    27017, 
    username='root', 
    password='rootpassword'
)

db = client.flask_db
notas = db.notas

@app.route('/')
def index():
    return 'Nothing to show'


def decode_data(data):
    data = data.decode('utf-8')
    data = ast.literal_eval(data)

    return data

@app.route('/new_note', methods=['POST'])
def new_note():
    try:
        dados = request.data

        logging.info(f'dados : {dados}')

        dados = decode_data(dados)
        if 'content' in dados:
            
            content = dados['content']
            logging.info(f"CONTENT: {dados['content']}")

            insert = notas.insert_one({'note_content': content})

            if insert.inserted_id:
                return jsonify({'mensagem': 'Dados inseridos com sucesso!'}), 200
            else:
                return jsonify({'mensagem': 'Erro ao inserir os dados.'}), 500

    except Exception as err:
        return jsonify({'msg': str(err)}), 500

@app.route('/my_notes', methods=['GET'])
def my_notes():
    result = notas.find()

    result_list = []
    for item in result:
        item['_id'] = str(item['_id'])
        result_list.append(item)

    logging.info(f'RESULT_INFO: {result_list}')

    return jsonify(result_list)

@app.route('/delete_note', methods=['POST'])
def delete_note():
    
    dados = request.data

    data_decoded = decode_data(dados)
    logging.info(f'Data that should be deleted : {data_decoded}')

    if data_decoded and '_id' in data_decoded:
        data_id = ObjectId(data_decoded['_id'])
        logging.info(data_id)

        result = notas.delete_one({'_id': data_id})

        if result.deleted_count == 1:
            return jsonify({"mensagem": "Documento excluído com sucesso"})
        else:
            return jsonify({"mensagem": "Documento não encontrado"})
    else:
        return jsonify({"mensagem": "Dados inválidos ou ID do documento não fornecido"})

@app.route('/edit_note')
def edit_note():
    # Will be implement as soon as possible
    pass

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)