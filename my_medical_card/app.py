from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms.fields import DateField
import qrcode
import os
from io import BytesIO
from flask import send_file


app = Flask(__name__)
app.config.from_object('config.Config')

# Configurações de banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecret'

# Inicializando banco de dados e gerenciador de login
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Modelo de usuário
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Carregar o usuário
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Formulário de login
class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

# Formulário de registro
class RegisterForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirme a Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

# Formulário médico
class MedicalForm(FlaskForm):
    name = StringField('Nome Completo', validators=[DataRequired()])
    blood_type = SelectField('Tipo Sanguíneo', choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')])
    birth_date = DateField('Data de Nascimento', format='%Y-%m-%d', validators=[DataRequired()])
    rg = StringField('RG', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired()])
    sus_number = StringField('Número do Cartão SUS', validators=[DataRequired()])
    cid = StringField('CID', validators=[DataRequired()])
    medication = TextAreaField('Toma algum remédio controlado?', validators=[DataRequired()])
    surgery = TextAreaField('Já passou por cirurgia?', validators=[DataRequired()])
    family_diseases = TextAreaField('Histórico de doença na família?', validators=[DataRequired()])
    allergies = TextAreaField('Possui alergia a algum remédio?', validators=[DataRequired()])
    chronic_disease = TextAreaField('Possui doença crônica?', validators=[DataRequired()])
    submit = SubmitField('Gerar Cartão')

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos', 'danger')
    return render_template('login.html', form=form)

# Página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Conta criada com sucesso! Faça o login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Página inicial com formulário (restrita a usuários logados)
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = MedicalForm()
    if form.validate_on_submit():
        return redirect(url_for('card', 
            name=form.name.data,
            blood_type=form.blood_type.data,
            birth_date=form.birth_date.data,
            rg=form.rg.data,
            cpf=form.cpf.data,
            sus_number=form.sus_number.data,
            cid=form.cid.data,
            medication=form.medication.data,
            surgery=form.surgery.data,
            family_diseases=form.family_diseases.data,
            allergies=form.allergies.data,
            chronic_disease=form.chronic_disease.data
        ))
    return render_template('form.html', form=form)

# Página do cartão virtual (restrita a usuários logados)
@app.route('/card')
@login_required
def card():
    name = request.args.get('name')
    blood_type = request.args.get('blood_type')
    birth_date = request.args.get('birth_date')
    rg = request.args.get('rg')
    cpf = request.args.get('cpf')
    sus_number = request.args.get('sus_number')
    cid = request.args.get('cid')
    medication = request.args.get('medication')
    surgery = request.args.get('surgery')
    family_diseases = request.args.get('family_diseases')
    allergies = request.args.get('allergies')
    chronic_disease = request.args.get('chronic_disease')

    return render_template('card.html', 
        name=name,
        blood_type=blood_type,
        birth_date=birth_date,
        rg=rg,
        cpf=cpf,
        sus_number=sus_number,
        cid=cid,
        medication=medication,
        surgery=surgery,
        family_diseases=family_diseases,
        allergies=allergies,
        chronic_disease=chronic_disease,
        user=current_user  # Passando o usuário atual para o template
    )
    
@app.route('/generate_qrcode')
@login_required
def generate_qrcode():
    # O conteúdo do QR Code pode ser o ID do usuário, ou qualquer dado relevante
    data = f'User ID: {current_user.id}, Username: {current_user.username}'
    
    # Gerar o QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Criar imagem em memória (sem salvar no disco)
    img = qr.make_image(fill='black', back_color='white')
    buf = BytesIO()
    img.save(buf)
    buf.seek(0)
    
    # Enviar a imagem como resposta
    return send_file(buf, mimetype='image/png')

# Rota para logout
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado!', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Criação das tabelas no banco de dados
    app.run(debug=True)
