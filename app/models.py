from . import db


class Disciplina(db.Model):
    __tablename__ = 'disciplinas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False, unique=True, index=True)
    semestre = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Disciplina {self.nome} - {self.semestre}º semestre>'
