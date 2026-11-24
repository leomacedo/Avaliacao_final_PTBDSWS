from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length


class DisciplinaForm(FlaskForm):
    nome = StringField('Cadastre a nova disciplina e o semestre associado:', validators=[DataRequired(message='Informe o nome da disciplina.'), Length(max=120, message='Use até 120 caracteres.')])
    semestre = RadioField('Semestre', choices=[(i, f'{i}º semestre') for i in range(1, 7)], coerce=int, validators=[InputRequired(message='Escolha um semestre.')])
    submit = SubmitField('Cadastrar')
