from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import bcrypt

app = Flask(__name__)
CORS(app)

def get_connection():
    return mysql.connector.connect(
        host="localHost",
        user="root",
        password="16022006",
        database="misout_db"
    )

# --- USUÁRIOS ---
@app.route("/add-user", methods=["POST"])
def add_user():
    data = request.json
    nome = data["nome"]
    email = data["email"]
    senha = data["senha"]

    try:
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome_completo, email, senha) VALUES (%s, %s, %s)",
            (nome, email, senha_hash.decode('utf-8'))
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "ok", "mensagem": "Usuário cadastrado!"})
    
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route("/usuarios", methods=["GET"])
def get_usuarios():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nome_completo, email, tipo_plano FROM usuarios")
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(resultados)
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

# --- LOGIN ---
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    senha = data["senha"]

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        
        if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario['senha'].encode('utf-8')):
            return jsonify({"status": "ok", "mensagem": "Login realizado!"})
        else:
            return jsonify({"status": "erro", "mensagem": "Email ou senha inválidos"}), 401
            
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

# --- INSCRIÇÕES ---
@app.route("/add-inscricao", methods=["POST"])
def add_inscricao():
    data = request.json
    endereco = data["endereco"]
    pontoRef = data["pontoRef"]
    tipoTurismo = data["tipoTurismo"]
    cidade = data["cidade"]
    uf = data["UF"]
    nomeLocal = data["nomeLocal"]
    dias_funcionamento = data.get("dias_funcionamento", "")
    preco_minimo = data.get("preco_minimo", 0)
    necessita_ingresso = data.get("necessita_ingresso", False)

    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM destinos WHERE nome = %s AND estado = %s", (cidade, uf))
        destino = cursor.fetchone()
        
        if not destino:
            return jsonify({"status": "erro", "mensagem": "Destino não encontrado"}), 400
            
        destino_id = destino[0]
        
        categoria_map = {
            'museu': 1, 'cultural': 1, 'histórico': 1,
            'estádio': 2, 'esportivo': 2, 'futebol': 2,
            'shopping': 3, 'compras': 3, 'lojas': 3,
            'evento': 4, 'festival': 4, 'show': 4,
            'teatro': 5, 'cinema': 5, 'cultural': 5,
            'parque': 6, 'natureza': 6, 'ar livre': 6,
            'restaurante': 7, 'gastronômico': 7, 'comida': 7,
            'igreja': 8, 'religioso': 8, 'templo': 8
        }
        
        tipo_lower = tipoTurismo.lower()
        categoria_id = 1  # default
        
        for key, value in categoria_map.items():
            if key in tipo_lower:
                categoria_id = value
                break
        
        
        cursor.execute(
            """INSERT INTO pontos_turisticos 
            (destino_id, categoria_id, nome, endereco, ponto_referencia, tipo_turismo, 
             dias_funcionamento, preco_minimo, necessita_ingresso, aprovado) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)""",  # ⚠️ aprovado = FALSE
            (destino_id, categoria_id, nomeLocal, endereco, pontoRef, tipoTurismo, 
             dias_funcionamento, preco_minimo, necessita_ingresso)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "ok", "mensagem": "Inscrição realizada! Aguarde aprovação."})
    
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route("/inscricoes", methods=["GET"])
def get_inscricoes():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT pt.*, d.nome as cidade, d.estado 
            FROM pontos_turisticos pt 
            JOIN destinos d ON pt.destino_id = d.id
        """)
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(resultados)
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

# --- ASSINATURAS ---
@app.route("/add-assinatura", methods=["POST"])
def add_assinatura():
    data = request.json
    nome = data["nome"]
    email = data["email"]
    telefone = data["telefone"]
    tipo_plano = data["tipo_plano"]
    valor = data["valor"]
    metodo_pagamento = data["metodo_pagamento"]

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verificar se usuário já existe
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        
        if usuario:
            usuario_id = usuario['id']
            cursor.execute(
                "UPDATE usuarios SET tipo_plano = %s WHERE id = %s",
                (tipo_plano, usuario_id)
            )
        else:
            cursor.execute(
                "INSERT INTO usuarios (nome_completo, email, tipo_plano) VALUES (%s, %s, %s)",
                (nome, email, tipo_plano)
            )
            usuario_id = cursor.lastrowid
        
        from datetime import datetime, timedelta
        data_inicio = datetime.now().date()
        data_fim = data_inicio + timedelta(days=30)
        
        cursor.execute(
            """INSERT INTO assinaturas 
            (usuario_id, tipo_plano, data_inicio, data_fim, valor, metodo_pagamento, status, telefone) 
            VALUES (%s, %s, %s, %s, %s, %s, 'ativa', %s)""",
            (usuario_id, tipo_plano, data_inicio, data_fim, valor, metodo_pagamento, telefone)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "ok", "mensagem": "Assinatura realizada com sucesso!"})
    
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route("/assinaturas", methods=["GET"])
def get_assinaturas():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.*, u.nome_completo, u.email 
            FROM assinaturas a 
            JOIN usuarios u ON a.usuario_id = u.id
        """)
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(resultados)
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500
    
# --- VINCULAR USUÁRIO COM ASSINATURA ---
@app.route("/vincular-assinatura", methods=["POST"])
def vincular_assinatura():
    data = request.json
    email = data["email"]
    senha = data["senha"]

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT a.* 
            FROM assinaturas a 
            JOIN usuarios u ON a.usuario_id = u.id 
            WHERE u.email = %s AND a.status = 'ativa'
        """, (email,))
        
        assinatura = cursor.fetchone()
        
        if assinatura:

            senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            cursor.execute(
                "UPDATE usuarios SET senha = %s WHERE email = %s",
                (senha_hash.decode('utf-8'), email)
            )
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return jsonify({"status": "ok", "mensagem": "Cadastro completado e vinculado à assinatura!"})
        else:
            return jsonify({"status": "erro", "mensagem": "Nenhuma assinatura ativa encontrada para este email"}), 400
            
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500
    
# --- CATEGORIAS POR DESTINO ---
@app.route("/categorias/<destino>", methods=["GET"])
def get_categorias_por_destino(destino):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT DISTINCT c.id, c.nome, c.icone, COUNT(pt.id) as total_pontos
            FROM categorias c
            LEFT JOIN pontos_turisticos pt ON c.id = pt.categoria_id 
            LEFT JOIN destinos d ON pt.destino_id = d.id
            WHERE d.nome = %s AND pt.aprovado = TRUE
            GROUP BY c.id, c.nome, c.icone
            HAVING COUNT(pt.id) > 0
            ORDER BY total_pontos DESC
        """, (destino.title(),))
        
        categorias = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(categorias)
        
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

# --- PONTOS TURÍSTICOS POR DESTINO E CATEGORIA ---
@app.route("/pontos-turisticos/<destino>/<categoria>", methods=["GET"])
def get_pontos_turisticos(destino, categoria):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT pt.*, d.nome as cidade, d.estado, c.nome as categoria_nome, c.icone
            FROM pontos_turisticos pt 
            JOIN destinos d ON pt.destino_id = d.id
            JOIN categorias c ON pt.categoria_id = c.id
            WHERE d.nome = %s AND c.nome = %s AND pt.aprovado = TRUE
        """, (destino.title(), categoria.title()))
        
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(resultados)
        
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

# --- TODOS OS PONTOS POR DESTINO ---
@app.route("/pontos-turisticos/<destino>", methods=["GET"])
def get_pontos_por_destino(destino):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT pt.*, d.nome as cidade, d.estado, c.nome as categoria_nome, c.icone
            FROM pontos_turisticos pt 
            JOIN destinos d ON pt.destino_id = d.id
            JOIN categorias c ON pt.categoria_id = c.id
            WHERE d.nome = %s AND pt.aprovado = TRUE
        """, (destino.title(),))
        
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(resultados)
        
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

# --- ESTATÍSTICAS DA CIDADE ---
@app.route("/estatisticas/<destino>", methods=["GET"])
def get_estatisticas_destino(destino):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT COUNT(*) as total_pontos
            FROM pontos_turisticos pt 
            JOIN destinos d ON pt.destino_id = d.id
            WHERE d.nome = %s AND pt.aprovado = TRUE
        """, (destino.title(),))
        total_pontos = cursor.fetchone()
        
        cursor.execute("""
            SELECT COUNT(DISTINCT c.id) as total_categorias
            FROM categorias c
            JOIN pontos_turisticos pt ON c.id = pt.categoria_id 
            JOIN destinos d ON pt.destino_id = d.id
            WHERE d.nome = %s AND pt.aprovado = TRUE
        """, (destino.title(),))
        total_categorias = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "total_pontos": total_pontos['total_pontos'],
            "total_categorias": total_categorias['total_categorias']
        })
        
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)