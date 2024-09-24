# app.py
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config.from_object('config.Config')

# Formulário para cadastro
class MedicalForm(FlaskForm):
    name = StringField('Nome Completo', validators=[DataRequired()])
    blood_type = SelectField('Tipo Sanguíneo', choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')])
    medication = TextAreaField('Toma algum remédio controlado?', validators=[DataRequired()])
    surgery = TextAreaField('Já passou por cirurgia?', validators=[DataRequired()])
    family_diseases = TextAreaField('Histórico de doença na família?', validators=[DataRequired()])
    allergies = TextAreaField('Possui alergia a algum remédio?', validators=[DataRequired()])
    chronic_disease = TextAreaField('Possui doença crônica?', validators=[DataRequired()])
    submit = SubmitField('Gerar Cartão')

# Página inicial com formulário
@app.route('/', methods=['GET', 'POST'])
def index():
    form = MedicalForm()
    if form.validate_on_submit():
        # Passa os dados para a próxima página
        return redirect(url_for('card', 
            name=form.name.data,
            blood_type=form.blood_type.data,
            medication=form.medication.data,
            surgery=form.surgery.data,
            family_diseases=form.family_diseases.data,
            allergies=form.allergies.data,
            chronic_disease=form.chronic_disease.data
        ))
    return render_template('form.html', form=form)

# Página do cartão virtual
@app.route('/card')
def card():
    # Obtém os dados do formulário para renderizar no cartão
    name = request.args.get('name')
    blood_type = request.args.get('blood_type')
    medication = request.args.get('medication')
    surgery = request.args.get('surgery')
    family_diseases = request.args.get('family_diseases')
    allergies = request.args.get('allergies')
    chronic_disease = request.args.get('chronic_disease')
    
    return render_template('card.html', 
        name=name,
        blood_type=blood_type,
        medication=medication,
        surgery=surgery,
        family_diseases=family_diseases,
        allergies=allergies,
        chronic_disease=chronic_disease
    )

if __name__ == '__main__':
    app.run(debug=True)
