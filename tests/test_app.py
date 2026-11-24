import unittest
from app import create_app, db
from app.models import Disciplina


class TestAvaliacao(unittest.TestCase):
    def setUp(self):
        self.app = create_app({'TESTING': True, 'SECRET_KEY': 'teste', 'SQLALCHEMY_DATABASE_URI': 'sqlite://', 'WTF_CSRF_ENABLED': False})
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_apenas_duas_rotas(self):
        rotas = {r.rule for r in self.app.url_map.iter_rules() if r.endpoint != 'static' and not r.endpoint.startswith('bootstrap.')}
        self.assertEqual(rotas, {'/', '/disciplinas'})

    def test_modulos_indisponiveis(self):
        for nome in ('professores', 'alunos', 'cursos', 'ocorrencias'):
            resposta = self.client.get('/' + nome)
            self.assertEqual(resposta.status_code, 404)
            self.assertIn('Não disponível'.encode(), resposta.data)

    def test_rotas_inexistentes_nao_sao_modulos(self):
        resposta = self.client.get('/qualquer-coisa')
        self.assertEqual(resposta.status_code, 404)
        self.assertIn('Página não encontrada'.encode(), resposta.data)

    def test_pagina_inicial_nome_prontuario_e_horario(self):
        resposta = self.client.get('/')
        self.assertIn('Avaliação semestral'.encode(), resposta.data)
        self.assertIn('Aluno: Leonardo Macedo Aurieni'.encode(), resposta.data)
        self.assertIn('Prontuário: PT3035867'.encode(), resposta.data)
        self.assertIn('A data e hora local é'.encode(), resposta.data)

    def test_indisponivel_com_titulo_e_horario(self):
        resposta = self.client.get('/professores')
        self.assertEqual(resposta.status_code, 404)
        self.assertIn('<h1>Não disponível</h1>'.encode(), resposta.data)
        self.assertIn('A data e hora local é'.encode(), resposta.data)
        self.assertNotIn('Aluno:'.encode(), resposta.data)

    def test_cadastro_e_persistencia(self):
        resposta = self.client.post('/disciplinas', data={'nome': 'Redes', 'semestre': '4'}, follow_redirects=True)
        self.assertIn('Disciplina cadastrada com sucesso!'.encode(), resposta.data)
        self.assertIn('4º semestre'.encode(), resposta.data)
        self.assertEqual(Disciplina.query.count(), 1)

    def test_validacoes(self):
        self.client.post('/disciplinas', data={'nome': 'Redes', 'semestre': '4'})
        self.client.post('/disciplinas', data={'nome': 'redes', 'semestre': '3'})
        self.assertEqual(Disciplina.query.count(), 1)
        self.client.post('/disciplinas', data={'nome': 'Teste', 'semestre': '7'})
        self.assertEqual(Disciplina.query.count(), 1)


if __name__ == '__main__':
    unittest.main()
