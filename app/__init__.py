import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(basedir, '.env'))
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'apenas-desenvolvimento-altere-no-servidor'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'data.sqlite')),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        STUDENT_NAME=os.environ.get('STUDENT_NAME', 'Leonardo Macedo Aurieni'),
        STUDENT_PRONTUARIO=os.environ.get('STUDENT_PRONTUARIO', 'PT3035867')
    )
    if test_config:
        app.config.update(test_config)

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    from .main import main
    app.register_blueprint(main)

    @app.errorhandler(404)
    def not_found(error):
        from flask import request
        from .main.views import contexto
        if request.path in ('/professores', '/alunos', '/cursos', '/ocorrencias'):
            return render_template('indisponivel.html', **contexto()), 404
        return render_template('error.html', mensagem='Página não encontrada.', codigo=404), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('error.html', mensagem='Ocorreu um erro interno. Tente novamente.', codigo=500), 500

    return app
