from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reloj Digital</title>

    <style>
        *{
            margin:0;
            padding:0;
            box-sizing:border-box;
            font-family:'Segoe UI', sans-serif;
        }

        body{
            height:100vh;
            display:flex;
            justify-content:center;
            align-items:center;
            background:linear-gradient(135deg,#0f172a,#1e293b,#334155);
            overflow:hidden;
        }

        .container{
            text-align:center;
            background:rgba(255,255,255,0.08);
            backdrop-filter:blur(15px);
            padding:50px;
            border-radius:30px;
            box-shadow:0 0 30px rgba(0,0,0,0.4);
            color:white;
            width:90%;
            max-width:600px;
        }

        h1{
            font-size:3rem;
            margin-bottom:20px;
            color:#38bdf8;
        }

        .clock{
            font-size:5rem;
            font-weight:bold;
            letter-spacing:4px;
            color:#fff;
            text-shadow:0 0 20px #38bdf8;
        }

        .date{
            margin-top:20px;
            font-size:1.5rem;
            color:#cbd5e1;
        }

        .footer{
            margin-top:30px;
            color:#94a3b8;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>⏰ Reloj Digital</h1>

    <div class="clock" id="clock">
        00:00:00
    </div>

    <div class="date" id="date">
        Cargando fecha...
    </div>

    <div class="footer">
        Landing Page con Flask
    </div>
</div>

<script>
function updateClock(){
    const now = new Date();

    const time = now.toLocaleTimeString('es-EC');
    const date = now.toLocaleDateString('es-EC',{
        weekday:'long',
        year:'numeric',
        month:'long',
        day:'numeric'
    });

    document.getElementById("clock").innerHTML = time;
    document.getElementById("date").innerHTML =
        date.charAt(0).toUpperCase() + date.slice(1);
}

setInterval(updateClock,1000);
updateClock();
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)