from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import functions
from connection import create_connection

app = Flask(__name__, static_url_path='/static')

app.secret_key = 'barbershop@123'


@app.route('/')
def index():
    session['email'] = None
    conn = create_connection()
    cursor = conn.cursor()
    preco = cursor.execute('SELECT preco FROM produtos').fetchall()
    conn.commit()
    conn.close()
    return render_template('index.html', item=preco)


@app.route('/login', methods=['POST'])
def login():
    return functions.login_users()


@app.route('/reset_pwd', methods=['POST'])
def reset_pwd():
    return functions.recuperar_senha()


@app.route('/cadastro', methods=['POST'])
def cadastro():
    return functions.cadastro('user')


@app.route('/menu_adm')
def menu_adm():
    login = functions.validaSessao('adm')
    return login


@app.route('/menu')
def menu():
    login = functions.validaSessao('')
    return login


@app.route('/agendamento', methods=['POST'])
def agendamento():
    return functions.agendamento()


@app.route('/cadastro_adm', methods=['POST'])
def cadastro_adm():
    return functions.cadastro('adm')


@app.route('/consulta_usuario', methods=['POST'])
def consulta_usuario():
    return functions.get_usuario()


@app.route('/delete_usuario/<email>', methods=['POST'])
def delete_usuario(email):
    delete = functions.delete(email, "user")
    return delete


@app.route('/consulta_agendamento/<type>', methods=['POST'])
def consulta_agendamento(type):
    if type == 'user':
        get = functions.get_agendamento(session['email'])
        return get
    get = functions.get_agendamento("adm")
    return get


@app.route('/delete_ag/<id>', methods=['POST'])
def delete_ag(id):
    delete = functions.delete(id, "ag")
    return delete


@app.route('/cadastro_servicos_precos', methods=['POST'])
def cadastro_servicos_precos():
    return functions.cadastro_servicos_precos()


@app.route('/consulta_servicos_precos', methods=['POST'])
def consulta_servicos_precos():
    get = functions.get_servicos_precos()
    return get


@app.route('/delete_ps/<id>', methods=['POST'])
def delete_ps(id):
    delete = functions.delete(id, "ps")
    return delete


@app.route('/cadastro_datahora', methods=['POST'])
def cadastro_datahora():
    return functions.cadastro_datahora()

@app.route('/consulta_datahora', methods=['POST'])
def consulta_consulta_datahora():
    get = functions.get_datahora()
    return get


@app.route('/delete_dh/<id>', methods=['POST'])
def delete_dh(id):
    delete = functions.delete(id, "dh")
    return delete

@app.route('/editar_user', methods=['POST'])
def editar_user():
    set = functions.editar_perfil("user")
    return set

@app.route('/editar_adm', methods=['POST'])
def editar_adm():
    set = functions.editar_perfil("adm")
    return set

if __name__ == '__main__':
    app.run(debug=True)
