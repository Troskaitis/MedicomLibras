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
from datetime import datetime


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
    

class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Relacionamento com o usuário
    name = db.Column(db.String(150), nullable=False)
    blood_type = db.Column(db.String(3), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    rg = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(20), nullable=False)
    sus_number = db.Column(db.String(20), nullable=False)
    cid = db.Column(db.String(10), nullable=False)
    medication = db.Column(db.Text, nullable=False)
    surgery = db.Column(db.Text, nullable=False)
    family_diseases = db.Column(db.Text, nullable=False)
    allergies = db.Column(db.Text, nullable=False)
    chronic_disease = db.Column(db.Text, nullable=False)

    user = db.relationship('User', backref='medical_records')  # Relacionamento com o modelo User


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

# Página Sobre
@app.route('/informative')
@login_required
def informative():
    return render_template('informative.html')

# Página inicial com formulário (restrita a usuários logados)
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = MedicalForm()

    # Verifique se já existe um registro médico para o usuário logado
    existing_record = MedicalRecord.query.filter_by(user_id=current_user.id).first()
    
    # Preenche o formulário com os dados existentes, se houver
    if existing_record and request.method == 'GET':
        form.name.data = existing_record.name
        form.blood_type.data = existing_record.blood_type
        form.birth_date.data = existing_record.birth_date
        form.rg.data = existing_record.rg
        form.cpf.data = existing_record.cpf
        form.sus_number.data = existing_record.sus_number
        form.cid.data = existing_record.cid
        form.medication.data = existing_record.medication
        form.surgery.data = existing_record.surgery
        form.family_diseases.data = existing_record.family_diseases
        form.allergies.data = existing_record.allergies
        form.chronic_disease.data = existing_record.chronic_disease

    # Quando o formulário é enviado
    if form.validate_on_submit():
        if existing_record:
            # Atualiza o registro existente com as novas informações
            existing_record.name = form.name.data
            existing_record.blood_type = form.blood_type.data
            existing_record.birth_date = form.birth_date.data
            existing_record.rg = form.rg.data
            existing_record.cpf = form.cpf.data
            existing_record.sus_number = form.sus_number.data
            existing_record.cid = form.cid.data
            existing_record.medication = form.medication.data
            existing_record.surgery = form.surgery.data
            existing_record.family_diseases = form.family_diseases.data
            existing_record.allergies = form.allergies.data
            existing_record.chronic_disease = form.chronic_disease.data
        else:
            # Cria um novo registro se nenhum existir
            new_record = MedicalRecord(
                user_id=current_user.id,
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
            )
            db.session.add(new_record)
        
        # Confirma a transação para salvar as alterações
        db.session.commit()
        flash('Dados médicos atualizados com sucesso!', 'success')
        return redirect(url_for('card'))

    return render_template('form.html', form=form)


# Página do cartão virtual (restrita a usuários logados)
@app.route('/card')
@login_required
def card():
    record = MedicalRecord.query.filter_by(user_id=current_user.id).first()
    if record:
        birth_date_formatted = record.birth_date.strftime('%d/%m/%Y')
        return render_template('card.html', record=record, birth_date=birth_date_formatted)
    else:
        flash('Nenhum dado médico encontrado para o usuário.', 'info')
        return redirect(url_for('index'))

    return render_template('card.html', 
        name=name,
        blood_type=blood_type,
        birth_date=birth_date_formatted,
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
    
# Definir o caminho absoluto para a pasta static
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.static_folder = os.path.join(BASE_DIR, 'static')

# Opcional: Função helper para verificar arquivos estáticos
def verify_static_file(filename):
    filepath = os.path.join(app.static_folder, filename)
    if not os.path.exists(filepath):
        print(f"Arquivo não encontrado: {filepath}")
        return False
    return True

@app.before_request
def check_static_files():
    # Verificar arquivos críticos no início
    verify_static_file('logo.png')
    verify_static_file('background.png')    


@app.route('/generate_qrcode')
@login_required
def generate_qrcode():
    # O conteúdo do QR Code pode ser o ID do usuário, ou qualquer dado relevante
    data = 'https://web-production-a5052.up.railway.app/login'
    
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
