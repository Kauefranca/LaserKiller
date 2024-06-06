from flask import Flask, render_template, request, session, redirect, Response
from flask_session import Session
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash

from sources.utils import errorhandler, login_required, not_login_required
from sources.postgres import Postgress
from sources.vision import Identificador

import json

# Carregar configurações
faq_items = json.load(open('config/faq.json', encoding='utf-8'))

DB_CONN = Postgress(host='localhost', database='postgres')
DB_CONN.connect()

identificador = Identificador()

app = Flask(__name__)

# app.secret_key = 'super secret key'
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_FILE_DIR"] = './sessions/'
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = 604800

Session(app)

# Garantir que as respostas não entrem em cache
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        rows = DB_CONN.execute_query("""SELECT * FROM usuario WHERE email = %s;""", (request.form.get("email"),))

        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return render_template("login.html", msg="Credenciais inválidas!")

        session["user_id"] = rows[0][0]

        user_id = rows[0][0]
        session["user_id"] = user_id

        if request.form.get('lembrar_me'):
            app.config["PERMANENT_SESSION_LIFETIME"] = 604800
        else:
            app.config["PERMANENT_SESSION_LIFETIME"] = 7200

        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/login")

@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html")

@app.route("/acompanhar", methods=["GET"])
@login_required
def reconhecimento():
    return render_template('acompanhar.html')

@app.route("/cadastro", methods=["GET"])
@login_required
def cadastro():
    return render_template('cadastro.html')

@app.route("/relatorio", methods=["GET", "POST"])
@login_required
def relatorio():
    if request.method == "POST":
        rows = DB_CONN.execute_query("""
            SELECT data, qntErvasDetec, porcErvasDetectadas, situacao, risco
            FROM registro;
        """)
    
        if len(rows) == 0:
            return render_template("login.html", msg="Credenciais inválidas!")

        result_json = []
        for row in rows:
            data, qntErvasDetec, porcErvasDetectadas, situacao, risco = row
            result_json.append({
                "Data": data.strftime("%Y-%m-%d %H:%M:%S"),
                "QntErvasDetec": qntErvasDetec,
                "PorcErvasDetectadas": porcErvasDetectadas,
                "Situacao": situacao,
                "Risco": risco
            })

            response = app.response_class(
                response=json.dumps(result_json),
                status=200,
                mimetype='application/json'
            )

        return response

    else: 
        return render_template('relatorio.html')

@app.route("/download", methods=["GET"])
@login_required
def download():
    return render_template('download.html')

@app.route("/perfil", methods=["GET"])
@login_required
def perfil():
    return render_template('perfil.html')

@app.route("/sobre", methods=["GET"])
def sobre():
    return render_template('sobre.html')

@app.route("/faq", methods=["GET"])
def faq():
    return render_template('faq.html', faq_items=faq_items)

@app.route("/recuperar", methods=["GET"])
@not_login_required
def recuperar():
    return render_template('recuperar.html')

@app.route("/politica-de-privacidade", methods=["GET"])
def politica_de_privacidade():
    return render_template('politica-de-privacidade.html')

@app.route('/camera_feed')
def rec():
    return Response(gen_feed(), mimetype='multipart/x-mixed-replace; boundary=frame ')

def gen_feed():
    while True:
        frame = identificador.read()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Método para capturar erros
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
    app.run(app, debug=True, use_reloader=True)