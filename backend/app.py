# Importando o Flask e criandos as rotas para o front comunicar com o back
from flask import Flask, send_from_directory, jsonify, request
from backend.utils.backup_usuarios import backup_usuarios
from pathlib import Path


# Estado global do backuup
status_backup= {
    "progresso": 0,
    "mensagem" : "Aguardando início do backup...",
    "em_execucao": False
}


app = Flask(__name__, static_folder="../frontend", template_folder="frontend")



# Rota criada para o index
@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")



# Rota para o back backup_usuarios (rota principal)
@app.route("/api/backup_usuarios", methods=["POST"])
def route_backup_usuarios():
    try:
        data = request.get_json()
        user_name = str(data.get("user_name"))

        resultado = backup_usuarios(user_name)

        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    


# Rota criada para o css e js
@app.route("/static/<path:path>")
def server_static(path):
    return send_from_directory("../frontend/static", path)



# Rota para listar os usuários
@app.route("/api/usuarios", methods=["GET"])
def route_users():
    base_path = Path(r"C:\Users")



    # Lista de usuario proibidos
    usuarios_proibidos = {
        #"Public",
        "Default",
        "Default User",
        "All Users",
        "Todos os Usuários",
        "Usuário Padrão",
        "Padrão"
    }

    usuarios = []

    for item in base_path.iterdir():
        if item.is_dir() and item.name not in usuarios_proibidos:
            usuarios.append(item.name)
    
    return jsonify({"usuarios": usuarios})


# Rota de status do backup
@app.route("/api/backup/status", methods=["GET"])
def status_backup_route():
    return jsonify({
        "progresso": status_backup["progresso"],
        "mensagem": status_backup["mensagem"],
        "em_execucao": status_backup["em_execucao"]
    })