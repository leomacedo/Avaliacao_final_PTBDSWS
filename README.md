# Avaliação semestral: Cadastro de Disciplinas

Aplicação Flask modular baseada nos padrões usados no repositório `leomacedo/PTBDSWS`: Blueprint, Flask-Bootstrap, Flask-WTF, Flask-SQLAlchemy e Flask-Migrate.

## Requisitos atendidos

- Apenas as rotas `/` e `/disciplinas`. Os links `/professores`, `/alunos`, `/cursos` e `/ocorrencias` são atendidos pelo tratamento de erro **404**, que exibe **Não disponível**, sem cadastrar rotas extras.
- Página inicial com nome e prontuário configuráveis por `.env`.
- Data e hora de Brasília (UTC-3) apresentadas nas páginas.
- Formulário para nome de disciplina e semestre do 1º ao 6º, com CSRF e validações.
- Cadastro incremental no banco SQLite e recuperação dos registros em ordem de cadastro.
- Mensagem Bootstrap amarela depois do cadastro; tratamento de erro 404/500 e validações.
- Templates com herança (`base.html`) e classe SQLAlchemy (`Disciplina`).

## Como executar no VS Code (Windows / PowerShell)

Abra a pasta `avaliacao_semestral` no VS Code e execute:

```powershell
py -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"
```

Copie o resultado para `SECRET_KEY` no `.env`, e confira seu nome e prontuário. Em seguida:

```powershell
flask --app flasky db upgrade
flask --app flasky run --debug
```

Abra http://127.0.0.1:5000. Para parar: `Ctrl+C`.

### Banco e migrações

A pasta `migrations/` **já está incluída** neste pacote. Para um banco novo, use `flask --app flasky db upgrade` (não execute `db init` e não gere outra migration inicial). Isso cria a tabela `disciplinas` e registra sua versão.

**Se você já tem um `data.sqlite` com disciplinas e aplicou anteriormente `flask --app flasky db stamp head`, mantenha esse banco:** basta executar `flask --app flasky db upgrade` quando necessário. Nunca apague o banco existente apenas para atualizar as telas.

## Como publicar no PythonAnywhere

1. Crie um repositório **novo** no GitHub para esta avaliação e faça o commit dos arquivos do projeto, incluindo a pasta `app/`, `requirements.txt` e `README.md`. Não envie `.env`, `venv/` ou `data.sqlite`.
2. No Bash do PythonAnywhere, clone o repositório e entre na pasta:

   ```bash
   git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
   cd SEU-REPOSITORIO
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

3. Edite `.env` (`nano .env`) com uma chave aleatória, nome e prontuário corretos.
4. Rode `flask --app flasky db upgrade` (a migration inicial já acompanha o repositório).
5. Na aba **Web**, crie uma aplicação com **Manual configuration** (Python compatível com o virtualenv). Defina o Virtualenv para `/home/SEU-USUARIO/SEU-REPOSITORIO/venv`.
6. No arquivo WSGI, remova o exemplo padrão e use:

   ```python
   import sys
   projeto = '/home/SEU-USUARIO/SEU-REPOSITORIO'
   if projeto not in sys.path:
       sys.path.insert(0, projeto)
   from flasky import app as application
   ```

7. Clique em **Reload** na aba Web. Acesse seu site e confira `/disciplinas`.
8. Tire um **print da página inicial** exibindo seu nome e prontuário e adicione ao repositório (por exemplo, `screenshot-inicial.png`).

## Testes

```powershell
python -m unittest discover -s tests -v
```

## Organização

```text
app/
  __init__.py
  models.py
  main/
    __init__.py
    forms.py
    views.py
  templates/
    base.html
    index.html
    disciplinas.html
    indisponivel.html
    error.html
flasky.py
requirements.txt
.env.example
```

> Observação: como o enunciado só autoriza `/` e `/disciplinas`, os caminhos dos outros módulos retornam **404** com a página "Não disponível" pelo tratamento de erros, sem registrar novas rotas.
