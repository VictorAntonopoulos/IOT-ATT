import sqlite3, threading, time, os, json
from flask import Flask, jsonify, send_from_directory, request
from flask_socketio import SocketIO

# Caminho completo do banco
DB_PATH = r"D:\IOT-master (1)\IOT-master\telemetria.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = "dashboard.html"

# Cria tabela se não existir
conn = sqlite3.connect(DB_PATH)
conn.execute("""
CREATE TABLE IF NOT EXISTS telemetria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    moto_id TEXT,
    sensor TEXT,
    value TEXT,
    timestamp INTEGER
)
""")
conn.commit()
conn.close()

# Inicializa Flask
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Servir HTML do dashboard
@app.route("/")
def index():
    return send_from_directory(BASE_DIR, HTML_FILE)

# Retornar últimas 20 leituras
@app.route("/api/telemetry/recent")
def recent():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
    cur = conn.cursor()
    cur.execute("SELECT * FROM telemetria ORDER BY id DESC LIMIT 20")
    rows = cur.fetchall()
    conn.close()
    return jsonify([
        {
            "motoId": r["moto_id"], 
            "sensor": r["sensor"], 
            "value": json.loads(r["value"]), 
            "timestamp": r["timestamp"],
            "ok": True
        } for r in reversed(rows)
    ])

# Rota para receber leituras via POST e emitir para Socket.IO
@app.route("/new_reading", methods=["POST"])
def new_reading():
    data = request.json
    if data:
        socketio.emit("new_reading", data)
    return jsonify({"status":"ok"}), 200

# Monitorar banco e enviar novas leituras em tempo real
def monitor_db():
    last_id = 0
    while True:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM telemetria WHERE id>? ORDER BY id ASC", (last_id,))
        rows = cur.fetchall()
        for r in rows:
            socketio.emit("new_reading", {
                "motoId": r["moto_id"],
                "sensor": r["sensor"],
                "value": json.loads(r["value"]),
                "timestamp": r["timestamp"],
                "ok": True
            })
            last_id = r["id"]
        conn.close()
        time.sleep(0.5)

# Inicia monitoramento em background
threading.Thread(target=monitor_db, daemon=True).start()

if __name__ == "__main__":
    print("Dashboard rodando em http://localhost:5008")
    socketio.run(app, host="0.0.0.0", port=5008)
