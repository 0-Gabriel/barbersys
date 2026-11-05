from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)


def conectar_bd():
    conn = sqlite3.connect('barbersys.db')
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/api/clientes', methods=['POST'])
def cadastrar_cliente():
    dados = request.get_json(silent=True) or {}
    nome = dados.get('nome')
    telefone = dados.get('telefone')
    email = dados.get('email')
    if not isinstance(nome, str) or not nome.strip() or not isinstance(telefone, str) or not telefone.strip():
        return jsonify({"status": "erro", "mensagem": "Nome e telefone sao obrigatorios."}), 400
    conn = conectar_bd()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cliente (nome, telefone, email) VALUES (?, ?, ?)", (nome.strip(), telefone.strip(), email))
        conn.commit()
        return jsonify({"status": "ok", "id": cursor.lastrowid}), 201
    finally:
        conn.close()


@app.route('/api/agendamentos', methods=['POST'])
def criar_agendamento():
    dados = request.get_json(silent=True) or {}
    id_cliente = dados.get('id_cliente')
    id_servico = dados.get('id_servico')
    id_profissional = dados.get('id_profissional')
    data_hora_bruta = dados.get('data_hora')
    if not all([id_cliente, id_servico, id_profissional, data_hora_bruta]):
        return jsonify({"status": "erro", "mensagem": "Todos os IDs e data/hora sao obrigatorios."}), 400
    try:
        dt_obj = datetime.fromisoformat(data_hora_bruta)
        data_hora = dt_obj.strftime('%Y-%m-%d %H:%M')
    except (TypeError, ValueError):
        return jsonify({"status": "erro", "mensagem": "Data/hora invalida."}), 400
    if dt_obj.minute not in (0, 30):
        return jsonify({"status": "erro", "mensagem": "Agende em blocos de 30 minutos."}), 400
    conn = conectar_bd()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM agendamento WHERE id_profissional = ? AND data_hora = ? AND status = 'Confirmado'",
            (id_profissional, data_hora))
        if cursor.fetchone()[0] > 0:
            return jsonify({"status": "erro", "mensagem": "Profissional ocupado neste horario."}), 409
        cursor.execute(
            "INSERT INTO agendamento (id_cliente, id_servico, id_profissional, data_hora, status) VALUES (?, ?, ?, ?, 'Confirmado')",
            (id_cliente, id_servico, id_profissional, data_hora))
        conn.commit()
        return jsonify({"status": "ok", "id": cursor.lastrowid}), 201
    except sqlite3.IntegrityError:
        return jsonify({"status": "erro", "mensagem": "Cliente, servico ou profissional inexistente."}), 400
    finally:
        conn.close()
def iniciar_bd():
    conn = sqlite3.connect('barbersys.db')
    with open('schema.sql', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.close()


if __name__ == '__main__':
    iniciar_bd()
    app.run(debug=True)