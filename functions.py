from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import bcrypt
import smtplib
from connection import create_connection
import random
from datetime import date

from app import index

app = Flask(__name__, template_folder='templates')


def dados_menu():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT produto FROM produtos")
    produtos = cursor.fetchall()
    cursor.execute("SELECT datahora FROM datahora")
    datahora = cursor.fetchall()
    cursor.execute("SELECT nome, email, telefone FROM usuarios WHERE email = ?", (session['email'],))
    dados = cursor.fetchall()
    conn.close()
    all = [produtos, datahora, dados]
    return all


def validaSessao(type):
    if session['email'] is None:
        return render_template('index.html', message_login="Voce precisa está logado para acessar o sitema",
                               item=index(), focus="login")
    conn = create_connection()
    cursor = conn.cursor()
    if type == 'adm':
        cursor.execute("SELECT status FROM usuarios WHERE email = ?", (session['email'],))
        status = cursor.fetchone()
        if status[0] == 'adm':
            return render_template('menu_adm.html', dados_user=dados_menu()[2], data_atual=date.today())
    return render_template('menu.html', produtos=dados_menu()[0], datahora=dados_menu()[1], dados_user=dados_menu()[2])


def login_users():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['senha']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        if user:
            hashed_password = user[4]
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                session['email'] = email
                if user[5] == "adm":
                    return redirect('/menu_adm')
                return redirect('/menu')
            else:
                return render_template('index.html', message_login="Senha incorreta", item=index(), focus="login")
        else:
            return render_template('index.html', message_login="Usuário não cadastrado", item=index(),
                                   focus="login")
    return render_template('index.html', item=index())


def recuperar_senha():
    if request.method == 'POST':
        email = request.form['email']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT email FROM usuarios WHERE email=?', [email])
        if len(cursor.fetchall()) != 0:
            escolhas_possiveis = 'ABC123'
            senha = ''
            for i in range(8):
                senha += random.choice(escolhas_possiveis)
            hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('UPDATE usuarios SET senha=? WHERE email=?',
                           (hashed_password.decode('utf-8'), email))
            body = 'Subject: Recuperar senha - Barbershop \n\n\n' + 'Olá senhor(a), segue sua senha provisoria, para o acesso de login no Barbershop: ' + senha
            try:
                smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
            except Exception as e:
                print(e)
                smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login('barbershopclubdb@outlook.com', "Un1v3sp2022")
            smtpObj.sendmail('barbershopclubdb@outlook.com', email, body.encode('utf-8'))
        conn.commit()
        conn.close()

        return render_template('index.html',
                               alert='Uma nova senha foi enviada para o seu email, verifique sua caixa de spam',
                               focus='login', item=index())
    return render_template('index.html', index())


def cadastro(type):
    if request.method == 'POST':
        if type != 'adm':
            nome = request.form['nome']
            email = request.form['email']
            telefone = request.form['telefone']
            senha = request.form['senha']
            hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        email = request.form['email']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT email FROM usuarios WHERE email=?', [email])
        message_login = ""
        if len(cursor.fetchall()) == 0:
            cursor.execute('INSERT INTO usuarios (nome, email, telefone, senha, status) VALUES (?, ?, ?, ?, ?)',
                           (nome, email, telefone, hashed_password.decode('utf-8'), type))
        else:
            if type == 'adm':
                cursor.execute('UPDATE usuarios SET status=? WHERE email=?',
                               (type, email))
                conn.commit()
                conn.close()
                return redirect('/menu_adm')
            message_login = "Usuario já cadastrado"
        conn.commit()
        conn.close()
        return render_template('index.html', item=index(), message_login=message_login, focus='login')
    return render_template('index.html', item=index())


def agendamento():
    if request.method == 'POST':
        email = session['email']
        servico = request.form['servico']
        data = request.form['data']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, telefone FROM usuarios WHERE email = ?", (email,))
        dados = cursor.fetchone()
        cursor.execute('INSERT INTO agendamento (nome, email, telefone, servico, data) VALUES (?, ?, ?, ?, ?)',
                       (dados[0], email, dados[1], servico, data))
        cursor.execute('DELETE FROM datahora WHERE datahora = ?', (data,))
        conn.commit()
        conn.close()
        return redirect("menu")
    return redirect("/")


def get_agendamento(email):
    if request.method == 'POST':
        conn = create_connection()
        cursor = conn.cursor()
        if email != "adm":
            cursor.execute('SELECT id, servico, data FROM agendamento WHERE email = ?', (email,))
        else:
            cursor.execute('SELECT id, nome, email, telefone, servico, data FROM agendamento')
        rows = cursor.fetchall()
        data = []
        if email != "adm":
            for row in rows:
                data.append({
                    'id': row[0],
                    'servico': row[1],
                    'data': row[2],
                    'preco': cursor.execute('SELECT preco FROM produtos WHERE produto = ?', (row[1],)).fetchall()[0]
                })
        else:
            for row in rows:
                data.append({
                    'id': row[0],
                    'nome': row[1],
                    'email': row[2],
                    'telefone': row[3],
                    'servico': row[4],
                    'data': row[5]
                })
        conn.close()
        return jsonify(data)
    return render_template('index.html', message_login="Voce precisa está logado para acessar o sitema",
                           item=index(), focus="login")


def get_usuario():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, email, telefone FROM usuarios')
    usuarios = cursor.fetchall()
    conn.close()

    usuario_list = []
    for usuario in usuarios:
        usuario_list.append({
            'id': usuario[0],
            'nome': usuario[1],
            'email': usuario[2],
            'telefone': usuario[3]
        })
    return jsonify(usuario_list)


def get_servicos_precos():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, produto, preco FROM produtos')
    produtos = cursor.fetchall()
    conn.close()

    produtos_list = []
    for produto in produtos:
        produtos_list.append({
            'id': produto[0],
            'produto': produto[1],
            'preco': produto[2],
        })
    return jsonify(produtos_list)


def get_datahora():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, datahora FROM datahora')
    datahora = cursor.fetchall()
    conn.close()

    datahora_list = []
    for datah in datahora:
        datahora_list.append({
            'id': datah[0],
            'datahora': datah[1],
        })
    return jsonify(datahora_list)


def cadastro_servicos_precos():
    if request.method == 'POST':
        servico = request.form['servico']
        preco = request.form['preco']
        preco = "R$ %.2f" % float(preco)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT produto FROM produtos WHERE produto=?', [servico])
        if len(cursor.fetchall()) != 0:
            cursor.execute('UPDATE produtos SET produto=?, preco=? WHERE produto=?',
                           (servico, preco, servico))
        else:
            cursor.execute('INSERT INTO produtos (produto, preco) VALUES (?, ?)',
                           (servico, preco))
        conn.commit()
        conn.close()
        return redirect('/menu_adm')
    return redirect('/menu_adm')


def cadastro_datahora():
    if request.method == 'POST':
        datahora = request.form['data']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT datahora FROM datahora WHERE datahora=?', [datahora])
        if len(cursor.fetchall()) != 0:
            cursor.execute('UPDATE datahora SET datahora=? WHERE datahora=?',
                           (datahora, datahora, datahora))
        else:
            cursor.execute('INSERT INTO datahora (datahora) VALUES (?)',
                           (datahora,))
        conn.commit()
        conn.close()
        return redirect('/menu_adm')
    return redirect('/menu_adm')


def delete(id, type):
    conn = create_connection()
    cursor = conn.cursor()
    match type:
        case "ag":
            teste = cursor.execute('SELECT data FROM agendamento WHERE id=?', (id,)).fetchone()[0]
            cursor.execute('INSERT INTO datahora (datahora) VALUES (?)',
                           (teste,))
            cursor.execute('DELETE FROM agendamento WHERE id = ?', (id,))

        case "ps":
            cursor.execute('DELETE FROM produtos WHERE id = ?', (id,))
        case "dh":
            cursor.execute('DELETE FROM datahora WHERE id = ?', (id,))
        case _:
            cursor.execute('DELETE FROM usuarios WHERE email = ?', (id,))
            cursor.execute('DELETE FROM agendamento WHERE email = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify(success=True)


def editar_perfil(type):
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        senha = request.form['senha']
        hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        conn = create_connection()
        cursor = conn.cursor()
        verifica = cursor.execute('SELECT email FROM usuarios WHERE email=?', [email])
        verifica = verifica.fetchall()
        if len(verifica) > 0:
            for i in verifica:
                if i != session['email']:
                    message = "Este email já está em uso"
                    return render_template('menu.html',
                                           produtos=dados_menu()[0],
                                           datahora=dados_menu()[1],
                                           dados_user=dados_menu()[2],
                                           message_edit=message,
                                           focus='editar')
        if senha == "":
            cursor.execute('UPDATE usuarios SET nome=?, email=?, telefone=?, status=? WHERE email=?',
                           (nome, email, telefone, type, session['email']))
        else:
            cursor.execute('UPDATE usuarios SET nome=?, email=?, telefone=?, senha=?, status=? WHERE email=?',
                           (nome, email, telefone, hashed_password, type, session['email']))
        conn.commit()
        conn.close()
        session['email'] = email
        if type == "adm":
            return redirect('/menu_adm')
        return redirect('/menu')
    return redirect('/')
