import click
from flask_migrate import Migrate
from app import create_app, db
from app.models import Disciplina

app = create_app()


@app.cli.command('init-db')
def init_db():
    """Cria as tabelas do SQLite sem apagar registros existentes."""
    with app.app_context():
        db.create_all()
    click.echo('[OK] Banco inicializado.')


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Disciplina': Disciplina}


if __name__ == '__main__':
    app.run(debug=True)
