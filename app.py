from datetime import datetime

from flask import Flask, render_template, url_for, flash, request, redirect
from sqlalchemy.exc import SQLAlchemyError

from api_routes import routes
from database import db_session, Funcionario
from sqlalchemy import select, and_, func
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

app = Flask(__name__)
# mover para .env
app.config['SECRET_KEY'] = '1234'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@login_manager.user_loader
def load_user(user_id):
    user = select(Funcionario).where(Funcionario.id == int(user_id))
    resultado = db_session.execute(user).scalar_one_or_none()
    return resultado

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_funcionario():
    if request.method == 'POST':
        nome = request.form['form-nome']
        data_de_nascimento = request.form['form-nascimento']
        cpf = request.form['form-cpf']
        email = request.form['form-email']
        senha = request.form['form-senha']
        cargo = request.form['form-cargo']
        salario = float(request.form['form-salario'])
        data_convertida = datetime.strptime(data_de_nascimento, '%Y-%m-%d')
        if not nome or not email or not senha or not data_de_nascimento or not cpf or not cargo or not salario:
            flash(f'Preencher todos os campos', 'danger')
            return render_template('login.html')
        verifica_email = select(Funcionario).where(Funcionario.email == email)
        verifica_cpf = select(Funcionario).where(Funcionario.cpf == cpf)
        existe_email = db_session.execute(verifica_email).scalar_one_or_none()
        existe_cpf = db_session.execute(verifica_cpf).scalar_one_or_none()

        if existe_email or existe_cpf:
            flash(f'Email {email} ja existente ou CPF {cpf} ja existe!', 'danger')
            return redirect (url_for('funcionarios'))
        try:
            novo_usuario = Funcionario(nome=nome, email=email, cpf=cpf, data_de_nascimento=data_convertida, senha=senha, cargo=cargo, salario=salario)
            novo_usuario.set_password(senha)
            db_session.add(novo_usuario)
            db_session.commit()
            flash(f'Funcionario {nome} cadastrado com sucesso', 'success')
            return redirect(url_for('funcionarios'))
        except SQLAlchemyError as e:
            flash(f'Erro na base de dados ao cadastrar funcionario', 'danger')
            print(f'Error na base de dados: {e}')
            return redirect(url_for('funcionarios'))
        except Exception as e:
            flash(f'Erro ao cadastrar funcionario', 'danger')
            print(f'Error ao cadastrar: {e}')
            return redirect(url_for('funcionarios'))
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('form-email')
        senha = request.form.get('form-senha')

        if email and senha:
            verificar_email = select(Funcionario).where(Funcionario.email == email)
            resultado_email = db_session.execute(verificar_email).scalar_one_or_none()
            if resultado_email:
                # se encontrado na base de dados
                if resultado_email.check_password(senha):
                    # login correto
                    login_user(resultado_email)
                    flash(f'Login feito com sucesso', 'success')
                    return redirect(url_for('home'))
                else:
                    # login incorreto
                    flash('Senha incorreta', 'alert-danger')
                    # render_templete : carrega a pagina html
                    # redirect: com o url_for ele chama a função e ela carrega a pagina
                    return redirect(url_for('login'))

            else:
                # se nao encontrado na base de dados
                flash(f'Email nao encontrado', 'alert-danger')
                return render_template('login.html')
        else:
            return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('Logout realizado com sucesso', 'success')
    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/calculos')
def calculos():
    return render_template("calculos.html")

@app.route('/funcionarios', methods=['GET', 'POST'])
@login_required
def funcionarios():
    _funcionarios_sql = select(Funcionario)
    _funcionarios_resultado = db_session.execute(_funcionarios_sql).scalars().all()

    return render_template("funcionarios.html", lista_funcionarios=_funcionarios_resultado)


@app.route('/operacoes')
def operacoes():
    return render_template("operacoes.html")


@app.route('/somar', methods=['GET', 'POST'])
def somar():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            soma = n1 + n2
            flash("Soma realizada!", 'alert-success')
            return render_template("operacoes.html", n1=n1, n2=n2, soma=soma)
        else:
            # Passo 1: Emitir a mensagem e a categoria do flash
            flash("Preencha o campo para realizar a soma!", 'alert-danger')

    return render_template("operacoes.html")


@app.route('/subtrair', methods=['GET', 'POST'])
def subtrair():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            subtrair = n1 - n2
            return render_template("operacoes.html", n1=n1, n2=n2, subtrair=subtrair)
        return render_template("operacoes.html")


@app.route('/multiplicar', methods=['GET', 'POST'])
def multiplicar():
    if request.method == 'POST':
        if request.form['form*n1'] and request.form['form*n2']:
            n1 = int(request.form['form*n1'])
            n2 = int(request.form['form*n2'])
            multiplicar = n1 * n2
            return render_template("operacoes.html", n1=n1, n2=n2, multiplicar=multiplicar)
        return render_template("operacoes.html")


@app.route('/dividir', methods=['GET', 'POST'])
def dividir():
    if request.method == 'POST':
        if request.form['form/n1'] and request.form['form/n2']:
            n1 = int(request.form['form/n1'])
            n2 = int(request.form['form/n2'])
            dividir = n1 / n2
            return render_template("operacoes.html", n1=n1, n2=n2, dividir=dividir)
        return render_template("operacoes.html")


@app.route('/geometria')
def geometria():
    return render_template("geometria.html")

@app.route('/triangulo', methods=['GET', 'POST'])
def triangulo():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            perimetro = n1 + n1 + n1
            area = n1 / n1 /2
            flash("Cálculo realizado!", 'alert-success')
            return render_template("geometria.html", n1=n1, perimetro=perimetro, area=area)
        else:
            # Passo 1: Emitir a mensagem e a categoria do flash
            flash("Preencha o campo para realizar o cálculo!", 'alert-danger')
        return render_template("geometria.html")

@app.route('/circulo', methods=['GET', 'POST'])
def circulo():
    if request.method == 'POST':
        n2 = int(request.form['form-n2'])
        perimetro_2 = 2 * 3.14 * n2
        area_2 = 3.14 * n2 ** 2
        flash("Cálculo realizado!", 'alert-success')
        return render_template("geometria.html", n2=n2, perimetro_2=perimetro_2, area_2=area_2)
    else:
        # Passo 1: Emitir a mensagem e a categoria do flash
        flash("Preencha o campo para realizar o cálculo!", 'alert-danger')
    return render_template("geometria.html")

@app.route('/quadrado', methods=['GET', 'POST'])
def quadrado():
    if request.method == 'POST':
        n3 = int(request.form['form-n3'])
        perimetro_3 = n3 * 4
        area_3 = n3 * n3
        flash("Cálculo realizado!", 'alert-success')
        return render_template("geometria.html", n3=n3, perimetro_3=perimetro_3, area_3=area_3)
    else:
        # Passo 1: Emitir a mensagem e a categoria do flash
        flash("Preencha o campo para realizar o cálculo!", 'alert-danger')
    return render_template("geometria.html")

@app.route('/hexagono', methods=['GET', 'POST'])
def hexagono():
    if request.method == 'POST':
        n4 = int(request.form['form-n4'])
        perimetro_4 = n4 * 6
        area_4 = n4 * n4 / 2 * 6
        flash("Cálculo realizado!", 'alert-success')
        return render_template("geometria.html", n4=n4, perimetro_4=perimetro_4, area_4=area_4)
    else:
            # Passo 1: Emitir a mensagem e a categoria do flash
            flash("Preencha o campo para realizar o cálculo!", 'alert-danger')
    return render_template("geometria.html")

@app.route('/animais')
def animais():
    return render_template('animais.html')

@app.route('/gatos')
def listar_gatos(): #Esse DEF precisa ser um VERBO
    gatos = routes.get_gatos()

    for gato in gatos:
        gato["temperament"] = gato["temperament"].split(',')
        gato["image"] = routes.get_image()["url"]

    return render_template('gatos.html', gatos=gatos)

# TODO Final do código

if __name__ == '__main__':
    app.run(debug=True)
