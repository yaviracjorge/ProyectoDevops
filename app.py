import os
import psycopg2
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# ==========================
# CONFIGURACIÓN
# ==========================

APP_NAME = os.getenv("APP_NAME", "Aplicación DevOps")

try:
    with open("VERSION", "r") as f:
        APP_VERSION = f.read().strip()
except FileNotFoundError:
    APP_VERSION = os.getenv("APP_VERSION", "3.0.0")

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")


# ==========================
# BASE DE DATOS
# ==========================

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS productos(
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100),
            precio NUMERIC(10,2),
            stock INT
        );
        """)

        cur.execute("SELECT COUNT(*) FROM productos")

        if cur.fetchone()[0] == 0:

            productos = [
                ('Laptop ASUS',899.99,15),
                ('Mouse Logi',25.50,50),
                ('Teclado Mecánico',75,30),
                ('Monitor 24"',150,20),
                ('Audífonos Gamer',45.90,40)
            ]

            cur.executemany(
                "INSERT INTO productos(nombre,precio,stock) VALUES(%s,%s,%s)",
                productos
            )

            print("Productos iniciales insertados.")

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print("BD no disponible todavía:", e)


# ==========================
# HTML
# ==========================

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>{{app_name}}</title>

<style>

*{
margin:0;
padding:0;
box-sizing:border-box;
font-family:Segoe UI,sans-serif;
}

body{

background:linear-gradient(135deg,#0f172a,#1e293b,#334155);
color:white;
padding:40px;

}

.container{

max-width:900px;
margin:auto;
background:rgba(255,255,255,.08);
backdrop-filter:blur(15px);
padding:40px;
border-radius:20px;
box-shadow:0 0 20px rgba(0,0,0,.4);

}

h1{

text-align:center;
color:#38bdf8;

}

.clock{

font-size:60px;
text-align:center;
margin-top:20px;
font-weight:bold;

}

.date{

text-align:center;
margin-top:10px;
font-size:20px;

}

.info{

margin-top:40px;
font-size:18px;

}

table{

width:100%;
margin-top:20px;
border-collapse:collapse;

}

th{

background:#38bdf8;
color:#000;
padding:12px;

}

td{

padding:10px;
border-bottom:1px solid rgba(255,255,255,.2);
text-align:center;

}

.footer{

margin-top:25px;
text-align:center;
color:#94a3b8;

}

</style>

</head>

<body>

<div class="container">

<h1>⏰ {{app_name}}</h1>

<div id="clock" class="clock">
00:00:00
</div>

<div id="date" class="date">
...
</div>

<div class="info">

<p><strong>Versión:</strong> {{version}}</p>

<p><strong>Estado PostgreSQL:</strong> {{db_status}}</p>

</div>

<h2 style="margin-top:35px;">Productos</h2>

<table>

<tr>

<th>ID</th>
<th>Nombre</th>
<th>Precio</th>
<th>Stock</th>

</tr>

{% for p in productos %}

<tr>

<td>{{p[0]}}</td>
<td>{{p[1]}}</td>
<td>${{p[2]}}</td>
<td>{{p[3]}}</td>

</tr>

{% endfor %}

</table>

<div class="footer">
Flask + PostgreSQL + DevOps
</div>

</div>

<script>

function updateClock(){

const now=new Date();

document.getElementById("clock").innerHTML=
now.toLocaleTimeString("es-EC");

let fecha=now.toLocaleDateString("es-EC",{

weekday:"long",
year:"numeric",
month:"long",
day:"numeric"

});

document.getElementById("date").innerHTML=
fecha.charAt(0).toUpperCase()+fecha.slice(1);

}

setInterval(updateClock,1000);

updateClock();

</script>

</body>

</html>
"""


# ==========================
# RUTAS
# ==========================

@app.route("/")
def home():

    try:

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM productos")

        productos = cur.fetchall()

        cur.close()
        conn.close()

        estado = "🟢 Conectado"

    except Exception as e:

        productos = []
        estado = f"🔴 {e}"

    return render_template_string(
        HTML,
        app_name=APP_NAME,
        version=APP_VERSION,
        db_status=estado,
        productos=productos
    )


@app.route("/productos")
def productos():

    try:

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM productos")

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify([
            {
                "id":r[0],
                "nombre":r[1],
                "precio":float(r[2]),
                "stock":r[3]
            }
            for r in rows
        ])

    except Exception as e:

        return jsonify({"error":str(e)}),500


@app.route("/api/info")
def info():

    try:
        conn = get_db_connection()
        conn.close()
        estado = "Conectado"

    except Exception as e:
        estado = str(e)

    return jsonify({

        "nombre_aplicacion":APP_NAME,
        "version":APP_VERSION,
        "postgresql":estado

    })


# ==========================
# MAIN
# ==========================

if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )