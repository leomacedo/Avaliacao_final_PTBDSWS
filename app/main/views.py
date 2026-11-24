from datetime import datetime, timezone, timedelta
from flask import current_app, flash, redirect, render_template, request, url_for
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from .. import db
from ..models import Disciplina
from . import main
from .forms import DisciplinaForm


def contexto():
    # Horário oficial de Brasília (UTC-3), sem precisar de bibliotecas extras.
    agora = datetime.now(timezone(timedelta(hours=-3)))
    return {'data_hora': agora.strftime('%d/%m/%Y %H:%M:%S')}


@main.route('/')
def index():
    return render_template('index.html', nome=current_app.config['STUDENT_NAME'], prontuario=current_app.config['STUDENT_PRONTUARIO'], **contexto())


@main.route('/disciplinas', methods=['GET', 'POST'])
def disciplinas():
    form = DisciplinaForm()
    if form.validate_on_submit():
        nome = form.nome.data.strip()
        if not nome:
            flash('Informe o nome da disciplina.', 'warning')
        elif Disciplina.query.filter(func.lower(Disciplina.nome) == nome.lower()).first():
            flash('Esta disciplina já está cadastrada.', 'warning')
        else:
            db.session.add(Disciplina(nome=nome, semestre=form.semestre.data))
            try:
                db.session.commit()
                flash('Disciplina cadastrada com sucesso!', 'warning')
                return redirect(url_for('main.disciplinas'))
            except IntegrityError:
                db.session.rollback()
                flash('Esta disciplina já está cadastrada.', 'warning')
    if request.method == 'POST' and not form.validate_on_submit():
        flash('Verifique os campos do formulário antes de cadastrar.', 'warning')
    disciplinas_cadastradas = Disciplina.query.order_by(Disciplina.id.asc()).all()
    return render_template('disciplinas.html', form=form, disciplinas=disciplinas_cadastradas, **contexto())
